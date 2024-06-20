import cv2
import threading
import time
import heapq
import queue
from signDetection import Segmentation
from categorization import Categorization
from camera import StartCamera
from embedded.eCar import Car
from lineFollower import LineFollower
from drawFrames import FrameDrawer

running = True

frame_available_condition = threading.Condition()
sign_detected_event = threading.Event()

actual_speed = 0

frame = None

imageQueue = queue.Queue()

previous_sign = ""
signType = ""

signsQueue = []

mySegmentator = Segmentation()
myCategorizer = Categorization()
myCar = Car("ttyUSB0", 115200)
myLineFollower = LineFollower()
myFrameDrawer = FrameDrawer()


def captureFrames():
    global running, frame
    myCamera = StartCamera()
    print("Capture thread started.")
    while running:
        ret, new_frame = myCamera.provideFrame()
        if ret:
            with frame_available_condition:
                frame = new_frame
                frame_available_condition.notify_all()
        else:
            print("Failed to capture frame")
    myCamera.cameraStop()
    print("Capture thread closed.")

def signDetection():
    global running, frame
    print("Detection thread started.")
    sign_priority_map = {"Stop": 1, "Pedestrian": 2, "Yield": 3, "Priority": 4, "No Sign": 5}
    colors = ("Teal", "Green", "Gold")
    lineSizes = (2, 2, 2)
    lastSign = None

    while running:
        with frame_available_condition:
            frame_available_condition.wait()

        try:
            if frame is not None:
                signFrame = frame.copy()
                masks = mySegmentator.detectAllSigns(signFrame)
                signs = []

                for mask in masks:
                    currentSigns = myCategorizer.categorizeSigns(mask[0], mask[1])

                    if currentSigns is not None:
                        signs.extend(list(currentSigns))

                if signs is not None:
                    detectedSignsImg = myFrameDrawer.drawSigns(signFrame, signs, colors, lineSizes)
                    cv2.imshow("Detected Signs", detectedSignsImg)
                    cv2.waitKey(2)
                    cv2.imshow("Original image", signFrame)

            #     most_important_sign = None
            #     highest_priority = float('inf')

            #     if len(signs) == 0:
            #         most_important_sign = "No Sign"
            #         highest_priority = 5

            #     for sign in signs:
            #         sign_priority = sign_priority_map.get(sign[1], 5)
            #         if sign_priority < highest_priority:
            #             highest_priority = sign_priority
            #             most_important_sign = sign[1]

            # if most_important_sign and most_important_sign != lastSign:
            #     lastSign = most_important_sign
            #     while not signs_to_process.empty():
            #         priority, sign = signs_to_process.get()
            #     signs_to_process.put((highest_priority, most_important_sign))
            #     sign_detected_event.set()

        except Exception as e:
            print(e)


    print("Detection thread closed.")

def signReaction():
    global running
    print("Reaction thread started.")
    while running:
        try:
            sign_detected_event.wait()
            if not signs_to_process.empty():
                priority, sign = signs_to_process.get()

            take_action_based_on_sign(sign)
            sign_detected_event.clear()
        except Exception as e:
            print(e)

    print("Reaction thread closed.")

def take_action_based_on_sign(signType):
    global actual_speed

    def yield_command():
        global actual_speed
        print("Yielding.")
        for velocity in range(actual_speed, -1, -1):
            myCar.setVelocity(velocity)
            time.sleep(0.1)  
            print(velocity)
        print("Velocity reduced to 0.")
        actual_speed = 0

    actions = {
        "Stop": lambda: (myCar.setVelocity(0), print("Stopping.")),
        "Pedestrian": lambda: (myCar.setVelocity(10), print("Slowing down, pedestrians ahead.")),
        "Yield": lambda: yield_command(),
        "Priority": lambda: (myCar.setVelocity(20), print("Speeding up, priority road ahead."),),
        "No Sign": lambda: (myCar.setVelocity(20), print("No sign detected"))
    }

    if signType == "Stop" or signType == "No Sign":
        actual_speed = 0
    elif signType == "Pedestrian":
        actual_speed = 10
    elif signType == "Priority":
        actual_speed = 30

    action = actions.get(signType, lambda: None)
    action()
    print(actual_speed)

def lineFollower():
    global running, frame
    color = "Magenta"
    lineSize = 1
    print("Line follower thread started.")
    while running:
        with frame_available_condition:
            frame_available_condition.wait()
        try:
            if frame is not None:
                
                topView, mainLine = myLineFollower.findLine(frame)
                if mainLine is not None:
                    line = ((mainLine[0], mainLine[1]), (mainLine[2], mainLine[3]))
                    topView = myFrameDrawer.drawLine(topView, line, color, lineSize)
                    slope = round(calculateSlope(mainLine), 3)

                    myCar.setSteering(slope)
                    previousSlope = slope
                
                cv2.imshow("Top View", topView)
                cv2.waitKey(2)
        except Exception as e:
            print(e)

    print("Line follower thread closed.")

def calculateSlope(line):
    x1, y1, x2, y2 = line
    return (y1 - y2) / (x2 - x1) if (x2 - x1) != 0 else float('inf')


def is_heap_empty(heap):
    return not heap


def key_event_handler(event, x, y, flags, param):
    global running
    if event == cv2.EVENT_LBUTTONDOWN and flags & cv2.EVENT_FLAG_CTRLKEY:
        running = False
        with frame_available_condition:
            frame_available_condition.notify_all() 
            sign_detected_event.set()

# Main function
signs_to_process = queue.Queue()  

def main():
    global myCar, myDetector, myFrameDrawer, myLineFollower
    global running
    running = True

    capture_thread = threading.Thread(target=captureFrames)
    detection_thread = threading.Thread(target=signDetection)
    reaction_thread = threading.Thread(target=signReaction)
    lineFollower_thread = threading.Thread(target=lineFollower)

    capture_thread.start()
    detection_thread.start()
    reaction_thread.start()
    lineFollower_thread.start()

    cv2.namedWindow('Detected Signs')
    cv2.setMouseCallback('Detected Signs', key_event_handler)

    capture_thread.join()
    detection_thread.join()
    reaction_thread.join()
    lineFollower_thread.join()


    cv2.destroyAllWindows()
    print("Gracefully shutdown all threads.")
    del myCar
    del mySegmentator
    del myCategorizer
    del myFrameDrawer
    del myLineFollower

if __name__ == "__main__":
    main()