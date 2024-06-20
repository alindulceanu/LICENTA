import cv2

class StartCamera:
    def __init__(self):
        pipeline = (
            'libcamerasrc ! '
            'video/x-raw,format=(string)YUY2,width=640,height=480,framerate=15/1 ! '
            'videoconvert ! '
            'video/x-raw,format=(string)BGR ! '
            'appsink'
        )
        self.vid = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER) 

    def __del__(self):
        self.vid.release() 
        cv2.destroyAllWindows() 
    
    def provideFrame(self):
            ret, frame = self.vid.read() 

            return ret, frame

    def cameraStop(self):
        self.vid.release() 
        cv2.destroyAllWindows() 

            
  
