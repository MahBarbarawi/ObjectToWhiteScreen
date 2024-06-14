import cv2

class WhiteScreen:

    def __init__(self,shape= (1324,900)):
        self.white=cv2.imread("./whitePlusSaved.png")
        self.white=cv2.cvtColor(self.white, cv2.COLOR_RGB2RGBA)
        self.dim=shape
        self.white = cv2.resize(self.white,  self.dim, interpolation=cv2.INTER_AREA)
    def plusReGenerate(self,colorLine=(0,0,0), thi=1,li=20 ):

        self.white=cv2.line(self.white,
                           (self.white.shape[1] // 2, self.white.shape[0] // 2 - li),
                           (self.white.shape[1] // 2, self.white.shape[0] // 2 + li),
                           colorLine,
                           thi)
        self.white=cv2.line(self.white,
                           (self.white.shape[1] // 2 - li,self.white.shape[0] // 2),
                           (self.white.shape[1] // 2 + li,self.white.shape[0] // 2),
                           colorLine,
                           thi)

    def clearScreen(self):
        self.white=cv2.imread("./whitePlusSaved.png")
        self.white = cv2.cvtColor(self.white, cv2.COLOR_RGB2RGBA)
        self.white = cv2.resize(self.white, self.dim, interpolation=cv2.INTER_AREA)