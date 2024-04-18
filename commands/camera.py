import cv2


class StartCamera:
    def __init__(self):
        # define a video capture object 
        pipeline = (
            'libcamerasrc ! '
            'video/x-raw,format=(string)YUY2,width=640,height=480,framerate=15/1 ! '
            'videoconvert ! '
            'video/x-raw,format=(string)BGR ! '
            'appsink'
        )
        self.vid = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER) 

    def __del__(self):
        # After the loop release the cap object 
        self.vid.release() 
        # Destroy all the windows 
        cv2.destroyAllWindows() 
    
    def provideFrame(self):
        
            # Capture the video frame 
            # by frame 
            ret, frame = self.vid.read() 

            return ret, frame

    def cameraStop(self):
        self.vid.release() 
        # Destroy all the windows 
        cv2.destroyAllWindows() 

            
  
