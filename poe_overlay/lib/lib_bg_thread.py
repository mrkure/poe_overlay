import time
import ctypes as c
import numpy as np, time
import multiprocessing as mp
from multiprocessing import Process
import lib_monitor_grabber as lmg
# import cv2 as cv

from lib_healt_bar_evaluator import HealthBarEvaluator as hbe

# -----------------------------DEBUG-------------------------------------------
DB = 1
def debug(to_print):
    if DB == 1:
        print(to_print)
                
# ------------------------BACKGROUND PROCESS-----------------------------------   

def capture_screen(capture_ar, states_ar, window_geometry):

    window_geometry = window_geometry # x, y, w, h 
    health_geometry = [115, 950,   15,  180]
    hbevaluator     = hbe(health_geometry)

    capture_ar      = np.frombuffer(capture_ar.get_obj(),dtype=np.uint8).reshape((window_geometry[3], window_geometry[2], 4))
    states_ar       = np.frombuffer(states_ar.get_obj(),dtype=np.uint)  
    monitor_grabber = lmg.MonitorGrabber(window_geometry)
   
    while states_ar.item(0):
        capture_ar[:,:,:]               = monitor_grabber.grab_geometry(window_geometry)
        health_value, mask, controll_ar = hbevaluator.evaluate_health_bar(capture_ar)
        states_ar[5] = health_value
        # print(health_value)
          
            
if __name__ == '__main__':
    window_geometry = [0, 0, 1900, 1135]
    states_ar  = mp.Array(c.c_uint, 10)  
    capture_ar = mp.Array(c.c_ubyte, window_geometry[3] * window_geometry[2] * 4)
    states_ar[0] = 1
    capture_screen(capture_ar, states_ar, window_geometry)
    
    # print('health' , y)
#     states[5] = y 
        
    # cv.imshow('frame',snapshot)

    # # cv.moveWindow('',0,0)
    # cv.waitKey(40)
    # time.sleep(2)
    # cv.destroyAllWindows()              
            
            
            
            
            
            
            