# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 21:09:13 2021

@author: 42073
"""
import numpy as np
import os, sys, time
import mss, mss.tools
import cv2 as cv
import mss.windows


class MonitorGrabber():
    def __init__(self, geometry):
        self.geometry        = geometry
        self.sct           = mss.mss()
        self.image_or      = None
        self.image_sh      = None
        self.image_general = None
        mss.windows.CAPTUREBLT = 0
       
    def update_grab(self):
        self.grab_game_window()
        self.shrink_game_window()
        
    def grab_game_window(self):
        x, y, w, h = self.geometry.rect_game
        monitor = {"top": y, "left":x, "width": w, "height": h }
        haystack = self.sct.grab(monitor)
        self.haystack = haystack
        self.image_or = np.asarray(haystack)
        aim = self.image_or
        return self.image_or
    
    def grab_geometry(self,window):
        x, y, w, h = window
        monitor = {"top": y, "left":x, "width": w, "height": h }
        haystack = self.sct.grab(monitor)
        self.image_general = np.asarray(haystack)
        return self.image_general  
           
    def shrink_game_window(self):
        image_sh     = np.array(self.image_or[:,::6,2], dtype='int32')
        image_sh[image_sh== 0] = 1
        image_sh_res = image_sh[:, :-1] * image_sh[:,1:]
        image_sh_res = image_sh_res[:, :-1] * image_sh[:,2:]
        image_sh_res = image_sh_res[:, :-1] * image_sh[:,3:]
        image_sh_res = image_sh_res[:, :-1] / image_sh[:,4:]
        image_sh_res = image_sh_res[:, :-1] * image_sh[:,5:]
        self.image_sh = image_sh_res
        return self.image_sh    
  
    def shrink_game_windowg(self):
        image_sh     = np.array(self.image_general[:,::6,2], dtype='int32')
        image_sh[image_sh== 0] = 1
        image_sh_res = image_sh[:, :-1] * image_sh[:,1:]
        image_sh_res = image_sh_res[:, :-1] * image_sh[:,2:]
        image_sh_res = image_sh_res[:, :-1] * image_sh[:,3:]
        image_sh_res = image_sh_res[:, :-1] / image_sh[:,4:]
        image_sh_res = image_sh_res[:, :-1] * image_sh[:,5:]
        self.image_sh = image_sh_res
        return self.image_sh          

# def filter_hsv(hsv_array, h_low, h_top, s, v, channel = 0):

#     shape = np.shape(hsv_array)
#     res_array = np.zeros(shape)

#     res_array[channel] [ hsv_array[0] <= h_low  ] += 80
#     res_array[channel] [ hsv_array[0] >= h_top  ] += 80

#     res_array[channel] [ hsv_array[1] >= s  ] += 80
#     res_array[channel] [ hsv_array[2] >= v  ] += 80   
#     res_array[channel] [ res_array[channel] < 240 ]  = 0
#     return res_array



# if __name__ == '__main__':
#     import win32gui  
#     import ctypes as c
#     # from PIL import Image
#     import multiprocessing as mp
#     # from matplotlib import pyplot as plt 
    
#     from lib_calc import Calc     
#     import lib_geometry as lge

#     grabber         = MonitorGrabber(5)
#     x, y, w, h      = 105,950,15,180
#     start = time.time()
#     for i in range(100):
#         # declare vars needed for multiprocessing 
#         mp_capture      = mp.Array(c.c_ubyte, h*w* 4)
#         mp_states       = mp.Array(c.c_ubyte, 10)  
#         capture         = np.frombuffer(mp_capture.get_obj(),dtype=np.uint8).reshape((h, w, 4))
#     # ----------------------------------GRAB---------------------------------------
#         grab            = grabber.grab_geometry([x, y, w, h])
#         capture[:,:,:]  = grab 
#         b = capture[:,:, 0 ]
#         g = capture[:,:, 1 ]
#         r = capture[:,:, 2 ]
#         o = capture[:,:, 3 ]    
        
        
#         # capture[:,:,0] = 0 
#         # capture[:,:,1] = 0     
#         # r [ r < 70] = 0  
#         # r [ r >= 70] = 255    
#         # capture[:,:,2] = 0
#     # --------------------------------GET CHUNK OF GRAB----------------------------
#         # rect_party_members    =  42,  186,  22, 800, 4
#         # rect_health           =  75,    3,  74, 103, 4
#         # x1, y1, x2, y2 = geometry.get_rectangle( rect_party_members) 
#         # chunk  = capture[ y1:y2, x1:x2]
#         # get_party_member(chunk, 0)
#     # ----------------------------------PLOT CAPTURE-------------------------------  
#         # plt.imshow(capture, interpolation='nearest')
#         # plt.show()
        
#         # img = Image.fromarray( np.array([r,b,g,o]))
#         # img.show()
        
#         # cv.imshow('',capture)
#         # cv.moveWindow('',-1900,0)
#         # cv.waitKey(40)
#         # time.sleep(5)
#         # cv.destroyAllWindows()
          
#     # ----------------------------------PLOT CHUNK---------------------------------     
#         # plt.imshow(chunk, interpolation='nearest')
#         # plt.show()
        
#         # img = Image.fromarray(chunk)
#         # img.show()
#         hsv = img = cv.cvtColor(capture, cv.COLOR_BGR2HSV)
#         # B, G, R
#         # define range of blue color in HSV

#         # lower mask (0-10)
#         lower_red = np.array([0,50,50])
#         upper_red = np.array([0,255,255])
#         mask0 = cv.inRange(hsv, lower_red, upper_red)
        
#         # upper mask (170-180)
#         lower_red = np.array([160,150,0])
#         upper_red = np.array([180,255,255])
#         mask1 = cv.inRange(hsv, lower_red, upper_red)
        
#         # join my masks
#         mask = mask0+mask1        
#         # lower_blue = np.array([110,50,50])
#         # upper_blue = np.array([130,255,255])
#         # # Threshold the HSV image to get only blue colors
#         # mask = cv.inRange(hsv, lower_blue, upper_blue)
#         # Bitwise-AND mask and original image
#         res = cv.bitwise_and(capture,capture, mask= mask)
#         aa = np.median(mask, axis=1)
        
#         cv.imshow('frame',capture)
#         cv.moveWindow('frame',-400,0)
#         cv.imshow('mask',mask)
#         cv.moveWindow('mask',-400,400)
#         cv.imshow('res',res)
#         cv.moveWindow('res',-400,800)
#         cv.imshow('aa',aa)
#         cv.moveWindow('aa',-800,800)
#         # cv.moveWindow('',0,0)
#         cv.waitKey(40)
#         time.sleep(2)
#         cv.destroyAllWindows()
#     # end  = time.time()
#     # print(1000/(end - start))
 



