import cv2
import config
import numpy as np

class NormalizedRGB:
    
    def __init__(self):
        self.rgb=np.zeros((config.height,config.width,3),np.uint8)
        
        #self.norm1=np.zeros((300,400),np.float32)
        #self.norm2=np.zeros((300,400),np.float32)
        #self.norm3=np.zeros((300,400),np.float32)
        
        self.norm=np.zeros((config.height,config.width,3),np.float32)
        self.norm_rgb=np.zeros((config.height,config.width,3),np.uint8)
        
        self.down=np.zeros((config.height,config.width,3),np.float32)
        
    
    def getRGB(self,rgb):
        self.rgb=rgb
        #self.down=cv2.pyrDown(rgb)
        self.down[:,:,:]=self.rgb[:,:,:]
        
        #print  self.down.shape 
        #self.down.shape=(150,200)
        
    def normalized(self):
               
#        t1=time.time()
        b=self.down[:,:,0]
        g=self.down[:,:,1]
        r=self.down[:,:,2]
        
        sum=b+g+r
        
        
        self.norm[:,:,0]=b/sum*255.0
        self.norm[:,:,1]=g/sum*255.0
        self.norm[:,:,2]=r/sum*255.0
        
 #       print "conversion time",time.time()-t1
        
        #self.norm=cv2.merge([self.norm1,self.norm2,self.norm3])
        self.norm_rgb=cv2.convertScaleAbs(self.norm)
        #self.norm.dtype=np.uint8
        return self.norm_rgb
