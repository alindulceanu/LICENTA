import cv2

# Define the gstreamer pipeline using libcamera
gst_pipeline = "libcamerasrc ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! appsink"

# Capture video
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Do something with the frame here
    # For example, print its dimensions
    print(f"Frame dimensions: {frame.shape}")
    
    # To exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
