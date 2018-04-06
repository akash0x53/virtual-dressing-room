#!/usr/bin/env python
import os
import gtk
import gtk.gdk as gdk
import gobject
import cv2
import numpy as np
import time

from Video import Video
from Back_sub import RemoveBackground
from color_replace import Replace
from normalized import NormalizedRGB
from Tshirt import DetectShirt

from config import red
from config import green,blue
from config import yellow,pink,brown,plain,temp1,temp2,color,design

templates="templates/"
assets = os.path.join(".", "assets")
tests = os.path.join(".", "tests")
TEST_MODE = bool(int(os.environ.get('VDR_TEST', 0)))


class MainUI:
    
    def __init__(self):
        
        self.isBanner_mode=True
        self.final=None
        self.design=7
        self.color=None
        
        #Initialize systems objects
        if TEST_MODE:
            self.vid=cv2.VideoCapture(os.path.join(tests, "demo.avi"))
        self.v=Video()
	#----------------testing purpose--------------#
        
        self.back=RemoveBackground()
        self.norm=NormalizedRGB()
        
        self.replace=Replace()
        #print self.replace
        self.tshirt=DetectShirt()

        self.p_mat=np.array(np.mat([[0,0],[100,0],[100,100],[0,100]],np.float32))
        self.design_template=cv2.imread(templates+"Green.png")
        #-----------------------------------------------------
        
        self.__glade__=gtk.Builder()
        self.__ui__=self.__glade__.add_from_file(os.path.join(assets, "main_ui.glade"))
        
        self.__main_win__=self.__glade__.get_object("vdr_main")
        self.drawing_area=self.__glade__.get_object("da1")
        
        self.about=self.__glade__.get_object("abt")
        self.about.connect("clicked",self.show_abt)
        self.about_dia=self.__glade__.get_object("about_dia")
                        
        #init Drawing Area
        self.drawing_area.realize()
        self.drawing_area.set_size_request(config.width, config.height)
        #get canvas
        self.canvas=self.drawing_area.window
        
        #get GC
        self.gc=self.canvas.new_gc()
        #draw rectnagle
        #print self.canvas,self.gc
        
        self.gc.set_background(gdk.Color(0,0,0,0))
        self.gc.set_foreground(gdk.Color(255,0,0,0))
        
        #print dir(self.canvas)
        self.canvas.draw_rectangle(self.gc,False,10,10,100,200)
        self.canvas.draw_line(self.gc,10,10,100,100)
        
                        
        #decorate Mainwindows
        self.__main_win__.modify_bg(gtk.STATE_NORMAL,gtk.gdk.Color(0,0,0,0))
        self.__main_win__.modify_fg(gtk.STATE_NORMAL,gtk.gdk.Color(0,255,0,0))
        
        
        self.tview1=self.__glade__.get_object("tv1")
        self.lstore1=self.__glade__.get_object("ls1")
        self.tview2=self.__glade__.get_object("tv2")
        self.lstore2=self.__glade__.get_object("ls2")
        self.apply_btn=self.__glade__.get_object("apply")
        self.apply_btn.connect("clicked",self.change_avtar)
        
        self.lstore1.append([gtk.gdk.pixbuf_new_from_file(templates+'Red.png'),red])
        self.lstore1.append([gtk.gdk.pixbuf_new_from_file(templates+'Green.png'),green])
        self.lstore1.append([gtk.gdk.pixbuf_new_from_file(templates+'Blue.png'),blue])
        self.lstore1.append([gtk.gdk.pixbuf_new_from_file(templates+'Yellow.png'),yellow])
        self.lstore1.append([gtk.gdk.pixbuf_new_from_file(templates+'Pink.png'),pink])
        self.lstore1.append([gtk.gdk.pixbuf_new_from_file(templates+'Brown.png'),brown])
        
        self.lstore2.append([gtk.gdk.pixbuf_new_from_file(templates+'Blue.png'),plain])
        self.lstore2.append([gtk.gdk.pixbuf_new_from_file(templates+'Nike.png'),temp1])
        self.lstore2.append([gtk.gdk.pixbuf_new_from_file(templates+'Reebok.png'),temp2])
        
                
        #treeview = gtk.TreeView(self.lstore1)
        self.tview1.set_model(self.lstore1)
        self.tview2.set_model(self.lstore2)
        
        self.tview1.modify_base(gtk.STATE_NORMAL,gtk.gdk.Color(0,0,0,0))
        self.tview2.modify_base(gtk.STATE_NORMAL,gtk.gdk.Color(0,0,0,0))
        
       
        cell = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn("Pixbuf", cell)
        column.add_attribute(cell, "pixbuf", 0)
        self.tview1.append_column(column)
        cell.set_padding(30,50)
        
        cell2=gtk.CellRendererPixbuf()
        column2 = gtk.TreeViewColumn("Pixbuf", cell2)
        column2.add_attribute(cell2, "pixbuf", 0)
        self.tview2.append_column(column2)
        cell2.set_padding(30,50)
                
               
        #self.canvas.draw_
        self.drawing_area.set_app_paintable(True)
        self.drawing_area.connect("expose-event",self.display_frame)
        
        selection_color=self.tview1.get_selection()
        selection_color.connect("changed",self.change_cloth_plain)
        
        selection_design=self.tview2.get_selection()
        selection_design.connect("changed",self.change_cloth_design)
        
        self.canvas.set_background(gtk.gdk.Color(0,0,0,0))
        
        self.__main_win__.connect("delete-event",gtk.mainquit)
        self.img=cv2.cv.LoadImage(os.path.join(assets, "Banner.png"))
        #
        
        self.__main_win__.show()
        self.__main_win__.maximize()
        
    def show_abt(self,event):
        self.about_dia.run()
        self.about_dia.hide()
        
        
    def change_avtar(self,event):
        print 'ok'
        if self.isBanner_mode:
            self.img=cv2.cv.LoadImage(os.path.join(assets, "Banner_2.png"))
            
            self.timer_id=gtk.timeout_add(20*1000,self.reset)
            self.isBanner_mode=False
            self.drawing_area.queue_draw()
    
    def reset(self):
        self.img=cv2.cv.LoadImage(templates+"Banner.png")
        
        self.isBanner_mode=True
        self.drawing_area.queue_draw()
        gtk.timeout_remove(self.timer_id)
                       
                      
    def display_frame(self,a,b):
        self.drawing_area.window.draw_rectangle(self.drawing_area.get_style().white_gc,False,0,0,799,599)
        
        if self.isBanner_mode:
            self.canvas.draw_rgb_image(self.gc,1,1,798,598,gtk.gdk.RGB_DITHER_NORMAL,self.img.tostring(),2400)
            #self.final=self.getOutput_frames()
            #self.final=cv2.cvtColor(self.final,cv2.cv.CV_BGR2RGB)
            
        elif not self.isBanner_mode:
            
            if self.final==None:
                self.final=self.getOutput_frames()
                self.final=cv2.cvtColor(self.final,cv2.cv.CV_BGR2RGB)
                self.drawing_area.queue_draw()
                return 
            else:
                self.canvas.draw_rgb_image(self.gc,1,1,798,598,gtk.gdk.RGB_DITHER_NORMAL,self.final.tostring(),2400)
                self.final=self.getOutput_frames()
                self.final=cv2.cvtColor(self.final,cv2.cv.CV_BGR2RGB)
                self.drawing_area.queue_draw()
                
            #self.canvas.draw_rgb_image(self.gc,1,1,798,598,gtk.gdk.RGB_DITHER_NORMAL,self.final.tostring(),2400)
            
        
    def getOutput_frames(self):
        # using VideoCapture for test
        
        if TEST_MODE:
            _,frame=self.vid.read() #NOTE: Testing without camera. uncomment this to feed from camera.
        else:
            frame=self.v.outFrame() #NOTE: feeding from Camera.

        self.norm.getRGB(frame) #input to Normalized RGB
               
        norm_rgb=self.norm.normalized() #normalized RGB
        print 'Got normalized RGB '       
        rgb_planes=self.v.imagePlanes(norm_rgb)
                
