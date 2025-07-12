# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 13:53:37 2022

@author: 42073
"""
import time
import keyboard
def on_key_down(key):
    print(key.name)

keyboard.on_press(on_key_down)

while True:
    time.sleep(1)  
    
    