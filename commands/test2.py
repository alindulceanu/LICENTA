import cv2
import numpy as np
from drawFrames import FrameDrawer
from camera import StartCamera


myCamera = StartCamera()
myFrameDrawer = FrameDrawer()

while True:
    ret, frame = myCamera.provideFrame()

    box = ((126,243), (526, 266), (590, 477), (42, 454))
    frame = myFrameDrawer.drawBoxCorners(frame, box, "Green")

    cv2.imshow("Trapeze", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# trapezeShape = np.float32([
#     [226,243],  # Top-left corner
#     [426, 246],  # Top-right corner
#     [608, 341],  # Bottom-right corner
#     [32, 341],   # Bottom-left corner
#     ])