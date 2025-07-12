# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 00:13:00 2022

@author: 42073
"""
import pyperclip, keyboard
from multiprocessing import Process, Queue
import sys
sys.path.append(r'F:/lib')
from my_lib import io 
import time
import re, datetime  
import os
import pandas as pd
BOSSES   = [
          'NPC: Kallis Sentholin',
          'NPC: Svirfneblin Boss', 
          'NPC: Spiderling Woman', 
          'NPC: Archmage', 
          'NPC: Archdevil', 
          'NPC: Uzael, Demon High Duke', 
          'NPC: Restless Guardian', 
          'NPC: Goblin Adjutant',  
          'NPC: Giant High Mage', ]

class log_parser_dmg:
    def __init__(self, folder):
        print('dmg clac create')
        self.folder = folder
        self.calc_damages    = True
        self.calc_ab_ac      = True
        self.calc_kills      = True
        self.calc_boss_kills = True        
        self.lines = []
        self.dic_month_time_replace = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'June':6,'July':7,'Aug':8,'Sept':9,'Oct':10,'Nov':11,'Dec':12,
            'Mon':'', 'Tue':'', 'Wed':'', 'Thu':'', 'Fri':'', 'Sat':'', 'Sun':''}
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

    def send_data(self, message): 
        self.queue_data.put(message)         

        
    def worker_read_logs(self, queue_driver, queue_data):
        run = False
        while True:
            
            driver_queue_empty = queue_driver.empty()        
            if driver_queue_empty: 
                pass
            else: 
                run = queue_driver.get()   
                if run == True:
                    print('start')
                    self.starttime = datetime.datetime.now().timestamp()
                    # queue_data.put([kills, treasures])
                elif run == False: # stop and calulate  
                    try:
                        self.endtime = datetime.datetime.now().timestamp()
                        print(self.starttime )
                        print(self.endtime)
                        print(self.endtime - self.starttime)
                        print('calc')                        
                        self.readfiles('txt')
                        self.get_parsed_log_frame()
                        print('\n------------------------------before------------------------------')

                        print(self.frame)
                        self.frame = self.frame[self.frame['time_epoch'] > self.starttime]
                        print('------------------------------after------------------------------\n')
                        print(self.frame)                   
                        self.frame.to_excel("U:/_python/project/nwn_overlay/data/dmg_comaprison.xlsx")
                        frame = self.get_damage_comparison(self.endtime - self.starttime)
                        frame.to_excel("U:/_python/project/nwn_overlay/data/dmg_comaprison2.xlsx")
                        message = self.format_frame_to_string(frame)
                        # self.send_data(message)
                        # data = self.log_parser_dmg.get_data() 
                        # if data[0]:
                        lines = message.split('\n')
                        for line in lines:
                            pyperclip.copy(line)
                            # time.sleep(0.5)
                            # keyboard.press_and_release('enter')
                            # time.sleep(0.5)
                            # keyboard.press_and_release('ctrl+v')  
                            # time.sleep(0.5)
                            # keyboard.press_and_release('enter')
                            # time.sleep(0.5)
                            time.sleep(0.1)
                            keyboard.press('enter')
                            time.sleep(0.1)
                            keyboard.release('enter')
                            time.sleep(0.1)                            
                            keyboard.press('ctrl')
                            time.sleep(0.1)
                            keyboard.press('v')
                            time.sleep(0.1)
                            keyboard.release('v')
                            time.sleep(0.1)
                            keyboard.release('ctrl')
                            time.sleep(0.1)
                            keyboard.press('enter')
                            time.sleep(0.1)
                            keyboard.release('enter')                                                       
                        print('end')
                    except:
                        print('exception in lib_log_parser_dmg worker_read_logs function')
            time.sleep(1)
            
    def readfiles(self, string_in_filename = 'nwclientLog1.txt'):
  
        files = io.get_files(self.folder, in_all = [], in_any = [], ex_all = [], ex_any = [], ext = ['txt'], case_sens = False, search_subdirs = True, print_ = False )
        files = [f for f in files if not '_nwclientLog1' in f]
        files = [f for f in files if not 'nwclientError' in f]
        for f in files:
            print(f)
        lines, liness  = [], []
        for file in files:
            if string_in_filename in file:
                with open(file, encoding="Latin-1") as f:
                    _lines = f.readlines()
                liness = liness + _lines            
        self.lines = liness    
        print('files readed')
        return liness 

    def get_time_epoch_from_line(self, line):
        # print(line)
        # x = line
        # o = line.replace('[HC]', ' HC').replace('[Shout]','').replace('[CHAT WINDOW TEXT]', '').replace('[', '').strip().split(']')
        # print(o)
        # try:
        #     time, line = line.replace('[HC]', ' HC').replace('[Shout]','').replace('[CHAT WINDOW TEXT]', '').replace('[', '').strip().split(']')
        # except:
        #     print(5)
        pattern = r'[a-zA-Z0-9\s]*:\d+:\d+'
        time = re.findall(pattern, line)[0]
        line = line.split(time +'] ')[1]

        for key, val in self.dic_month_time_replace.items():
            time = time.replace(key, str(val))
        time = '2022'+time
        # time = time.replace(':', ' ').split(' ')
        time = time.replace('  ', ' ').replace(':', ' ').split(' ')
        try:
            y, m, d, h, minn, s = [int(i) for i in time]
        except:
            print(5)
        time_epoch = datetime.datetime(y, m, d, h, minn, s).timestamp() 
        return time_epoch, line
    
    def get_damage_from_line(self, line):
        attacker, line = line.split('damages')
        attacker = attacker.strip()
        defender, line = line.split(':')
        defender = defender.strip()
        damage    = int(re.findall(r'\d+\s', line)[0]) 
        return {'damage':damage, 'defender':defender, 'attacker':attacker, 'type':'damage'} 

    def get_kill_from_line(self, line):
        attacker, defender = line.split(' killed ')
        attacker = attacker.strip()
        defender = defender.strip()
        return {'attacker':attacker, 'defender':defender, 'type':'kill'} 

    def get_boss_kill_from_line(self, line):
        if ' has been slain' in line:
            defender = line.split(' has been slain')[0]
            defender = defender.strip()
        else:
            defender = line.replace(' NPC: ', '')
            # NPC: Kallis Sentholin,   Kill count: 1
        return {'defender':defender, 'type':'boss_kill'} 
        
    # TYPES - boss_kill, kill, damage
    def get_parsed_log_frame(self):
        frames, npcs = [], {}           
        for line in self.lines:
            dic = {'time_epoch':'none', 'type':'none', 'npc':False, 'attacker':'none', 'defender':'none',  'damage':'none', 'line':line}
            if '[Party]' in line or '[Shout]' in line:
                continue
            # CALCULATE DAMAGES 
            elif ' damages ' in line and self.calc_damages:   
                dic['time_epoch'], line = self.get_time_epoch_from_line(line)
                damages                 = self.get_damage_from_line(line)
                dic                     = {**dic, **damages}
                frames.append(pd.DataFrame([dic]))
            # CALCULATE BOSS KILLS 
            elif ' has been slain' in line or  any([boss in line for boss in BOSSES]):
                dic['time_epoch'], line = self.get_time_epoch_from_line(line)
                boss_kills              = self.get_boss_kill_from_line(line)
                dic                     = {**dic, **boss_kills}
                frames.append(pd.DataFrame([dic]))                  
                
            # CALCULATE KILLS
            elif 'killed ' in line and self.calc_kills:
                dic['time_epoch'], line = self.get_time_epoch_from_line(line)
                kills                   = self.get_kill_from_line(line)
                dic                     = {**dic, **kills}
                frames.append(pd.DataFrame([dic]))           
            else:pass
            
            if ' NPC: ' in line:
                npc = re.findall(r'NPC:.*,', line)[0].replace('NPC: ','')[0:-1]
                npcs[npc] = 0
        print('data parsed')     
    # [CHAT WINDOW TEXT] [Sun Nov 21 22:17:48] NPC: Bolgrol, Guardian of the Hell,   Kill count: 1    
       
        frame = pd.concat(frames)        
        frame = frame.sort_values(by='time_epoch')
        frame = frame.reset_index(drop=True)  
        
        # frame['NPC'] = False
        # creatures = frame[(frame['type'] == 'kill')]['defender'].unique()
        

       
        # dictionary of npcs from log parse 'NPC: ..... killed.'              
        for key, item in npcs.items():
            frame.loc[frame[(frame['attacker'] == key)].index, 'npc'] = True 
       
        # dictionary of npcs from txt file
        path = r'U:/_python/project/nwn_overlay/data/npc_list.txt'        
        npcs_txt = {}
        with open(path) as file:
            next_line =  file.readline()
            while next_line:
                npcs_txt[next_line.strip()] = 0
                next_line = file.readline()
        
        creatures_other =  frame[(frame['npc'] == False) & (frame['type'] == 'damage')]['attacker'].unique().tolist()        
        for creature_other in creatures_other:
            if creature_other in npcs_txt.keys():
                frame.loc[frame[(frame['attacker'] == creature_other)].index, 'npc'] = True  
        
        # merge and save dictionaries:
        list_to_save = list({**npcs_txt, **npcs}.keys()) 
        list_to_save.sort()
        with open(path, "w") as outfile:
            outfile.write("\n".join(list_to_save))

        self.frame = frame              
        return frame          

    def get_kills_count(self):
        frames, dic, frame = [], {}, self.frame
        aa = frame[(frame['npc'] == False) & (frame['type'] == 'kill')]['attacker'].unique()
        for player in aa:
            dic['player'] = player
            dic['kill_count'] = len(frame[(frame['attacker'] == player) & (frame['type'] == 'kill')])
            frames.append(pd.DataFrame([dic]))
        
        frame = pd.concat(frames)       
        frame = frame.sort_values(by='kill_count', ascending=False)
        frame = frame.reset_index(drop=True)
        return frame
    
    def get_damage_comparison(self, time_lenght):
        min_name_length = 20
        frames, dic, frame = [], {}, self.frame
        aa = frame[(frame['npc'] == False) & (frame['type'] == 'damage')]['attacker'].unique()
        for player in aa:
            dic['player'] = player
            damage = frame[(frame['attacker'] == player) & (frame['type'] == 'damage')]['damage'].sum()               
            dic['damage'] = damage
            dic['dpr'] = int(damage/time_lenght*6)
            dic['dps'] = int(damage/time_lenght)
            dic['time'] = int(time_lenght)            
            dic['percent'] = int(damage/time_lenght)
            frames.append(pd.DataFrame([dic]))
        
        frame = pd.concat(frames)       
        frame = frame.sort_values(by='damage', ascending=False)
        frame = frame.reset_index(drop=True)
        # maxx  = frame.iloc[0,1]
        total = frame['damage'].sum()
        frame['percent'] = frame['damage']/total*100
        frame['percent'] = frame['percent'].apply(lambda x: int(x))
        return frame


    def format_frame_to_string(self, frame):
        frame['player'] = frame['player'].apply(lambda x:x[0:35] )
        frame['player'] = frame['player'].apply(lambda x:x.replace(' ', '_').replace('  ', '_') )
        # frame['damage'] = frame['damage'].apply(lambda x: 'dt_'+str(x))
        
        frame['damage'] = frame['damage'].apply(lambda x: 'dtot-'+ str(round(x/1000,1))+'K' if (x >= 1000) else 'dt-'+str(x)) 
        
        frame['dpr']    = frame['dpr'].apply(lambda x: '..dpr-'+str(x))
        frame['dps']    = frame['dps'].apply(lambda x: '..dps-'+str(x))
        frame['time']    = frame['time'].apply(lambda x: '..ti-'+str(x))        
        frame['percent'] = frame['percent'].apply(lambda x: '..'+str(x) + '%')
        
        string = r'/w                       '
        columns = len(list(frame))
        rows = len(frame)
        for j in range(rows):
            string += '  '
            for i in range(columns):
                if i == 0:
                    lenn = len(frame.iloc[j, i])
                    if lenn < 20:
                        fill = 20 - lenn
                        string += frame.iloc[j, i]+'_'*fill    +' '
                    else:                   
                        string += frame.iloc[j, i]+' '
                else:
                    string += frame.iloc[j, i]
        print(string)
        return string
    
    def get_boss_kills(self):
        frame = self.frame
        frame = frame[(frame['type'] == 'boss_kill')]
        return frame
        
# =============================================================================
# MAIN    
# =============================================================================
if __name__ == '__main__':
# TODO nefunguje ex_all a ex_any pri cteni files
    parser       = log_parser_dmg(r'C:/Users/42073/Documents/Neverwinter Nights/logs_mk')       
    parser.readfiles('txt')
    frame        = parser.get_parsed_log_frame()
    f_dmg        = parser.get_damage_comparison(100)
    # f_boss_kills = parser.get_boss_kills()
    # f_kill_count = parser.get_kills_count()
                
    anpcs        =  frame[(frame['npc'] == True) & (frame['type'] == 'damage')]['attacker'].unique().tolist()
    aplayers     =  frame[(frame['npc'] == False) & (frame['type'] == 'damage')]['attacker'].unique().tolist() 
      
    















        