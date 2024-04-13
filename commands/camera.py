import cv2


class StartCamera:
    def __init__(self):
        # define a video capture object 
        self.vid = cv2.VideoCapture(0) 

    def __del__(self):
        # After the loop release the cap object 
        self.vid.release() 
        # Destroy all the windows 
        cv2.destroyAllWindows() 
    
    def provideFrame(self):
        
            # Capture the video frame 
            # by frame 
            ret, frame = self.vid.read() 
            #frame = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
            
            cv2.imshow("Camera", frame)
            # the 'q' button is set as the 
            # quitting button you may use any 
            # desired button of your choice 

            return frame

            
  
