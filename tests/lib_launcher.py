import numpy as np
import os, sys, subprocess, time, ctypes
import win32gui, win32process

class Nwn_launcher:
    def __init__(self, account):
        self.account = account
        self.process = None
        self.hwnd    = None
        
    # cdkey.ini change
    def change_cd_key(self):
        with open(self.account['user_dir'] + '/' + 'cdkey.ini', 'w') as file:
            file.write('[NWN1]\nYourKey=' + self.account['key'])
   
    # settings.tml name change          
    def change_tml_file_pos_size_window(self):  
        with open(self.account['user_dir'] + '/' + 'settings.tml', 'r') as file :
            filedata = file.readlines()
            for num, line in enumerate(filedata):
                if 'name = ' in line:
                    filedata[num] = '\t\tname = "{}" \n'.format(self.account['name'])
                    break
        # Write the file out again
        with open(self.account['user_dir'] + '/' + 'settings.tml', 'w') as file:
            file.writelines(filedata)
   
    # key_ini_file logs change  
    def change_logs_directory(self):   
        logs_dir = self.account['user_dir'] + '/' + 'logs_' + self.account['name']
        with open(self.account['user_dir'] + '/' + 'nwn.ini', 'r') as file :
            filedata = file.readlines()
            for num, line in enumerate(filedata):
                if 'LOGS=' in line:
                    filedata[num] = 'LOGS=' + logs_dir  + '\n'
                    break 
        # Write the file out again
        with open(self.account['user_dir'] + '/' + 'nwn.ini', 'w') as file:
            file.writelines(filedata)    
            
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

    def rotate_logs(self):          
        # logs rotation
        logs_dir = self.account['user_dir'] + '/' + 'logs_' + self.account['name']
        keep_n_logs = self.account['logs_num']
        files  = os.listdir(logs_dir)
        
        files = [logs_dir + r'/' + f for f in files]    
        loggs = []
        for file in files:
            if '_' in os.path.basename(file):
                loggs.append(file)
        if len(loggs) > keep_n_logs-1:
            for file in loggs[keep_n_logs-1:]:
                os.remove(file)
                loggs.remove(file)
        for file in reversed(loggs):  
            number = int(os.path.basename(file).split('_')[0].split(r'/')[-1])
            new_name = logs_dir + r'/' + "{:02d}".format(number+1) + '_' + os.path.basename(file).split('_')[1]
            os.rename(file, new_name)
        os.rename(logs_dir + '/' + 'nwclientLog1.txt', 
        logs_dir + '/' + '01_nwclientLog1.txt')            
        return 
    
    def prepare_all(self):
        self.change_cd_key()
        self.change_tml_file_pos_size_window()
        self.change_logs_directory()
        self.rotate_logs()  
       
    def get_hwnds_for_pid (self,pid):
        def callback (hwnd, hwnds):
          if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled (hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId (hwnd)
            if found_pid == pid:
                hwnds.append (hwnd)
          return True
    
        hwnds = []
        win32gui.EnumWindows (callback, hwnds)
        return hwnds  
    
    # run application
    def run_game(self):
        os.chdir(self.account['game_dir'])
        if self.account['ip'] == '':
            process = subprocess.Popen([self.account['game_dir']+'/nwmain.exe'])
        else:
            process = subprocess.Popen([self.account['game_dir']+'/nwmain.exe', '+connect', self.account['ip']])
        self.process = process
    
    # move application
    def adjust_game(self):
        time.sleep(2)
        user32 = ctypes.windll.user32
        # handle = user32.FindWindowW(None, self.account['win_name'])
        handle = self.get_hwnds_for_pid(self.process.pid)[0]
        self.hwnd = handle
        user32.MoveWindow(handle, self.account['pos'][0], self.account['pos'][1], self.account['size'][0], self.account['size'][1], True)
        
    def get_if_process_running(self):
        # print(self.process.poll())
        if self.process.poll() == None:
            return True
        return False
# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':
    account1 = {'name':      "mk",           
               'pos':       [0, 0], 
               'size':      [1900,1150],  
               'logs_num':  5,
               'ip':        '188.244.50.172:5121',
               'key':       'AUEXY-FEVC9-DCAW3-HYM39-HFH9U-6ANCN-6VTCR', 
               'game_dir':   r'C:/Program Files (x86)/Steam/steamapps/common/Neverwinter Nights/bin/win32',
               'user_dir':   r'C:/Users/42073/Documents/Neverwinter Nights',
               }

    account2 = {'name':     "mk2",           
               'pos':       [-1900, 0],
               'size':      [1900,1050], 
               'logs_num':  5,
               'ip':        '188.244.50.172:5121',
               'key':       'KQKRX-MWQAC-KANT3-VXL9V-6U97Q-YHHPT-69N49',  
               'game_dir':   r'C:/Program Files (x86)/Steam/steamapps/common/Neverwinter Nights/bin/win32',
               'user_dir':   r'C:/Users/42073/Documents/Neverwinter Nights',
               }
    
    nwn_launcher = Nwn_launcher(account1)
    nwn_launcher.prepare_all()
    processid = nwn_launcher.run_game()
    nwn_launcher.adjust_game()
    while True:
        nwn_launcher.get_if_process_running()
        print(nwn_launcher.get_if_process_running())
        time.sleep(1)
    # time.sleep(2)       
             
    # nwn_launcher = Nwn_launcher(account2)
    # nwn_launcher.prepare_all()
    # nwn_launcher.run_game()
    # nwn_launcher.adjust_game()                        
                        
                        
                        
                        
                        
                        
                        
    