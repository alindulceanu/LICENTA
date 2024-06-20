import cv2
import numpy as np

class Segmentation:
    def __init__(self):
        pass

    def __del__(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def preProcessing(self, image):
        hsv = cv2.GaussianBlur(image, (11, 11), 0)
        cv2.imshow("Gaussian Blur", hsv)
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
        cv2.imshow("HSV", hsv)

        return hsv      

    def processFrame(self, hsv, color):     

        if color == "Red":
            lowerRed = np.array([0, 130, 140])
            upperRed = np.array([10, 255, 255])
            lowerRed2 = np.array([160, 130, 140])
            upperRed2 = np.array([180, 255, 255])

            mask1 = cv2.inRange(hsv, lowerRed, upperRed)
            mask2 = cv2.inRange(hsv, lowerRed2, upperRed2)

            mask = cv2.bitwise_or(mask1, mask2)

        elif color == "Blue":
            lowerBlue = np.array([100, 130, 50])
            upperBlue = np.array([140, 255, 255])

            mask = cv2.inRange(hsv, lowerBlue, upperBlue)

        elif color == "Yellow":
            lowerYellow = np.array([27, 150, 160])
            upperYellow = np.array([33, 255, 255])

            mask = cv2.inRange(hsv, lowerYellow, upperYellow)
            
        return mask

    def applyMorphologicalOperations(self, mask, kernelSize, dilateIterations, erodeIterations):
        mask = cv2.dilate(mask, kernelSize, iterations = dilateIterations)
        mask = cv2.erode(mask, kernelSize, iterations = erodeIterations)

        return mask

    def detectAllSigns(self, image):
        hsv = self.preProcessing(image)

        maskRed = self.processFrame(hsv, "Red")
        maskBlue = self.processFrame(hsv, "Blue")
        maskYellow = self.processFrame(hsv, "Yellow")

        # cv2.imshow("red", maskRed)
        # cv2.imshow("blue", maskBlue)
        # cv2.imshow("yellow", maskYellow)

        kernelRed = np.ones((3,3), np.uint8)
        maskRed = self.applyMorphologicalOperations(maskRed, kernelRed, 3, 1)

        kernelBlue = np.ones((5,5), np.uint8)
        maskBlue = self.applyMorphologicalOperations(maskBlue, kernelBlue, 3, 1)

        kernelYellow = np.ones((3,3), np.uint8)
        maskYellow = self.applyMorphologicalOperations(maskYellow, kernelYellow, 3, 3)

        cv2.imshow("red", maskRed)
        cv2.imshow("blue", maskBlue)
        cv2.imshow("yellow", maskYellow)



        masks = ((maskRed, "red"), (maskBlue, "blue"), (maskYellow, "yellow"))
        # colors = ["Red", "Blue", "Yellow"]
        # allSigns = []

        # for i in range(len(masks)):
        #     app, cont = self.findAllContours(masks[i])

        #     if (app, cont) != (False, False):
        #         signs = self.findShapes(app, cont, colors[i])

        #         for sign in signs:
        #             allSigns.append(sign)

        return masks