import cv2
import numpy as np

class LineFollower:
    def __init__(self):
        # Defining the resulting window dimmensions
        self.width = 640
        self.height = 480
        boxWidth = 150
        boxHeight = 100

        p1 = ((self.width - boxWidth) / 2, (self.height - boxHeight) / 2)
        p2 = ((self.width + boxWidth) / 2, (self.height - boxHeight) / 2)
        p3 = ((self.width - boxWidth) / 2, (self.height + boxHeight) / 2)
        p4 = ((self.width + boxWidth) / 2, (self.height + boxHeight) / 2)

        self.centerBox = (p1, p2, p3, p4)

        # Defining the extraction trapeze
        trapezeShape = np.float32([
            [226,243],  # Top-left corner
            [426, 246],  # Top-right corner
            [608, 341],  # Bottom-right corner
            [32, 341],   # Bottom-left corner
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
        lowerYellow = np.array([20, 75, 75])
        upperYellow = np.array([40, 255, 255])

        mask = cv2.inRange(topView, lowerYellow, upperYellow)

        kernel = np.ones((6,6), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=3)
        mask = cv2.erode(mask, kernel, iterations=2)

        edges = cv2.Canny(mask, 150, 160, apertureSize=3)

        return edges

    def __detectLine(self, edges):
        lines = cv2.HoughLines(edges, 1.5, np.pi / 180, 200)
        lineCoords = []

        # Converting the lines from polar coordinate system to cartesian
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            center = (x0, y0)
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            lineCoords.append((((x1, y1), (x2, y2)), center))

        return lineCoords

    def __excludeErronousLines(self, lineCoords, box):
        validLines = []
        for line in lineCoords:
            x0, y0 = line[1]

            xlow, ylow = self.centerBox[0]
            xhigh, yhigh = self.centerBox[3]

            if x0 >= xlow and x0 <= xhigh and y0 >= ylow and y0 <= yhigh:
                validLines.append(line)

        return validLines

    def findLine(self, frame):
        topView = self.__convertImage(frame, self.transformMatrix)
        processedImage = self.__processImage(topView)
        allLines = self.__detectLine(processedImage)
        selectedLines = self.__excludeErronousLines(allLines)

        return topView, selectedLines

