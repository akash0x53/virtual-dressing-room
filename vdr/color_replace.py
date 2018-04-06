import cv2
import cv2.cv as cv
import numpy as np
import config
from config import color


class Replace:
    
    def __init__(self):
        global color
        self.rgb=np.zeros((config.height,config.width,3),np.uint8)
        self.mask=np.zeros((config.height,config.width),np.uint8)
        self.hue_val=color
        self.scratch=np.zeros((config.height,config.width,3),np.uint8)
        
        #cv2.namedWindow("hue")
        #cv2.createTrackbar("hue", "hue",self.hue_val,255,self.change)
    
    def change(self,val):
        self.hue_val=val
    
    def getFrames(self,img,mask=None):
        self.rgb=img
        self.mask=mask
        self.scratch=np.zeros((config.height,config.width,3),np.uint8)
        
        self.scratch=cv2.cvtColor(img,cv2.cv.CV_BGR2HSV)
        self.hue,self.sat,self.val=cv2.split(self.scratch)
        print 'hsv conversion completed'
    
    def replace_color(self,col=None):
        print self.hue[0][0]
        self.hue_val=col
        #cv2.imshow("hue",self.hue)
        if col!=None:
            cv.Set(cv.fromarray(self.hue),(self.hue_val),cv.fromarray(self.mask))
            
        self.scratch=cv2.merge([self.hue,self.sat,self.val])
        self.scratch=cv2.cvtColor(self.scratch,cv2.cv.CV_HSV2BGR)
        print 'replaced'
        return self.scratch
    
    def replace_design(self,cntr,p_mat,design_template,input_image):
        area=list()
                
        for i in range(len(cntr)):
            
            area.append(cv2.contourArea(cntr[i].astype('int')))
        
        max_area=max(area)
        
        for i in range(len(area)):
            if max_area==area[i]:
                index=i
        mom=cv2.moments(cntr[index].astype('int'))
        #print mom
        x=mom['m10']
        y=mom['m01']
        cx=int(x/max_area)
        cy=int(y/max_area)
        #print 'center-X',cx
        #print 'center-Y',cy
                        
        rect=cv2.boundingRect(np.array(cntr[index],np.float32))
        
        x=rect[0]
        y=rect[1]
        w=rect[2]
        h=rect[3]
        
        q=np.array([
                    [x+w/3,(y+h)/3],
                    [x+w/2,(y+h)/3],
                    [x+w/2,y+h/3],
                    [x+w/3,y+h/3]
                ],np.float32)
        
        
        mat=cv2.getPerspectiveTransform(p_mat,q)
        
        dst=cv2.warpPerspective(design_template,mat,(config.width,config.height))
        
        
        temp=cv2.cvtColor(input_image,cv2.cv.CV_BGR2BGRA)
        temp=cv2.addWeighted(temp,1.0,dst,1.0,1.0)       
        res=cv2.cvtColor(temp,cv2.cv.CV_BGRA2BGR)
        
        return res 
        
        
        
        
        
    
            


        
