# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 21:01:49 2021

@author: 42073
"""
import os, sys, win32gui, win32api
import numpy as np
import mouse
import time
import params_geometry

# from nwn_bot_data import Data 
class Geometry:
    def __init__(self, hwnd):
        self.hwnd        = hwnd 
        self.active      = False
        self.game_center = False
        self.rect_game   = False
        # self.rect_map    = False
        # self.rect_cam_v  = False
        # self.rect_cam_h  = False
        # self.rect_health = False
        # self.rectangles  = False
        # self.combat_rect = False
        while True:
            # print('waiting for game to be active from Geometry constructor')
            if self.is_game_active_by_hwnd():
                self.initiate_geometry()
                break
            # time.sleep(2)    
            
    def get_rectangles(self):
        self.rect_health           = self.get_rectangle(params_geometry.rect_health)
        self.rect_healt_party      = self.get_rectangle(params_geometry.rect_healt_party)
        self.rect_party_members    = self.get_rectangle(params_geometry.rect_party_members)
        self.rect_auto_heal_on_off = self.get_rectangle(params_geometry.rect_auto_heal_on_off)
        self.rect_stopwatch        = self.get_rectangle(params_geometry.rect_stopwatch)
        self.rect_boss_kills       = self.get_rectangle(params_geometry.rect_boss_kills)
        self.shadow_evade          = self.get_rectangle(params_geometry.rect_shadow_evade)  
        self.shadow_twin           = self.get_rectangle(params_geometry.rect_shadow_twin) 
        self.rect_dmg_counter_on_off = self.get_rectangle(params_geometry.rect_dmg_counter_on_off)
        
    def is_game_active_by_hwnd(self):
        if self.hwnd == win32gui.GetForegroundWindow():
            self.active = True
            return True
        self.active = False
        return False
    
    def initiate_geometry(self):
        self.get_game_rect()
        self.get_window_center()
        self.get_rectangles()
                    
    def update_geometry(self):   
        rect_game = self.get_game_rect()
        if rect_game != self.rect_game:            
           self.rect_game = rect_game
           x, y, w, h = rect_game
           self.game_center = w/2, h/2
           self.update_rectangles()
        return rect_game
                     
    def get_game_rect(self):
        # (left, top, right, bottom)
        windowrect = win32gui.GetWindowRect(self.hwnd)
        x      = windowrect[0]      +7
        y      = windowrect[1]     +31
        width  = windowrect[2]  -x  -7
        height = windowrect[3]  -y  -7
        self.rect_game = x, y, width, height
        return self.rect_game
   
# rect_stopwatch        = 0, 40, 100, 0, 2 # x, y, x2, y2, 
   
    # returns x, y, x2, y2       
    def get_rectangle(self, window):
        _, __, gw, gh = self.rect_game
        x, y, x2, y2, rel_to    = window
        if rel_to == 1:
            return x, y, x2, y2
        elif rel_to == 2:
            return x, gh - y, x2, gh  - y2                    
        elif rel_to == 3:
            return gw -x, gh - y, gw - x2, gh  - y2              
        elif rel_to == 4:
            return gw -x, y, gw - x2, y2             
        elif rel_to == 5:
            return int(gw/2 + x), int(gh/2 -y),  int(x2 -x) , int( -y2 + y) 
        
    # def get_rectangle2(self, window, rel_to = 1):
    #     _, __, gw, gh = self.rect_game
    #     x, y, x2, y2    = window
    #     if rel_to == 1:
    #         return x, y, x2 -x, y2-y
    #     elif rel_to == 2:
    #         return x, gh - y, x+x2, -y2 + y                        
    #     elif rel_to == 3:
    #         return gw -x, gh - y, - x2  + x, -y2 + y               
    #     elif rel_to == 4:
    #         return gw -x, y, gw- x2, y2              
    #     elif rel_to == 5:
    #         return int(gw/2 + x), int(gh/2 -y),  int(x2 -x) , int( -y2 + y)        

    def get_monitor_rect(self):
        w, h = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
        return 0,0, w, h
    
    def get_mouse_pos(self, rel_to = 1):
        x, y, w, h  = self.rect_game
        xm, ym      = self._get_mouse_pos()
        x, y        = xm - x, ym - y 
        if rel_to == 1:
            return x, y        
        elif rel_to == 2: 
            return x, h-y        
        elif rel_to == 3:
            return w -x, h-y        
        elif rel_to == 4: 
            return w -x, y
        elif rel_to == 5:
            return x -w/2, h/2 -y 
        else:pass
   
    def set_mouse_pos(self, xm, ym, rel_to = 1):
        xw, yw, w, h  = self.rect_game 
        if rel_to == 1:
            self._set_mouse_pos(xw + xm, yw + ym)        
        elif rel_to == 2: 
            self._set_mouse_pos(xw + xm, yw + h - ym)        
        elif rel_to == 3:
            self._set_mouse_pos(xw + w - xm, yw + h - ym)        
        elif rel_to == 4: 
            self._set_mouse_pos(xw + w - xm, yw + ym)
        elif rel_to == 5:
            self._set_mouse_pos(xw + w/2 + xm, yw + h/2 - ym ) 
        return           
        
    def get_window_center(self):
        xw, yw, w, h = self.rect_game
        self.game_center = w/2 + xw, h/2 + yw
        return w/2 + xw, h/2 + yw
    
    def get_distance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2        
        return np.sqrt(abs(x1 -x2)**2 + abs(y1 - y2)**2)

    def _get_mouse_pos(self):
        x, y = mouse.get_position()
        return x, y
    def _set_mouse_pos(self, x, y):
        mouse.move(x, y)
        
if __name__ == '__main__':
    import cv2 as cv
    import ctypes as c
    import multiprocessing as mp
    from lib_launcher import Nwn_launcher
    from lib_monitor_grabber import MonitorGrabber
    
    account1 = {'name':      "mk",           
               'pos':       [0, 0], 
               'size':      [1900,1150],  
               'logs_num':  5,
               'ip':        '188.244.50.172:5121',
               'key':       'AUEXY-FEVC9-DCAW3-HYM39-HFH9U-6ANCN-6VTCR', 
               'game_dir':   r'C:/Program Files (x86)/Steam/steamapps/common/Neverwinter Nights/bin/win32',
               'user_dir':   r'C:/Users/42073/Documents/Neverwinter Nights',
               }
#--------------------------------LAUNCHER--------------------------------------
    nwn_launcher = Nwn_launcher(account1)
    nwn_launcher.prepare_all()
    nwn_launcher.run_game()
    nwn_launcher.adjust_game()
    
#--------------------------------GEOMETRY--------------------------------------    
    geometry = Geometry(nwn_launcher.hwnd)
    
#--------------------------------GRABBER---------------------------------------    
    mg = MonitorGrabber(account1)
    # cv.imshow('', self.snapshot[x:x2, y:y2])
    time.sleep(10)
    mgg = mg.grab_game_window()
    mp_capture = mp.Array(c.c_ubyte, h*w*4)
    mp_states  = mp.Array(c.c_ubyte, 10)                                          # [0] run/stop, [1] frame number
    snapshot   = np.frombuffer(mp_capture.get_obj(),dtype=np.uint8).reshape((h,w,4))
    snapshot[:,:,:] = mgg
    # a = mg.grab_game_window2()
    x1, x2, y1, y2 = test(w, h, 40,5,5,80)
    xxx = snapshot[y1:y2, x1:x2]
    cv.imshow('', xxx)
    cv.waitKey(25)
    time.sleep(10)
    # cv.imshow('', a)


    

    
    
        
        
