# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 16:42:20 2022

@author: 42073
"""
import time
# import params as par
import lib_launcher as lla
import multiprocessing as mp
import ctypes as c
import numpy as np
import lib_driver as ldr
import lib_bg_thread as bgt
from multiprocessing import Process
import cv2 as cv
params = lla.account1

if __name__ == '__main__':
#-----------------------------LAUNCH GAME--------------------------------------
    # nwn_launcher = lla.Nwn_launcher(params)
    # nwn_launcher.prepare_all()
    # nwn_launcher.run_game()
    # nwn_launcher.adjust_game()    
    # c.c_ubyte, dtype=np.uint8
#-----------------------------MULTIPROC DATA-----------------------------------
    mp_capture = mp.Array(c.c_ubyte, params['size'][1] *params['size'][0]*4)                                         # [0] run/stop, [1] frame number
    snapshot   = np.frombuffer(mp_capture.get_obj(),dtype=np.uint8).reshape((params['size'][1] ,params['size'][0],4))
    mp_states  = mp.Array(c.c_uint, 10)   
    states     = np.frombuffer(mp_states.get_obj(),dtype=np.uint)   
    
    p = Process(target=bgt.capture_screen, args=(mp_capture, mp_states, params))
    p.start()
#----------------------------------DRIVER--------------------------------------    
    driver     = ldr.Driver(states)
# # =============================================================================
# # MAIN
# # =============================================================================


    driver.start_bg_thread()
    while True:
        aa =snapshot[0:800, 1800:,:]

            
            
            
    # driver.start_bg_thread()
    # start = time.time()
    # while True:
    #     # driver.wait_for_new_frame()
    #     # do some stuff with snapshot
    #     # aa =snapshot[0:800, 1800:,:]
    #     # aa = snapshot
    #     # cv.moveWindow('', -1925,-65)
    #     # cv.imshow('', aa)
    #     # cv.waitKey(12)
    #     # print(driver.frame_current)        
    #     # driver.update_frame()

    #     if states[1] > 5000:
    #         driver.stop_bg_thread()
    #         break
    # end  = time.time()
    # print(states[1]/(end - start))    
    # input('end')            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            