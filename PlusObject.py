import cv2
import numpy as np

class PlusDedication:
    def __init__(self, model="best.onnx"):
        self.net = cv2.dnn.readNetFromONNX(model)


    def plusCapture(self,img):
        blob = cv2.dnn.blobFromImage(img, scalefactor=1 / 255, size=(640, 640), mean=[0, 0, 0], swapRB=True, crop=False)
        self.net.setInput(blob)
        detections = self.net.forward()[0]
        self.confidences = []
        self.boxes = []
        rows = detections.shape[0]

        img_width, img_height = img.shape[1], img.shape[0]
        x_scale = img_width / 640
        y_scale = img_height / 640
        for i in range(rows):
            row = detections[i]
            confidence = row[4]
            if confidence > 0.7:
                classes_score = row[5:]
                ind = np.argmax(classes_score)
                if classes_score[ind] > 0.5:
                    self.confidences.append(confidence)
                    cx, cy, w, h = row[:4]
                    x1 = int((cx - w / 2) * x_scale)
                    y1 = int((cy - h / 2) * y_scale)
                    width = int(w * x_scale)
                    height = int(h * y_scale)
                    box = np.array([x1, y1, width, height])
                    self.boxes.append(box)

        if self.boxes ==[]:
            return  False
        return True

    def PlusDedictions(self):
        indices = cv2.dnn.NMSBoxes(self.boxes, self.confidences, 0.5, 0.5)
        for i in indices:
            x1, y1, w, h = self.boxes[i]
            cx = (2 * x1 + w) // 2
            cy = (2 * y1 + h) // 2
            space =(w+x1)*(y1 + h)
        print("cx,cy", cx,cy)
        return    cx,cy,(w,h)
        # return x1, y1, w, h
