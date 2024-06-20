import cv2
import numpy as np

class LineFollower:
    def __init__(self):
        # Defining the resulting window dimmensions
        self.width = 640
        self.height = 480
        boxWidth = 400
        boxHeight = 300

        p1 = ((self.width - boxWidth) / 2, (self.height - boxHeight) / 2)
        p2 = ((self.width + boxWidth) / 2, (self.height - boxHeight) / 2)
        p3 = ((self.width - boxWidth) / 2, (self.height + boxHeight) / 2)
        p4 = ((self.width + boxWidth) / 2, (self.height + boxHeight) / 2)

        self.centerBox = (p1, p2, p3, p4)

        # Defining the extraction trapeze
        trapezeShape = np.float32([
            [136, 253],  # Top-left corner
            [516, 252],  # Top-right corner
            [580, 453],  # Bottom-right corner
            [52, 474],   # Bottom-left corner
            ])

        # Defining the resulting window
        windowShape = np.float32([
            [0, 0],
            [self.width, 0],
            [self.width, self.height],
            [0, self.height]
            ])

        self.transformMatrix = self.__computeTransformMatrix(trapezeShape, windowShape)

    def __computeTransformMatrix(self, trapezeShape, windowShape):
        matrix = cv2.getPerspectiveTransform(trapezeShape, windowShape)
        return matrix

    def __convertImage(self, frame, matrix):
        topView = cv2.warpPerspective(frame, matrix, (self.width, self.height))
        return topView

    def __processImage(self, topView):
        topView = cv2.cvtColor(topView, cv2.COLOR_BGR2GRAY) 
        #topView = cv2.cvtColor(topView, cv2.COLOR_BGR2HSV)
        #blurred_image = cv2.GaussianBlur(topView, (5, 5), 0)
        _, topView = cv2.threshold(topView, 127, 255, cv2.THRESH_BINARY)
        # lowerYellow = np.array([20, 75, 75])
        # upperYellow = np.array([40, 255, 255])
        # lowerWhite = np.array([0, 0, 200])
        # upperWhite = np.array([179, 55, 255])
        # mask = cv2.inRange(topView, lowerWhite, upperWhite)

        
        # kernel_size = 5
        # kernel = np.ones((kernel_size, kernel_size), np.uint8)

        # # Morphological closing to remove noise inside the white line
        # closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # # Morphological opening to remove noise outside the white line
        # opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

        # kernel = np.ones((6,6), np.uint8)
        # mask = cv2.dilate(mask, kernel, iterations=3)
        # mask = cv2.erode(mask, kernel, iterations=2)
        # cv2.imshow("White", topView)
        return topView

    def __skeletonize(self, frame):
        skeleton = np.zeros(frame.shape, np.uint8)
        eroded = np.zeros(frame.shape, np.uint8)
        temp = np.zeros(frame.shape, np.uint8)

        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

        if cv2.countNonZero(frame) == 0 or np.all(frame == 255):
            return None

        while True:
            cv2.erode(frame, element, eroded)
            cv2.dilate(eroded, element, temp)
            cv2.subtract(frame, temp, temp)
            cv2.bitwise_or(skeleton, temp, skeleton)
            frame, eroded = eroded, frame  # Swap instead of copy
            

            if cv2.countNonZero(frame) == 0:
                cv2.imshow("skeleton", skeleton)
                return skeleton


        

    def __detectLine(self, edges):
        try:
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

            # Converting the lines from polar coordinate system to cartesian
            if lines is not None:
                # Assuming the longest line is the main line
                main_line = sorted(lines, key=lambda x: np.linalg.norm((x[0][0] - x[0][2], x[0][1] - x[0][3])), reverse=True)[0]
                return main_line[0]

        except:
            return None

    def __excludeErronousLines(self, lineCoords):
        validLines = []
        for line in lineCoords:
            x0, y0 = line[1]

            xlow, ylow = self.centerBox[0]
            xhigh, yhigh = self.centerBox[3]

            if x0 >= xlow and x0 <= xhigh and y0 >= ylow and y0 <= yhigh:
                validLines.append(line)

        return validLines

    def findLine(self, frame):
        try:
            topView = self.__convertImage(frame, self.transformMatrix)
            #print(f"top:{topView}")
            processedImage = self.__processImage(topView)
            #print(f"proces:{processedImage}")
            skeletonImage = self.__skeletonize(processedImage)
            #print(f"skeleton:{skeletonImage}")

            try:
                if skeletonImage == None:
                    return topView, None
            except:
                x = 1

            mainLine = self.__detectLine(skeletonImage)
            # if len(allLines) != 0:
            #     selectedLines = self.__excludeErronousLines(allLines)

            #     return topView, selectedLines

            # else:
            #     return topView, None

            return topView, mainLine

        except:
            print("bruh")

