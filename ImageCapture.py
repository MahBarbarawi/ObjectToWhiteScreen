import cv2
import numpy as np

import requests
import imutils

from rembg import remove

from ObjectModel import ObjectDediction
from whiteScreen import WhiteScreen
from PlusObject import PlusDedication


plus=PlusDedication()
white=WhiteScreen()
# objectD=ObjectDediction()


class imges:
    def __init__(self,img="./lena.png"):
        self.MainImg=cv2.imread(img)
        self.ShowImg=np.zeros([720 , 300 , 3], dtype=np.uint8).fill(255)
        self.cutImg = {}



    def imgsettings(self):
        pass


    def ImageCrop(self,Image,dim,per=.1):
        Image=remove(Image)
        # print(dim[1]//80,dim[0]/80)
        self.Img= cv2.resize(Image, (int(dim[1]/per),int(dim[0]/per)), interpolation = cv2.INTER_AREA)

        cv2.imshow("croped img",self.Img)

    def ImageImplemintationPlace(self,img):
        # img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # img = cv2.resize(img, white.dim, interpolation=cv2.INTER_AREA)

        cv2.imshow("kkk",img)
        print("imshape",img.shape)
        w, h = white.dim
        img_width, img_height = img.shape[1], img.shape[0]
        print("h,w",h,w)
        print("img_width,img_height",img.shape[1], img.shape[0])
        xPluscenterPhone , yPluscenterPhone ,SpaceOldBox= plus.PlusDedictions()
        print("xPluscenterPhone , yPluscenterPhone",xPluscenterPhone , yPluscenterPhone)
        print("xPluscenterPhone > img_width//2",xPluscenterPhone > img_width//2)
        print("yPluscenterPhone > img_height//2",yPluscenterPhone > img_height//2)
        print(SpaceOldBox)
        ph=48

        xper=round(abs(xPluscenterPhone-img_width/2)/(SpaceOldBox[0] / ph))
        print("xper",xper)
        if xPluscenterPhone > img_width//2:
            x=abs(round(xper-w/2))

        else:
            x = abs(round(xper+w/2))


        yper=round(abs(yPluscenterPhone-img_height/2)/(SpaceOldBox[1] / ph))
        print("yper",yper)

        if yPluscenterPhone > img_height//2:
            y=abs(round(yper-h/2))

        else:

            y =abs(round(yper+h/2))

        return x,y
    def ImplemintingImg(self,axis, white ):
        imgImpl_width, imgImpl_height =self.Img.shape[1],self.Img.shape[0]
        print("axis",axis)
        print("white",white.shape)
        print(axis[1]-imgImpl_height , axis[1] + imgImpl_height,axis[0]-imgImpl_width , axis[0] + imgImpl_width )
        roi = white[axis[1]-imgImpl_height//2 : axis[1] + imgImpl_height//2 ,
                    axis[0]-imgImpl_width //2 : axis[0] + imgImpl_width //2 ]
        print("roi", roi.shape)
        print("img", self.Img.shape)
        if (roi.shape!=self.Img.shape) :
            print("error",)
            print("roi",roi.shape)
            print("img",self.Img.shape)
        else :
            #Now create a mask of logo and create its inverse mask also
            img2gray = cv2.cvtColor(self.Img, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            # Now black-out the area of logo in ROI
            img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
            # Take only region of logo from logo image.
            img2_fg = cv2.bitwise_and(self.Img, self.Img, mask=mask)
            # Put logo in ROI and modify the main image
            dst = cv2.add(img1_bg, img2_fg)
            white[axis[1] - imgImpl_height // 2: axis[1] + imgImpl_height // 2, axis[0] - imgImpl_width // 2: axis[0] + imgImpl_width // 2] = dst
            # cv2.imshow("camera", img)
        return white

    def pic(self):
        pass
    def CropedBox(self,img2,color=(0,0,0),per=45,val=50):
        y,x,_=img2.shape
        strx = int((x*(per/100))//2)
        stry =  int((y*.1)//2)

        img2 = cv2.line(img2,(strx,stry)  ,(strx+val,stry),color,2)
        img2 = cv2.line(img2,(x-strx,stry),(x-strx-val,stry),color,2)

        img2 = cv2.line(img2,(strx,stry),(strx,stry+val),color,2)
        img2 = cv2.line(img2,(x-strx,stry),(x-strx,stry+val),color,2)

        img2 = cv2.line(img2,(strx,y-stry),(strx,y-stry-val),color,2)
        img2 = cv2.line(img2,(strx,y-stry),(strx+val,y-stry),color,2)

        img2 = cv2.line(img2,(x-strx,y-stry),(x-strx-val,y-stry),color,2)
        img2 = cv2.line(img2,(x-strx,y-stry),(x-strx,y-stry-val),color,2)

        img2 = cv2.line(img2,(x//2-val//2,y//2),(x//2+val//2,y//2),color,2)
        img2 = cv2.line(img2,(x//2,y//2-val//2),(x//2,y//2+val//2),color,2)
        return img2 ,(strx,stry,x-strx,y-stry)
    def plusShape(self,img):
        pass
    def livePic(self,ipAdress='192.168.68.101:8080'):
        switch,place=False,False
        while True:
            #### img
            img_resp = requests.get("http://"+ipAdress+"/shot.jpg")
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            img = cv2.imdecode(img_arr, -1)
            img = imutils.resize(img, width=500, height=750)
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            img2=img.copy()
            # img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # print(white.white.shape)
            ######
            # img=cv2.imread("./plus2.jpg")
            # img2 =cv2.imread("./object.jpg")
            # dim=(500,700)
            # img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            # img2 = cv2.resize(img2, dim, interpolation=cv2.INTER_AREA)

            if switch :
                place=plus.plusCapture(img)
                if not place:
                    img2= cv2.putText(img2, "No plus dedicated", (10, 10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)

            img2, cor = self.CropedBox(img2)

            #
            # print("##########main#########")
            # print(img.shape)
            # print(img.shape)
            # print("###################")


            cv2.imshow("imgcordenats", img2)
            cv2.imshow("img", img)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                self.ImageCrop(img[cor[1]:cor[3],cor[0]:cor[2]],img.shape)
                switch = True

            if cv2.waitKey(1) & 0xFF == ord('p') and place:
                print("x,y",self.ImageImplemintationPlace(img))
                white.white=self.ImplemintingImg(self.ImageImplemintationPlace(img), white.white)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if cv2.waitKey(1) & 0xFF == ord('r') :
                white.clearScreen()
            if cv2.waitKey(1) & 0xFF == ord('w') :
                white.plusReGenerate(li=24,thi=8,colorLine=(255,0,0))
            cv2.imshow("whitescreen",white.white)
            cv2.imshow("imgcordenats",img2)
            cv2.imshow("img",img)
            cv2.waitKey(1000)






