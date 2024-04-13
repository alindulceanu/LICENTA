from signDetection import SignDetector
from camera import StartCamera
from embbeded.eCar import Car
import cv2
import time

myCamera = StartCamera()
# myCar = Car("ttyUSB0", 9600)
myDetector = SignDetector()

while True:
    frame = myCamera.provideFrame()
    signs = myDetector.detectAllSigns(frame)
    detectedSignsImg = myDetector.drawSigns(frame, signs)
    cv2.imshow("Detected Signs", detectedSignsImg)

    if len(signs) != 0:
        for sign in signs:
            if len(sign) != 0:
                print(sign)
                if sign[0][1] == "Stop":
                    # myCar.setVelocity(0)
                    print("Stop!")

                elif sign[0][1] == "Yield":
                    # myCar.setVelocity(0)
                    # time.sleep(5)
                    # myCar.setVelocity(30)
                    print("Yield")

                elif sign[0][1] == "Priority":
                    print("Priority")

                elif sign[0][1] == "Pedestrian":
                    print("Pedestrian")


    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

