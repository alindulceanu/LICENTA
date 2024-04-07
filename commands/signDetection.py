import cv2
import numpy as np

class signDetection:
    def __init__(self):
        image = 0

    def __del__(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def processFrame(self, image, color):
        # Convert the image to HSV color space for easier color segmentation
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        if color == "Red":
            # Define the range of red color in HSV
            lowerRed = np.array([0, 50, 50])
            upperRed = np.array([10, 255, 255])
            lowerRed2 = np.array([160, 50, 50])
            upperRed2 = np.array([180, 255, 255])

            # Threshold the HSV image to get only red colors
            mask1 = cv2.inRange(hsv, lowerRed, upperRed)
            mask2 = cv2.inRange(hsv, lowerRed2, upperRed2)

            mask = cv2.bitwise_or(mask1, mask2)

        elif color == "Blue":
            lowerBlue = np.array([110, 50, 50])
            upperBlue = np.array([130, 255, 255])

            mask = cv2.inRange(hsv, lowerBlue, upperBlue)

        elif color == "WhiteNYellow":
            lowerYellow = np.array([20, 100, 100])
            upperYellow = np.array([40, 255, 255])

            mask = cv2.inRange(hsv, lowerYellow, upperYellow)
            cv2.imshow("XD", mask)


        kernel = np.ones((10,10), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=3)
        mask = cv2.erode(mask, kernel, iterations=2)
        cv2.imshow("XDD", mask)
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) != 0:
            approx, area = self.findContours(contours)
            return approx, area
        
        else:
            return False
        
    def findContours(self, contours):
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
            area = cv2.contourArea(cnt)

            return approx, area

    def findOctogonSign(self, image): 
        # nu gaseste stop-ul pentru ca se duce direct la yield, trebuie detectate toate contururile, nu numai primul
        try:
            approx, area = self.processFrame(image, 'Red')
        
            if len(approx) == 8 and area > 10000:
                # Get bounding rect of contour
                x, y, w, h = cv2.boundingRect(approx)
                # Draw rectangle around the contour
                cv2.rectangle(self.image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # Put text below the rectangle
                cv2.putText(self.image, "Stop Sign", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                return True, image

            return False, image
        
        except(Exception):
            return False, image
    def findTriangleSign(self, approx):
        try:
            approx, area = self.processFrame(image, 'Red')
        
            if len(approx) == 3 and area > 10000:
                # Get bounding rect of contour
                x, y, w, h = cv2.boundingRect(approx)
                # Draw rectangle around the contour
                cv2.rectangle(self.image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # Put text below the rectangle
                cv2.putText(self.image, "Yield Sign", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                return True, image

            return False, image
        
        except(Exception):
            return False, image

    def findSquareSign(self, approx):
        try:
            approx, area = self.processFrame(image, 'WhiteNYellow')
        
            if len(approx) == 4 and area > 10000:
                # Get bounding rect of contour
                x, y, w, h = cv2.boundingRect(approx)
                # Draw rectangle around the contour
                cv2.rectangle(self.image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # Put text below the rectangle
                cv2.putText(self.image, "Pedestrian Sign", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                return True, image

            return False, image 
        
        except(Exception):
            return False, image

    def detectSigns(self, image):
        self.image = image

        stop = self.findOctogonSign(image)
        yieldSign = self.findTriangleSign(image)
        pedestrianSign = self.findSquareSign(image)
        cv2.imshow("img", self.image)


imageProcessor = signDetection()

imageProcessor.detectSigns(image)

'''
# Load an image
image = cv2.imread('stop4.jpg')

# Detect stop signs
detected, result_image = detect_stop_sign(image)

# Show the result
cv2.imshow('Detected Stop Signs', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
