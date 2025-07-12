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
kills_number  = 5
kills_time    = 40
treasure_time = 1


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
treasures = ['treasure22', 'Treasure22']


class Log_parser:
    def __init__(self, account):
        self.folder = account['user_dir'] + '/' 'logs_' + account['name']
        # print(self.folder)
        self.lines          = []
        self.lines_filtered = []
        self.queue_driver, self.queue_data = Queue(), Queue()
        reader_p = Process(target=self.worker_read_logs, args=(self.queue_driver, self.queue_data), daemon=True)
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
            return [True, msg]
        else:return [False, '']
    
    def worker_read_logs(self, queue_driver, queue_data):
        run = False
        while True:
            
            driver_queue_empty = queue_driver.empty()        
            if driver_queue_empty: pass
            else: run = queue_driver.get()   
            if run == True:
                self.readfiles()
                self.get_filtered_lines()
                kills      = self.get_boss_kills(kills_number)    
                treasures  = self.get_treasure()  
                queue_data.put([kills, treasures])
            else:pass
            time.sleep(1)

    def readfiles(self, string_in_filename = 'nwclientLog'):
        files  = os.listdir(self.folder)
        files = [self.folder + r'/' + f for f in files]    
        # print(files)
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
        pattern = r'(\w{2,3}\s*\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})'
        timee   = re.findall(pattern, line)[0].replace('  ', ' ').replace(':', ' ').split(' ')
        now     = datetime.now()
        bef     = datetime(now.year, dic[timee[0]], int(timee[1]), int(timee[2]), int(timee[3]), int(timee[4]))
        delta   = int((now-bef).total_seconds()/60)        
        return delta

    def get_filtered_lines(self):   
        self.lines_filtered = []
        for line in self.lines:
            if any ([objectt in line for objectt in bosses+treasures]):
                self.lines_filtered.append(line)
        # print(self.lines_filtered)
        return self.lines_filtered
        
    def get_boss_kills(self, last_x_lines = 5):
        lines, lines2 = [], []
        for line in self.lines_filtered:
            if any ([boss in line for boss in bosses]):
                lines.append(line)

        for num, line in enumerate(lines):       
            time = self.get_time_delta_from_line(line)
            if time < kills_time:
                pattern   = r'(\[[a-zA-Z ]{2,50}\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\])'
                to_remove = re.findall(pattern, line)
                lines2.append('{:02d} min: {}'.format(time, line.replace(to_remove[0], '') )) 
        lines2 = lines2[-last_x_lines:][::-1]
        return lines2
    
    def get_treasure(self):
        lines, lines2 = [], []
        for line in self.lines_filtered:
            if any ([string in line for string in treasures]):
                lines.append(line)
        for num, line in enumerate(lines):       
            time = self.get_time_delta_from_line(line)      
            if time < treasure_time:
                lines2.append('{:02d} min: {}'.format(time, line.split(']')[-1] ))                
        lines2 = lines2[-1:]
        return lines2


           
if __name__ == '__main__':
    import params 
    log_parser = Log_parser(params.account1)
    log_parser.start_logs()
    while True:
        print(log_parser.get_data())
        time.sleep(1)
        # log_parser.stop_logs()
            


    # line = r'[CHAT WINDOW TEXT] [Tue Feb  1 08:21:34] The Summoner has been slain.'
    # dic     = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'June':6,'July':7,'Aug':8,'Sept':9,'Oct':10,'Nov':11,'Dec':12}        
    # pattern = r'(\w{2,3}\s*\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})'

    # timee    = re.findall(pattern, line)[0].replace('  ', ' ').replace(':', ' ').split(' ')



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    