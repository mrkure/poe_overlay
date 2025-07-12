# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 16:55:41 2022

@author: 42073
"""
import time

class Driver: 
    def __init__(self, states):   
        self.frame_current, self.frame_last = 0, 0
        self.states = states  
    def wait_for_new_frame(self, time_ = 1):
        while True:
            self.frame_current = self.states[1]
            time.sleep(0.5)
            print(self.states, ' ', self.frame_current, ' ', self.states[1])
            if self.frame_current > self.frame_last:
                return
            # debug('waiting for new frame')
            # time.sleep(time_)           
    def update_frame(self):
        # debug(self.states)
        if self.frame_current == 255:
            self.frame_last = 0
        else:
            self.frame_last = self.frame_current
    def start_bg_thread(self):
        self.states[0] = 1
        # debug(self.states)
    def stop_bg_thread(self):
        # debug(self.states)
        self.states[0] = 0   