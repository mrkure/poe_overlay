# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 08:56:38 2022

@author: 42073
"""

from multiprocessing import Process, Queue

import time

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 22:58:06 2022

@author: 42073
"""
import os, re
from datetime import datetime

bosses = [
          'NPC: Svirfneblin Boss', 
          'NPC: Spiderling Woman', 
          'NPC: Archmage', 
          'NPC: Archdevil', 
          'NPC: Uzael, Demon High Duke', 
          'NPC: Restless Guardian', 
          'NPC: Goblin Adjutant',  
          'NPC: Giant High Mage',            
          'slain']
treasures = [
            'treasure22', 'Treasure22']


class Log_parser:
    def __init__(self, folder):
        self.folder = folder
        self.lines          = []
        self.lines_filtered = []
        self.queue_driver, self.queue_data = Queue(), Queue()
        reader_p = Process(target=self.worker_read_logs, args=(self.queue_driver, self.queue_data))
        reader_p.start()  
         
    def stop_logs(self):
        self.queue_driver.put(False)
        return
    
    def start_logs(self):
        self.queue_driver.put(True)
        return
     
    def get_data(self):
        if not self.queue_data.empty():
            msg = self.queue_data.get()         
            return msg
        else:return 'empty queue'
    
    def worker_read_logs(self, queue_driver, queue_data):
        run = False
        while True:
            
            driver_queue_empty = queue_driver.empty()        
            if driver_queue_empty: pass
            else: run = queue_driver.get()   
            # print('from worker ', run)
            if run == True:

                self.readfiles()
                self.get_filtered_lines()
                kills      = self.get_boss_kills()    
                treasures  = self.get_treasure()  
                queue_data.put([kills, treasures])
            else:pass
            time.sleep(1)

    def readfiles(self, string_in_filename = 'nwclientLog'):
        # READ ALL FILES TO LINES
        files  = os.listdir(self.folder)
        files = [self.folder + r'/' + f for f in files]    
        
        lines, liness  = [], []
        for file in files:
            if string_in_filename in file:
                with open(file, encoding="Latin-1") as f:
                    _lines = f.readlines()
                liness = liness + _lines            
        for line in liness:
            lines.append(line.rstrip().lstrip())  
        self.lines = lines    
        return lines  
    
    def get_time_delta_from_line(self, line):
        dic     = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'June':6,'July':7,'Aug':8,'Sept':9,'Oct':10,'Nov':11,'Dec':12}        
        pattern = r'(\w{2,3}\s\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})'
        time    = re.findall(pattern, line)[0].replace(':', ' ').split(' ')
        now     = datetime.now()
        bef     = datetime(now.year, dic[time[0]], int(time[1]), int(time[2]), int(time[3]), int(time[4]))
        delta   = int((now-bef).total_seconds()/60)        
        return delta

    def get_filtered_lines(self):   
        self.lines_filtered = []
        for line in self.lines:
            if any ([objectt in line for objectt in bosses+treasures]):
                self.lines_filtered.append(line)
        return self.lines_filtered
        
    def get_boss_kills(self, last_x_lines = 5):
        lines, lines2 = [], []
        for line in self.lines_filtered:
            if any ([boss in line for boss in bosses]):
                lines.append(line)

        for num, line in enumerate(lines):       
            time = self.get_time_delta_from_line(line)
            if time < 400:
                # lines2.append('{} min: {}'.format(time, line.split(']')[-1] )) 
                pattern   = r'(\[[a-zA-Z ]{2,50}\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\])'
                to_remove = re.findall(pattern, line)
                lines2.append('{} min: {}'.format(time, line.replace(to_remove[0], '') )) 
        lines2 = lines2[-last_x_lines:][::-1]
        return lines2
    
    def get_treasure(self, selflast_x_lines = 2):
        lines, lines2 = [], []
        for line in self.lines_filtered:
            if any ([string in line for string in treasures]):
                lines.append(line)
        for num, line in enumerate(lines):       
            time = self.get_time_delta_from_line(line)
            if time < 10:
                time  = '0' + str(time)
            else:
                time = str(time)        
            if time < 2:
                lines2.append('{:02d} min: {}'.format(time, line.split(']')[-1] ))                
        lines2 = lines2[-1:]
        return lines2


            
if __name__ == '__main__':
        log_parser = Log_parser(r'C:/Users/42073/Documents/Neverwinter Nights/logs')
        log_parser.start_logs()
        while True:
            print(log_parser.get_data())
            time.sleep(1)
            log_parser.stop_logs()
            






# def stop_logs(queue):
#     queue_driver.put('stop')
#     return

# def start_logs(queue):
#     queue_driver.put(True)
#     return
 
# def get_data(queue):
#     # print('from get data')
#     if not queue.empty():
#         msg = queue.get()         
#         return msg
#     else:return 'empty queue'

# def worker_read_logs(queue_driver, queue_data):
#     x, run = 0, False
#     while True:
#         driver_queue_empty = queue_driver.empty()        
#         if driver_queue_empty: pass
#         else: run = queue_driver.get()   
        
#         if run == True:
#             # evaluate logs
#             queue_data.put('result string')
#         else:pass
#         time.sleep(3.2)
#         x += 1
        
        
# if __name__=='__main__':
#     queue_driver, queue_data = Queue(), Queue()
#     reader_p = Process(target=worker_read_logs, args=(queue_driver, queue_data))
#     reader_p.start()   
#     # start_logs(queue_driver)
#     x = 0
#     while True:
#         print(get_data(queue_data))
#         time.sleep(1)
#         # stop_logs(queue_driver)
#         if x == 10:
#             break
#         x += 1
        
        
        
    # reader_p.daemon = True
  
    # input('asdfsaf')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    