import cv2
import cv2.cv as cv
import numpy as np

import config

class DetectShirt:
    
    def __init__(self):
        self.norm_rgb=np.zeros((config.height,config.width,3),np.uint8)
        self.dst=np.zeros((config.height,config.width),np.uint8)
        self.b=0
        self.g=0
        self.r=0
        
        self.lb=0
        self.lg=0
        self.lr=0
        
        self.m=np.zeros((config.height,config.width),np.uint8)
        #self.win=cv2.namedWindow("detect")
        #self.dst=cv.CreateImage((config.width,config.height),8,1)
        
        #cv2.createTrackbar("blue", "detect",0,255,self.change_b)
        #cv2.createTrackbar("green","detect",0,255,self.change_g)
        #cv2.createTrackbar("red","detect",0,255,self.change_r)
        
        #cv2.createTrackbar("low_blue", "detect",0,255,self.change_lb)
        #cv2.createTrackbar("low_green","detect",0,255,self.change_lg)
        #cv2.createTrackbar("low_red","detect",0,255,self.change_lr)
        
    def getFrames(self,frame):
        self.norm_rgb[:,:,:]=frame[:,:,:]
        
    def change_b(self,val):
        self.b=val
    def change_g(self,val):
        self.g=val
    def change_r(self,val):
        self.r=val
        
    def change_lb(self,val):
        self.lb=val
    def change_lg(self,val):
        self.lg=val
    def change_lr(self,val):
        self.lr=val
    
    def detect_shirt(self):
        
        
        #self.dst=cv2.inRange(self.norm_rgb,np.array([self.lb,self.lg,self.lr],np.uint8),np.array([self.b,self.g,self.r],np.uint8))
        self.dst=cv2.inRange(self.norm_rgb,np.array([20,20,20],np.uint8),np.array([255,110,80],np.uint8))
        cv2.threshold(self.dst,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)
        fg=cv2.erode(self.dst,None,iterations=2)
        #cv2.imshow("fore",fg)  
        bg=cv2.dilate(self.dst,None,iterations=3)
        _,bg=cv2.threshold(bg, 1,128,1)
        #cv2.imshow("back",bg)
        
        mark=cv2.add(fg,bg)
        mark32=np.int32(mark)
        cv2.watershed(self.norm_rgb,mark32)
        self.m=cv2.convertScaleAbs(mark32)
        _,self.m=cv2.threshold(self.m,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        #cv2.imshow("final_tshirt",self.m)
        
        cntr,h=cv2.findContours(self.m,cv2.cv.CV_RETR_EXTERNAL,cv2.cv.CV_CHAIN_APPROX_SIMPLE)
               
        return self.m,cntr
        
    def detect_shirt2(self):
        self.hsv=cv2.cvtColor(self.norm_rgb,cv.CV_BGR2HSV)
        self.hue,s,_=cv2.split(self.hsv)
        
        _,self.dst=cv2.threshold(self.hue,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        self.fg=cv2.erode(self.dst,None,iterations=3)
        self.bg=cv2.dilate(self.dst,None,iterations=1)
        _,self.bg=cv2.threshold(self.bg,1,128,1)
        mark=cv2.add(self.fg,self.bg)
        mark32=np.int32(mark)
        cv2.watershed(self.norm_rgb,mark32)
        
        m=cv2.convertScaleAbs(mark32)
        _,m=cv2.threshold(m,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        cntr,h=cv2.findContours(m,cv.CV_RETR_EXTERNAL,cv.CV_CHAIN_APPROX_SIMPLE)
        print len(cntr)
        #print cntr[0].shape
        #cntr[1].dtype=np.float32
        #ret=cv2.contourArea(np.array(cntr[1]))
        #print ret
        #cntr[0].dtype=np.uint8
        cv2.drawContours(m,cntr,-1,(255,255,255),3)
        cv2.imshow("mask_fg",self.fg)
        cv2.imshow("mask_bg",self.bg)
        cv2.imshow("mark",m)
        
        
        
