import cv2
import config


class IVideo:
    pass

"""
  VideoInput
  /    \
 /      \
Camera VideoFile 
"""

class Video:
    def __init__(self):
        self.__cap__=cv2.VideoCapture()
        self.__cap__.open(0)
        self.__cap__.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,config.height)
        self.__cap__.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,config.width)
        self.__frame__=None
        
    def getCapture(self):
        return self.__cap__
    
    def outFrame(self):
        res,self.__frame__=self.__cap__.read()
        self.__frame__=cv2.flip(self.__frame__, 1)
        
        if res:
            return self.__frame__
        else:
            print 'Error: Cant read from Camera'
            
    def imagePlanes(self,frame=None):
        if frame==None:
            frame=self.__frame__
            
        planes=cv2.split(frame)
        return planes

    def __del__(self):
        self.__cap__.release()
        print 'released camera'
                
