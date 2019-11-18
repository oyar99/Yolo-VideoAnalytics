import cv2
import numpy as np

#Load YOLO algorithm
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = ["person"]

layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

#Read livestream
cap = cv2.VideoCapture(0)
while (cap.isOpened()):
    success, image = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
     
    height, width, channels = image.shape
    #Detect object
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop = False)

    net.setInput(blob)
    outs = net.forward(outputlayers)

    confidences = []
    boxes = []

    #show info on the screen
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.9:
                print(confidence)
                #A person has been detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                #Draw rectangle around object
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(confidence)

    for i in range(0, len(boxes)):
        x, y, w, h = boxes[i]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) 
    
    cv2.imshow("Image", image)
cap.release()
cv2.destroyAllWindows()
