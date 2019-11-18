import cv2

class VideoCapture:

    def __init__(self, index = 0):
        self.cap = cv2.VideoCapture(index)

    def is_opened(self):
        return self.cap.isOpened()

    def read(self):
        success, frame = self.cap.read()
        if success:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        else:
            return None

    def release(self):
        self.cap.release()
