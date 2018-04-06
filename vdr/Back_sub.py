import cv2
import cv2.cv as cv
import numpy as np
import config

class RemoveBackground:
    ''' background subtraction, Frame compare metho'''
    def __init__(self):
        self.__foreground__=None
        self.__back__=None
        
        self.mem=cv.CreateMemStorage()
        self.scratch=None
                    
    def getFrames(self,frame=None):
        if frame==None:
            print 'Error: Cant read from Camera'
        else:
            
            self.__foreground__=frame
            
    def loadBackground(self):
        self.__back__=cv2.imread("./train/back_g.jpg",cv2.cv.CV_LOAD_IMAGE_UNCHANGED)
        self.__back__=cv2.blur(self.__back__, (3,3))
            
    
    def subtract_back(self,frm):
        #dst=self.__back__-self.__foreground__
        temp=np.zeros((config.height,config.width),np.uint8)
        
        self.__foreground__=cv2.blur(self.__foreground__,(3,3))
        dst=cv2.absdiff(self.__back__,self.__foreground__)
        
        #dst=cv2.adaptiveThreshold(dst,255,cv.CV_THRESH_BINARY,cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C,5,10)
        val,dst=cv2.threshold(dst,0,255,cv.CV_THRESH_BINARY+cv.CV_THRESH_OTSU)
        
        fg=cv2.erode(dst,None,iterations=1)
        bg=cv2.dilate(dst,None,iterations=4)
        
        _,bg=cv2.threshold(bg,1,128,1)
        
        mark=cv2.add(fg,bg)
        mark32=np.int32(mark)
        #dst.copy(temp)
        
        #seq=cv.FindContours(cv.fromarray(dst),self.mem,cv.CV_RETR_EXTERNAL,cv.CV_CHAIN_APPROX_SIMPLE)
        #cntr,h=cv2.findContours(dst,cv.CV_RETR_EXTERNAL,cv.CV_CHAIN_APPROX_SIMPLE)
        #print cntr,h
        #cv.DrawContours(cv.fromarray(temp),seq,(255,255,255),(255,255,255),1,cv.CV_FILLED)
        cv2.watershed(frm, mark32)
        self.final_mask=cv2.convertScaleAbs(mark32)
        #print temp
        
        #--outputs---
        #cv2.imshow("subtraction",fg)
        #cv2.imshow("thres",dst)
        #cv2.imshow("thres1",bg)
        #cv2.imshow("mark",mark)
        #cv2.imshow("final",self.final_mask)
        
    def remove(self,frm):
        _,self.final_mask=cv2.threshold(self.final_mask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        res=cv2.bitwise_and(frm,frm,mask=self.final_mask)
        return res
        
        