#-------bg subtraction part-----------
#        load background samples
        self.back.loadBackground()
        self.back.getFrames(rgb_planes[1])
        self.back.subtract_back(norm_rgb)
        
        subtracted=self.back.remove(frame)
        print 'background subtracted now'
        
        self.tshirt.getFrames(norm_rgb)
        mask,cntr=self.tshirt.detect_shirt()
        print 'found tshirt'
        
        self.replace.getFrames(subtracted,mask)
        
        res=self.replace.replace_color(self.color)
        
        if self.design is not 7:
            res=self.replace.replace_design(cntr,self.p_mat, self.design_template, res)
        
        #replace.replace_design(cntr, p_mat,design_template,res)

        #cv2.imshow("subtracted", res)
        
        return res
        
        
    def change_cloth_plain(self,selected):
        global color
        model,iter=selected.get_selected()
        color=model.get_value(iter,1)
        self.color=color
     
        
    def change_cloth_design(self,selected):
        global design
        model,iter=selected.get_selected()
        self.design=model.get_value(iter,1)
        
        if self.design==8:
            self.design_template=cv2.imread(templates+"nike.png",cv2.cv.CV_LOAD_IMAGE_UNCHANGED)
        if self.design==9:
            self.design_template=cv2.imread(templates+"Rbk.png",cv2.cv.CV_LOAD_IMAGE_UNCHANGED)
            
        
        
def sample_bg(frame):
    '''This function sample some background images for bakground subtraction.'''
    if frame==None:
            print 'Training skipped...NOTE: VDR will use already sampled background.'
    else:
        cv2.imwrite("./train/back_g.jpg",frame)        

def Main():
    
    train=False
    print 'training started'
    
    if train:
        v=Video()
        n=NormalizedRGB()
        for i in range(100):
            frm=v.outFrame()
            n.getRGB(frm)
            norm=n.normalized()
            plain=v.imagePlanes(norm)
        
            sample_bg(plain[1])
        print 'training ends...'
        del v
    
    
    m=MainUI()
    gtk.main()

if __name__=="__main__":
    Main()
