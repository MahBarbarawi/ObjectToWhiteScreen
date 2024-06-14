import cv2



class ObjectDediction:
    def __init__(
            self,
            configPath = './ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt',
            weightsPath = "./frozen_inference_graph.pb",
            thersho = .6,
            ClassName="./coco.names"

    ):
        #net settings
        self.net = cv2.dnn_DetectionModel(weightsPath, configPath)

        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        with open(ClassName, 'rt') as f:
            self.className = f.read().rstrip('\n').split('\n')

        self.thersho=thersho

    def NetSettings(self,):
        #learn Net settings //// editing move __init__
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

    def dedictions(self,img):
        classIds, confs, bbox = self.net.detect(img, confThreshold=self.thersho)
        return classIds, confs, bbox