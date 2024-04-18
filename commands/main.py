import cv2
import threading
import time
import heapq
import queue
from signDetection import SignDetector
from camera import StartCamera
from embedded.eCar import Car
from lineFollower import LineFollower
from drawFrames import FrameDrawer

running = True

# Event to signal when a frame is available for processing
frame_available_condition = threading.Condition()
signs_to_process = threading.Event()
frame = []

# Thread-safe queue to pass image data
imageQueue = queue.Queue()

previous_sign = ""
signType = ""

# Thread-safe queue to store detected signs
signsQueue = []

# Initialize the camera, sign detector, and car
myCamera = StartCamera()
myDetector = SignDetector()
myCar = Car("ttyUSB0", 115200)
myLineFollower = LineFollower()
myFrameDrawer = FrameDrawer()

# Function to capture frames from the camera
def captureFrames():
    global running, frame
    camera = StartCamera()
    print("Capture thread started.")
    while running:
        ret, new_frame = camera.provideFrame()
        if ret:
            with frame_available_condition:
                frame = new_frame
                frame_available_condition.notify_all()
        else:
            print("Failed to capture frame")
    camera.cameraStop()
    print("Capture thread closed.")

# Function to detect signs and process frames
def signDetection():
    global running, frame
    print("Detection thread started.")
    colors = ("Green", "Blue", "Green")
    lineSizes = (2,1,3)

    while running:
        with frame_available_condition:
            frame_available_condition.wait()

        if frame is not None:
            signs = myDetector.detectAllSigns(frame)
            detectedSignsImg = myFrameDrawer.drawSigns(frame, signs, colors, lineSizes)
            if detectedSignsImg is not None:
                cv2.imshow("Detected Signs", detectedSignsImg)
                cv2.waitKey(2)

            most_important_sign = None
            highest_priority = float('inf')

            for sign in signs:
                if sign:
                    sign_priority_map = {"Stop": 1, "Pedestrian": 2, "Yield": 3, "Priority": 4}
                    sign_priority = sign_priority_map.get(sign[0][1], 5)
                    if sign_priority < highest_priority:
                        highest_priority = sign_priority
                        most_important_sign = sign[0][1]

        if most_important_sign:
            print(f"Detected highest priority sign: {most_important_sign}")
            signs_to_process.put((highest_priority, most_important_sign))  # Send to reaction function
    print("Detection thread closed.")

def signReaction():
    global running, previous_sign
    
    print("Reaction thread started.")
    while running:
        priority, signType = signs_to_process.get()  # Wait until a sign is available
        print(f"Processing {signType} with highest priority from the detection")
        take_action_based_on_sign(signType)
        previous_sign = signType
    print("Reaction thread closed.")

def take_action_based_on_sign(signType):
    actions = {
        "Stop": lambda: myCar.setVelocity(0),
        "Pedestrian": lambda: myCar.setVelocity(13),
        "Yield": lambda: (myCar.setVelocity(0), time.sleep(5), myCar.setVelocity(20)),
        "Priority": lambda: myCar.setVelocity(30)
    }
    action = actions.get(signType, lambda: None)
    action()

def lineFollower():
    global running, frame
    color = "Magenta"
    lineSize = 1
    print("Line follower thread started.")
    while running:
        with frame_available_condition:
            frame_available_condition.wait()  # Wait for a new frame
            if frame is not None:
                # Process the frame for line following
                topView, selectedLines = myLineFollower.findLine(frame)
                frame = myFrameDrawer.drawLineFollower(frame, selectedLines, color, lineSize)

    print("Line follower thread closed.")



def is_heap_empty(heap):
    return not heap

# Function to handle key events
def key_event_handler(event, x, y, flags, param):
    global running
    if event == cv2.EVENT_LBUTTONDOWN and flags & cv2.EVENT_FLAG_CTRLKEY:
        running = False
        #frame_available_condition.set()  # Unblock any threads waiting on this event
        signs_to_process.set()  # Unblock the reaction thread

# Main function
signs_to_process = queue.Queue()  # Simplified to a single queue without using heap

def main():
    global running
    running = True

    capture_thread = threading.Thread(target=captureFrames)
    detection_thread = threading.Thread(target=signDetection)
    reaction_thread = threading.Thread(target=signReaction)

    capture_thread.start()
    detection_thread.start()
    reaction_thread.start()

    cv2.namedWindow('Detected Signs')
    cv2.setMouseCallback('Detected Signs', key_event_handler)

    try:
        while running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Interrupt received, shutting down.")
        running = False
        frame_available_event.set()
        signs_to_process.put((0, 'Exit'))  # Signal reaction thread to exit

    capture_thread.join()
    detection_thread.join()
    reaction_thread.join()

    myCamera.cameraStop()
    cv2.destroyAllWindows()
    print("Gracefully shutdown all threads.")

if __name__ == "__main__":
    main()