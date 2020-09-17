import cv2
import sys
from imutils.video import WebcamVideoStream
class VideoCamera(object):
    def __init__(self):
        url= 'http://192.168.43.1:8000/video'
        self.stream = WebcamVideoStream(url).start()
    def __del__(self):
        self.stream.stop()
    def get_frame(self):
        image =self.stream.read()
        detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        face = detect.detectMultiScale(image, 1.1, 7)
        for(x,y,h,w) in face:
            cv2.rectangle(image, (x, y),(x+w, y+h), (0,0,255), 2)
        ret, jpeg = cv2.imencode('.jpg', image)
        data = []
        data.append(jpeg.tobytes())
        return data
# Get user supplied values

# Load the cascade

