# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 13:32:29 2022

@author: mrkure
"""
import os, mouse, keyboard, time, json
from mklib.lib_io import mkIO


class Recorder:
    def __init__(self):
        self.hooks = []
        self.rec_hooked = False
        self.last_key   = ''
        self.last_time  = 0
        self.sequences = {}
        self.recording = False
        self.khook, self.mhook, self.mhook2, self.hooked = None, None, None, False
        self.dic_mouse_up_down = {-1:'down', 1:'up'}
        self.mousex, self.mousey = 0,0
        self.interrupt = False
        self.dic = {'mouse_press':   self.mousePress,
                    'mouse_release': self.mouseRelease, 
                    'mouse_move':    self.mouseMove,
                    'key_press':     self.keyPress,
                    'key_release':   self.keyRelease,
                    'sleep':         self.sleep,
                    'mouse_double_click': self.mouseDoubleClick}
        
        keyboard.add_hotkey('f1', self.set_interrupt, args=())  
        
    def set_interrupt(self):
        self.interrupt = True
        
    def mousePress(self, *args):
        mouse.press(args[0][0])
        # mouse.press(args[0][0])
    def mouseRelease(self, *args):
        mouse.release(args[0][0])
        # mouse.release(args[0][0])
    def mouseMove(self, *args):
        mouse.move(args[0][0], args[0][1])

    def mouseDoubleClick(self, *args):
        pass
        # mouse.move(args[0][0], args[0][1])
        
    def keyPress(self, *args):
        keyboard.press(args[0][0])

    def keyRelease(self, *args):
        keyboard.release(args[0][0])
    
    def sleep(self, *args):
        time.sleep(args[0][0])        
        
    def start_recording(self, name):
        print('start recording')
        self.recording  = True
        if not self.hooked:
            self.name      = name
            self.hooked    = True
            self.sequence  = []
            self.khook     = keyboard.hook(self.on_keyboard_used, suppress=False)
            self.mhook     = mouse.hook(self.on_mouse_used) 
            self.last_time = time.time()

    def stop_recording(self):
        print('stop recording')
        if self.hooked:
            keyboard.unhook(self.khook)
            mouse.unhook(self.mhook)    
            self.hooked = False
            x = 0
            for num, i in enumerate(reversed(self.sequence)):
                if i[0] == 'mouse_release':
                    if i[1][0] == 'left':
                        x += 1
                elif i[0] == 'key_release':
                        x += 1                        
                if x == 2:
                    break
            self.sequence = self.sequence[0:num*-1]
            self.sequence.append(  ['mouse_move', [960, 600]]  )
            self.sequences[self.name] = self.sequence
        self.recording = False
     
    def run_recording(self, name, delay = 0.05):  
        print('play recording')
        for val in self.sequences[name]:
            print(self.interrupt)
            if self.interrupt: 
                self.interrupt = False
                return
            self.dic[val[0]](val[1])   
                
    def load_recordings(self, file):
        try:
            with open(file, "r") as fp:         
                self.sequences = json.load(fp)
        except:pass
        
    def save_recordings(self, file):
        with open(file, "w") as fp:
            json.dump(self.sequences, fp, indent=4)

    def get_recordings_names(self):        
        return [key for key, value in self.sequences.items()]
                                           
#%% EVENTS HANDLING
    def on_keyboard_used(self, event):
        if event.name+event.event_type == self.last_key and 0:
            return
        else:
            dic = {'down':'key_press', 'up':'key_release'}
            self.sequence.append(['sleep', [event.time - self.last_time, 0]]) 
            self.sequence.append([dic[event.event_type], [event.name.lower(), event.name.lower()]])
            self.last_key  = event.name+event.event_type
            self.last_time = event.time
            # print(event.name, event.event_type)

    def on_mouse_used(self, event):
        # print(event)
        dic = {'down':'mouse_press', 'up':'mouse_release', 'double':'mouse_double_click'}
        if type(event) == mouse.ButtonEvent:
            
            self.dic_mouse_up_down
            self.sequence.append(['sleep', [event.time - self.last_time, 0]])
            self.sequence.append([dic[event.event_type], [event.button, event.button]])
            self.last_time = time.time()
            # print(event.time)
            # print(event.event_type)
            # print(event.button)fdsadfaasdfdsa
            
        elif type(event) == mouse.MoveEvent:
            self.sequence.append(['sleep', [event.time - self.last_time,0]])
            self.sequence.append(['mouse_move', [event.x, event.y]])
            self.last_time = time.time()

            
        # elif type(event) == mouse.WheelEvent:
        #     print(dic[event.delta])        
        #     print(event.time)       
                   
    # def on_right_click(self):
    #     x, y = mouse.get_position() 
    #     self.sequence.append(['sleep', [time.time() - self.last_time,0]])
    #     self.sequence.append(['mouse_move', [x, y]])
    #     self.sequence.append(['sleep', [0.25,0]])
    #     self.sequence.append(['right_click', [None, None]])
    #     self.sequence.append(['sleep', [0.25,0]])

    #     self.last_time = time.time()
    #     print('right click')  
        
    # def on_left_click(self):
    #     x, y = mouse.get_position()
    #     self.sequence.append(['sleep', [time.time() - self.last_time,0]])
    #     self.sequence.append(['mouse_move', [x, y]])
    #     self.sequence.append(['sleep', [0.25,0]])
    #     self.sequence.append(['left_click', [None, None]])
    #     self.sequence.append(['sleep', [0.25,0]])
    #     self.last_time = time.time()
    #     print('left click')
                
#%% HOOK UNHOOK
    def hook_all(self):
        # if not self.rec_hooked:
        #     self.hooks.append(keyboard.add_hotkey('f1', self.play_sequence, args=()) )   
        # self.rec_hooked = True
       pass
    def unhook_all(self):
        if self.rec_hooked:
            for hook in self.hooks:
                keyboard.remove_hotkey(hook)
            self.hooks = []
        self.rec_hooked = False
        
#%% TEST                   
if __name__ == '__main__':
    file = r'C:/_repositories/resources/recordings.txt'         
    rec = Recorder()    
    rec.load_recordings(file) 
    x = rec.get_recordings_names()
    rec.start_recording('newtest')
    for i in range(50):
        time.sleep(0.1)
    
    rec.stop_recording()
    rec.save_recordings(file)
    a = rec.sequence
  
    # rec.run_recording('newtest')





















