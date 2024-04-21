import cv2
import numpy as np

class SignDetector:
    def __init__(self):
        pass

    def __del__(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def processFrame(self, image, color):
        hsv = cv2.GaussianBlur(image, (15, 15), 2)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)        

        if color == "Red":
            # Define the range of red color in HSV
            lowerRed = np.array([0, 150, 100])
            upperRed = np.array([10, 255, 255])
            lowerRed2 = np.array([170, 150, 100])
            upperRed2 = np.array([180, 255, 255])

            # Threshold the HSV image to get only red colors
            mask1 = cv2.inRange(hsv, lowerRed, upperRed)
            mask2 = cv2.inRange(hsv, lowerRed2, upperRed2)

            mask = cv2.bitwise_or(mask1, mask2)

        elif color == "Blue":
            lowerBlue = np.array([105, 150, 200])
            upperBlue = np.array([135, 255, 255])

            mask = cv2.inRange(hsv, lowerBlue, upperBlue)

        elif color == "Yellow":
            lowerYellow = np.array([25, 125, 100])
            upperYellow = np.array([35, 255, 255])

            mask = cv2.inRange(hsv, lowerYellow, upperYellow)

        kernel = np.ones((5,5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.erode(mask, kernel, iterations=1)

        return mask
    
    def findAllContours(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        app = []
        contArea = []

        for cnt in contours:
            epsilon = 0.03
            closedPerimeter = True
            perimeter = cv2.arcLength(cnt, closedPerimeter)

            approx = cv2.approxPolyDP(cnt, epsilon * perimeter, closedPerimeter)

            area = cv2.contourArea(cnt)

            app.append(approx)
            contArea.append(area)

        if len(contours) != 0:
            return app, contArea

        return False, False

    def findShapes(self, app, contArea, color):
        signs = []

        for i in range(len(app)):
            x, y, w, h = cv2.boundingRect(app[i])

            if len(app[i]) == 8 and contArea[i] > 3000 and color == "Red":
                signs.append(((x, y, w, h), "Stop", app[i]))

            elif len(app[i]) == 3 and contArea[i] > 3000 and color == "Red":
                signs.append(((x, y, w, h), "Yield", app[i]))

            elif len(app[i]) == 4 and contArea[i] > 3000 and color == "Blue":
                signs.append(((x, y, w, h), "Pedestrian", app[i]))

            elif len(app[i]) == 4 and contArea[i] > 3000 and color == "Yellow":
                signs.append(((x - 10, y - 10, w + 20, h + 20), "Priority", app[i]))
        
        return signs
    
    def drawSigns(self, image, signs):
        for i in range(len(signs)):
            for coords, sign, cont in signs[i]:
                cv2.rectangle(image, (coords[0], coords[1]), (coords[0] + coords[2], coords[1] + coords[3]), (0, 255, 0), 2)
                cv2.drawContours(image, [cont], -1, (255, 0, 0), 3)
                cv2.putText(image,  sign, (coords[0], coords[1] + coords[3] +20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        return image


    def detectAllSigns(self, image):
        maskRed = self.processFrame(image, "Red")
        maskBlue = self.processFrame(image, "Blue")
        maskYellow = self.processFrame(image, "Yellow")
        cv2.imshow("red", maskRed)
        cv2.imshow("blue", maskBlue)
        cv2.imshow("yellow", maskYellow)

        masks = [maskRed, maskBlue, maskYellow]
        colors = ["Red", "Blue", "Yellow"]
        allSigns = []

        for i in range(len(masks)):
            app, cont = self.findAllContours(masks[i])

            if (app, cont) != (False, False):
                signs = self.findShapes(app, cont, colors[i])

                for sign in signs:
                    allSigns.append(sign)

        return allSigns