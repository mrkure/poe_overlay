# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 17:35:49 2021

@author: 42073
"""
import os, sys, win32gui, win32ui, keyboard
from PIL import Image
import numpy as np, pandas as pd
# import cv2 as cv
# import matplotlib.pyplot as plt



hotkeys = {
         '1':[False, 'travel'],
         '2':[False, 'click'],
         '3':[False, 'bash'],
         '4':[False, 'wait'],
         '7':[False, 'reset camera'],
         '5':[False, 'zoom toggle'], 
         '6':[False, 'v angle toggle'],
         '8':[False, 'attack distance down'],
         '9':[False, 'attack distance up'],          
         '0':[False, 'pause'],
         '=':[False, 'break'],                                                                                                         
         }
    
def if_key_pressed(hotkeys, drr):
    actions, cd, ca = drr.actions, drr.cd, drr.ca
    for key, value in hotkeys.items():
        if keyboard.is_pressed(key) and hotkeys[key][0] == False: 
            hotkeys[key][0] = True
            if any([key == i for i in ['1', '2', '3', '4']]):
                
                data = [hotkeys[key][1],
                        cd.map_pos_x,       
                        cd.map_pos_y,  
                        cd.map_angle,    
                        cd.camera_hor_angle, 
                        cd.camera_ver_angle, 
                        cd.camera_zoom,       
                        cd.mouse_pos_x,     
                        cd.mouse_pos_y, 
                        ca.attack_distance,
                        True,
                        True,
                        0]    
                columns          = ['action', 'map x', 'map y', 'map angle', 
                                    'cam h angle', 'cam v angle', 'cam zoom', 
                                    'mouse x', 'mouse y', 'attack distance', 'set cam in', 'set cam out', 'wait']
                actions.append(pd.DataFrame([data], columns = columns))
          
            print(hotkeys[key][1]) 
            return hotkeys[key][1]
        if not keyboard.is_pressed(key):
            hotkeys[key][0] = False1  
    return ''   


while True:
    if keyboard.on_release('1'):
        print(1)










