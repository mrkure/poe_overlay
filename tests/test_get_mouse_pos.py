# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 21:01:49 2021

@author: 42073
"""
import os, sys, win32gui, win32api
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__))))
import numpy as np
import mouse
import time
import params_geometry as Data

# from nwn_bot_data import Data 
class Geometry:
    def __init__(self, hwnd):
        self.hwnd        = hwnd 
        self.active      = False
        self.game_center = False
        self.rect_game   = False
        self.rect_map    = False
        self.rect_cam_v  = False
        self.rect_cam_h  = False
        self.rect_health = False
        self.rectangles  = False
        self.combat_rect = False
        # if self.is_game_active():
        #     self.update_geometry()
            
    def is_game_active_by_hwnd(self):
        if self.hwnd == win32gui.GetForegroundWindow():
            self.set_active(True)
            return True
        self.set_active(False)
        return False

    def set_active(self, value):
        self.active == value
        
    def update_geometry(self):   
        if self.is_game_active_by_hwnd():
            rect_game = self.get_game_rect()
            if rect_game != self.rect_game:            
               self.rect_game = rect_game
               x, y, w, h = rect_game
               self.game_center = w/2, h/2
               self.update_rectangles()
            return rect_game
        else:
            pass
                     
    def get_game_rect(self):
        windowrect = win32gui.GetWindowRect(self.hwnd)
        x      = windowrect[0]      +7
        y      = windowrect[1]     +31
        width  = windowrect[2]  -x  -7
        height = windowrect[3]  -y  -7
        return x, y, width, height
    
    def get_game_rect_of_active_window(self):
        name = win32gui.GetWindowText (win32gui.GetForegroundWindow())
        hwnd = win32gui. FindWindow (None, name) 
        windowrect = win32gui.GetWindowRect(hwnd)
        x      = windowrect[0]      +7
        y      = windowrect[1]     +31
        width  = windowrect[2]  -x  -7
        height = windowrect[3]  -y  -7
        return x, y, width, height
   
    def update_rectangles(self):
        self.rect_map   = self.get_rectangle(Data.CURRENT_MAP_RECT,1)
        self.rect_cam_v = self.get_rectangle(Data.COMPAS_RECT_V,3)
        self.rect_cam_h = self.get_rectangle(Data.COMPAS_RECT_H,3)
        self.rect_health = self.get_rectangle(Data.HEALTH_RECT,4)
        self.combat_rect = self.get_rectangle(Data.COMBAT_RECT,1)
        self.inventory_rect = self.get_rectangle(Data.INVENTORY_RECT,1)
        self.rectangles = [self.rect_map, self.rect_cam_v, self.rect_cam_h, self.rect_health, self.combat_rect]
    
    def get_rectangle(self, window, rel_to = 1):
        _, __, gw, gh = self.rect_game
        x, y, x2, y2    = window
        if rel_to == 1:
            return x, y, x2 -x, y2-y
        elif rel_to == 2:
            return x, gh - y, x+x2, -y2 + y                        
        elif rel_to == 3:
            return gw -x, gh - y, - x2  + x, -y2 + y               
        elif rel_to == 4:
            return gw -x, y, - x2  + x,  y+y2              
        elif rel_to == 5:
            return int(gw/2 + x), int(gh/2 -y),  int(x2 -x) , int( -y2 + y) 

    def get_monitor_rect(self):
        w, h = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
        return 0,0, w, h

    def get_rect(self, x, y, w = 300, h = 300):
        return x, y, w, h
    
    def get_mouse_pos(self, window =  None, rel_to = 1):
        if window == None:
            x, y, w, h  = self.rect_game            
        else:
            x, y, w, h  = window   
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

    geometry = Geometry('fake')
    time.sleep(2)
    window = geometry.get_game_rect_of_active_window()
    print(window)
    while True:
        a = geometry.get_mouse_pos(window, 1)
        b = geometry.get_mouse_pos(window,2)
        c = geometry.get_mouse_pos(window,3)
        d = geometry.get_mouse_pos(window,4)
        e = geometry.get_mouse_pos(window,5)
        to_print = 'window = {},{},{},{}   rel1 = {:<5} {:<5}   rel2 = {:<5} {:<5}  rel3 = {:<5} {:<5}  rel4 = {:<5} {:<5}  rel5 = {:<5} {:<5}'.format(
            window[0], window[1], window[2], window[3],
                         a[0], a[1], b[0], b[1], c[0], c[1], d[0], d[1], e[0], e[1] )
        
        print(to_print)
        time.sleep(1)    



    





















    
    
        
        
