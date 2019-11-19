import numpy as np
import cv2
from threading import Thread


class FrameAnalyzer(Thread):

    _running = False
    _stopped = False
    boxes = []
    con = 0

    def __init__(self, algorithm, trained_model, classes, confidence):
        self.algorithm = algorithm
        self.trained_model = trained_model
        self.classes = classes
        self.confidence = confidence
        super(FrameAnalyzer, self).__init__()

    def set_video_source(self,frame):
        self.frame = frame

    def run(self):
        if self._stopped:
            return self.frame

        self._running = True
        net = cv2.dnn.readNet(self.trained_model, self.algorithm)
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        height, width, channels = self.frame.shape

        blob = cv2.dnn.blobFromImage(self.frame, 0.00392, (416, 416), (0, 0, 0), True, crop = False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        confidences = []
        empty = True
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence_res = scores[class_id]
                if (confidence_res > self.confidence):
                    print(confidence_res)
                    self.con = confidence_res
                    empty = False
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    self.boxes.clear()
                    self.boxes.append([x, y, w, h])

                    confidences.append(confidence_res)
        
        if empty:
            self.boxes.clear()
        
        self._running = False
        return self.frame

    def draw_detection(self, frame_local):
        for i in range(0, len(self.boxes)):
            x, y, w, h = self.boxes[i]
            cv2.rectangle(frame_local, (x,y), (x + w, y + h), (0, 255, 0), 2)
        return frame_local

    def is_running(self):
        return self._running
    
    def stop(self):
        self._stopped = True
        self = FrameAnalyzer(0, 0, 0, 0)
