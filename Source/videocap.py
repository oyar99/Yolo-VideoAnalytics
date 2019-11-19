#External modules
import cv2

'''Class'''
class VideoCapture:

    def __init__(self, index = 0):
        self.cap = cv2.VideoCapture(index)

    def is_opened(self):
        return self.cap.isOpened()

    def read(self):
        success, frame = self.cap.read()
        if success:
            return frame
        else:
            return None

    def release(self):
        self.cap.release()

    def __del__(self):
        self.release()
