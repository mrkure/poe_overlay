# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 11:08:08 2022

@author: 42073
"""
import pyperclip
pyperclip.copy('The text to be copied to the clipboard.')
spam = pyperclip.paste()
import pandas as pd
import time
import keyboard
# def on_key_down(key):
#     print(key.name)

# keyboard.on_press(on_key_down)

# while True:
#     time.sleep(1)  
    
d = {'col1': [1, 2, 3,4,4,6], 'col2': [10, 20, 30,40,50,60]}
df = pd.DataFrame(d)
string = df.to_string()
time.sleep(2)
lines = string.split('\n')
for line in lines:
    pyperclip.copy(line)
    keyboard.press_and_release('enter')
    time.sleep(0.2)
    keyboard.press_and_release('ctrl+v')  
    time.sleep(0.2)
    
    
    
