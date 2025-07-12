import sys, os; sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'lib')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__))))

import ctypes as c
import numpy as np
import multiprocessing as mp
from multiprocessing import Process
import time, keyboard, mouse, datetime, win32gui, pyperclip

from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

import lib_driver as ldr
import lib_geometry as lge
import lib_launcher as lla
import lib_bg_thread as bgt
import lib_log_parser as logp
import lib_log_parser_dmg as llpd

from lib_calc import Calc
from lib_config_window import Config_Window

import params_accounts as par
import params_geometry as parg


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow, current_account):
        self.MainWindow = MainWindow

#-----------------------------LAUNCH GAME--------------------------------------
        self.nwn_launcher = lla.Nwn_launcher(current_account)
        self.nwn_launcher.prepare_all()
        self.nwn_launcher.run_game()
        self.nwn_launcher.adjust_game()    
         
#-------------------------------GEOMETRY---------------------------------------
        self.game_window = lge.Geometry(self.nwn_launcher.hwnd)   
        
#---------------------------------WINDOW SETTINGS------------------------------
        MainWindow.setObjectName("Overlay")
        MainWindow.resize(self.game_window.rect_game [2] - self.game_window.rect_game [0]+5, self.game_window.rect_game [3] - self.game_window.rect_game [1]+30)
        MainWindow.move(self.game_window.rect_game [0]+1, self.game_window.rect_game [1]+1)
        MainWindow.setWindowFlags ( QtCore.Qt.FramelessWindowHint  | 
                                    QtCore.Qt.WindowStaysOnTopHint | 
                                    QtCore.Qt.WindowTransparentForInput)    
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
      
#----------------------------------LABEL KILLS---------------------------------
        self.label_kills = QtWidgets.QLabel(self.centralwidget) 
        self.label_kills.setFont(QFont('Arial', 12))
        self.label_kills.setAutoFillBackground(False)
        self.label_kills.setAlignment(QtCore.Qt.AlignTop)     
        self.label_kills.setGeometry(QtCore.QRect(370, 30, 0, 0))
        self.label_kills.setObjectName("label_kills")
        self.label_kills.setStyleSheet("background-color: rgba(255, 255, 255, 150);")
        
#----------------------------------LABEL TREASURES-----------------------------
        self.label_treasures = QtWidgets.QLabel(self.centralwidget) 
        self.label_treasures.setFont(QFont('Arial', 12))
        self.label_treasures.setAutoFillBackground(False)
        self.label_treasures.setAlignment(QtCore.Qt.AlignCenter)     
        self.label_treasures.setGeometry(QtCore.QRect(600, 500, 0, 0))
        self.label_treasures.setObjectName("label_kills")
        self.label_treasures.setStyleSheet("background-color: rgba(255, 0, 0, 150);")   
      
#----------------------------------LABEL HEALTH--------------------------------
        self.label_health = QtWidgets.QLabel(self.centralwidget) 
        self.label_health.setFont(QFont('Arial', 12))
        self.label_health.setAutoFillBackground(False)
        self.label_health.setAlignment(QtCore.Qt.AlignCenter)     
        self.label_health.setGeometry(QtCore.QRect(800, 800, 0, 0))
        self.label_health.setObjectName("label_health")
        self.label_health.setStyleSheet("background-color: rgba(255, 0, 0, 150);")   
        
#----------------------------------LABEL STOPWATCH-----------------------------
        self.stopwatch = QtWidgets.QLabel(self.centralwidget) 
        self.stopwatch.setFont(QFont('Arial', 12))
        self.stopwatch.setAutoFillBackground(False)
        self.stopwatch.setAlignment(QtCore.Qt.AlignCenter)  
        x, y, x2, y2 = self.game_window.rect_stopwatch
        self.stopwatch.setGeometry(QtCore.QRect(x, y, y2-y, x2-x))
        self.stopwatch.setObjectName("label_health")
        self.stopwatch.setStyleSheet("background-color: rgba(255, 0, 0, 150);") 
        self.stopwatch_time = 0
        self.stopwatch_toggle_last = 0
        self.stopwatch_toggle_current = 0    
#----------------------------------LABEL shadow evade-----------------------------
        self.shadow_evade = QtWidgets.QLabel(self.centralwidget) 
        self.shadow_evade.setFont(QFont('Arial', 12))
        self.shadow_evade.setAutoFillBackground(False)
        self.shadow_evade.setAlignment(QtCore.Qt.AlignCenter)  
        x, y, x2, y2 = self.game_window.shadow_evade
        self.shadow_evade.setGeometry(QtCore.QRect(x, y, 0,0))
        self.shadow_evade.setObjectName("label_shadow_evade")
        self.shadow_evade.setStyleSheet("background-color: rgba(255, 0, 0, 150);") 
        self.shadow_evade_timer = 126
        self.shadow_evade_state = 0
#----------------------------------LABEL shadow twin-----------------------------
        self.shadow_twin = QtWidgets.QLabel(self.centralwidget) 
        self.shadow_twin.setFont(QFont('Arial', 12))
        self.shadow_twin.setAutoFillBackground(False)
        self.shadow_twin.setAlignment(QtCore.Qt.AlignCenter)  
        x, y, x2, y2 = self.game_window.shadow_twin
        self.shadow_twin.setGeometry(QtCore.QRect(x, y, 0,0))
        self.shadow_twin.setObjectName("label_shadow_twin")
        self.shadow_twin.setStyleSheet("background-color: rgba(255, 0, 0, 150);") 
        self.shadow_twin_timer = 240
        self.shadow_twin_state = 0         
#----------------------------------LABEL AUTO HEAL-----------------------------
        self.label_auto_heal = QtWidgets.QLabel(self.centralwidget) 
        self.label_auto_heal.setFont(QFont('Arial', 12))
        self.label_auto_heal.setAutoFillBackground(False)
        self.label_auto_heal.setAlignment(QtCore.Qt.AlignCenter)     
        self.label_auto_heal.setGeometry(QtCore.QRect(700, 700, 100, 100))
        self.label_auto_heal.setObjectName("label_auto_heal")
        self.label_auto_heal.setStyleSheet("background-color: rgba(255, 0, 0, 150);") 
        self.auto_heal      = False
        self.member_to_heal = False
#----------------------------------LABEL DMG COUNTER---------------------------
        self.label_dmg_counter = QtWidgets.QLabel(self.centralwidget) 
        self.label_dmg_counter.setFont(QFont('Arial', 12))
        self.label_dmg_counter.setAutoFillBackground(False)
        self.label_dmg_counter.setAlignment(QtCore.Qt.AlignCenter)     
        self.label_dmg_counter.setGeometry(QtCore.QRect(900, 900, 100, 100))
        self.label_dmg_counter.setObjectName("label_auto_heal")
        self.label_dmg_counter.setStyleSheet("background-color: rgba(255, 0, 0, 150);") 
        self.log_parser_dmg = llpd.log_parser_dmg('C:/Users/42073/Documents/Neverwinter Nights/logs_mk')
        self.dmg_counter_value   = False       
        
#------------------------------LABELS PARTY MEMBERS----------------------------      
        self.party_members = []
        for i in range(9):
            label = QtWidgets.QLabel(self.centralwidget) 
            label.setFont(QFont('Arial', 12))
            label.setAutoFillBackground(False)
            label.setAlignment(QtCore.Qt.AlignCenter)     
            label.setGeometry(QtCore.QRect(800, 800, 0, 0))
            label.setObjectName("label_health" + str(i))
            label.setStyleSheet("background-color: rgba(255, 0, 0, 150);") 
            self.party_members.append(label)        

#-----------------------------LISTENER----------------------------        
        keyboard.on_press(self.on_key_down)     
        
#-----------------------------MULTIPROC DATA-----------------------------------
        x, y, w, h  = self.game_window.rect_game
        paramss = {'size':[w, h ] }
        self.mp_capture = mp.Array(c.c_ubyte, paramss['size'][1] *paramss['size'][0]*4) # [0] run/stop, [1] frame number
        self.capture    = np.frombuffer(self.mp_capture.get_obj(),dtype=np.uint8).reshape((paramss['size'][1] ,paramss['size'][0],4))
        self.mp_states  = mp.Array(c.c_uint, 10)   
        self.states     = np.frombuffer(self.mp_states.get_obj(),dtype=np.uint)               
        p = Process(target=bgt.capture_screen, args=(self.mp_capture, self.mp_states, self.game_window), daemon=True)
        p.start()            
        

#----------------------------------DRIVER--------------------------------------    
        self.driver     = ldr.Driver(self.states)
        self.driver.start_bg_thread()        
        self.log_parser = logp.Log_parser(current_account)
        self.log_parser.start_logs()
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
#----------------------------------TIMERS--------------------------------------
        self.timer_msec=QtCore.QTimer()
        self.timer_msec.timeout.connect(self.Ontimer_msec)
        self.timer_msec.start(1)
        self.counter = 0
        self.timer_sec=QtCore.QTimer()
        self.timer_sec.timeout.connect(self.Ontimer_sec)
        self.timer_sec.start(1000)        
        
# =============================================================================
#                             METHODS
# =============================================================================
    def refresh_tab(self):
        keyboard.release('tab')
        keyboard.press('tab')  
        keyboard.press('tab') 
        keyboard.press('tab')   
            
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
    def update_object(self, object_, x, y, w, h, r, g, b, o, text, size = 12):
        object_.setText(text)  
        object_.setGeometry(QtCore.QRect(x, y, w, h))
        object_.setStyleSheet(f"background-color: rgba({r},{g}, {b}, {o});")
        object_.setFont(QFont('Arial', size))
   
    def update_auto_heal(self):
        x, y, x2, y2 = self.game_window.rect_auto_heal_on_off
        if self.auto_heal:            
            self.update_object(self.label_auto_heal, x, y, x2-x, y2-y, 0, 255, 0, 255, 'ON', size = 20) 
        else:
            self.update_object(self.label_auto_heal, x, y, x2-x, y2-y, 255, 0, 0, 255, 'OFF', size = 20)            

    def update_dmg_counter(self):
        x, y, x2, y2 = self.game_window.rect_dmg_counter_on_off
        if self.dmg_counter_value:            
            self.update_object(self.label_dmg_counter, x, y, x2-x, y2-y, 0, 255, 0, 255, 'ON', size = 20) 
        else:
            self.update_object(self.label_dmg_counter, x, y, x2-x, y2-y, 255, 0, 0, 255, 'OFF', size = 20)  
            
    def update_boss_kills(self, kills):
        x, y, x2, y2 = self.game_window.rect_boss_kills
        string, num = '', 0
        for kill in kills:
            string += '   ' + kill.replace('[CHAT WINDOW TEXT] ', '') + '\n'
            num+= 1
        self.update_object(self.label_kills, x, y, x2-x, num*20, 255, 255, 255, 150, string)          
    
    def update_treasures(self, treasures):
        string, num = '', 0
        for treasure in treasures:
            string += '   ' + treasure.replace('[CHAT WINDOW TEXT] ', '') 
            num += 1
        self.update_object(self.label_treasures, 700, 550, 550, num*20, 255, 0, 0, 150, string) 
        
    def update_health(self, value):
        self.update_object(self.label_health, 284, 700, 60, 60, 255, 0, 0, 255, str(value), size = 20)    

    def update_stopwatch(self, show, value):
        x, y, x2, y2 = self.game_window.rect_stopwatch
        if show:
            time = str(datetime.timedelta(seconds=value))
                
            self.update_object(self.stopwatch, x, y, x2-x, y2-y, 255, 0, 0, 255, time, size = 16) 
        else:
            self.update_object(self.stopwatch, x, y, y-y2, x2-x, 255, 0, 0, 0, '0', size = 20) 
    
    def update_shadow_evade(self, show, value):
        x, y, x2, y2 = self.game_window.shadow_evade
        if show:
            time = str(self.shadow_evade_timer)
                
            self.update_object(self.shadow_evade, x, y, x2-x, y2-y, 0,255, 0, 255, time, size = 16) 
        else:
            self.update_object(self.shadow_evade, x, y, y-y2, x2-x, 0,255, 0, 0, '0', size = 20)  
            
    def update_shadow_twin(self, show, value):
        x, y, x2, y2 = self.game_window.shadow_twin
        if show:
            time = str(self.shadow_twin_timer)
                
            self.update_object(self.shadow_twin, x, y, x2-x, y2-y, 0, 255, 0, 255, time, size = 16) 
        else:
            self.update_object(self.shadow_twin, x, y, y-y2, x2-x, 0, 255, 0, 0, '0', size = 20)    
            
    def update_party(self, members, labels):
        members = [member for member in members if member[1] == True]
        count      = len(members)
        mon_middle = 950
        box_width  = 50
        space_width = 25
        boxandspace = box_width + space_width
        start_x_pos = int(mon_middle - box_width/2*count - space_width/2 * (count - 1))
        healt_max, health_value, member_to_heal = 150, 150, False
        
        for num, label in  enumerate(labels):
            if num < len(members) and members[num][1] == True:
                member = members[num]
                health_value = member[2]
                if health_value < 40:
                    self.update_object(label, start_x_pos + boxandspace*num, 750, box_width, box_width, 255, 0, 0, 255, str(health_value), size = 20)                    
                elif health_value < 70:
                    self.update_object(label, start_x_pos + boxandspace*num, 750, box_width, box_width, 255, 234, 0, 255, str(health_value), size = 20)  
                else:
                    self.update_object(label, start_x_pos + boxandspace*num, 750, box_width, box_width, 0, 255, 0, 255, str(health_value), size = 20) 
            else:
                self.update_object(label, start_x_pos + boxandspace*num, 550, 0, 0, 255, 0, 0, 150, '') 
            if (health_value < healt_max) and  (health_value > 0 ):
                healt_max = health_value
                member_to_heal = num  + 1  
        self.member_to_heal = member_to_heal
        return member_to_heal

    def on_key_down(self, key):
        name = key.name
        if name == parg.keybinds['start_stop_dps_counter']:
            self.dmg_counter_value = 1 - self.dmg_counter_value # toggle 0 and 1
            if self.dmg_counter_value == True:
                self.log_parser_dmg.start_logs()
                print('start logs')
            if self.dmg_counter_value == False:
                self.log_parser_dmg.stop_logs()       
                print('stop logs')
        if name == parg.keybinds['toggle_keybinds_on_off']:
            self.auto_heal = 1 - self.auto_heal # toggle 0 and 1
            
        if name == parg.keybinds['shadow_evade']:
            self.shadow_evade_state = 1  # toggle 0 and 1
            self.shadow_evade_timer = 126
            
        if name == parg.keybinds['shadow_twin']:
            self.shadow_twin_state = 1  # toggle 0 and 1
            self.shadow_twin_timer = 240
            
        if name == parg.keybinds['toggle_stopwatch']:
            self.stopwatch_toggle_current = 1 - self.stopwatch_toggle_current # toggle 0 and 1  
            
        if self.member_to_heal:
            if self.auto_heal:
                if any(name == item for item in [parg.keybinds['key_1'], parg.keybinds['key_2'], parg.keybinds['key_3'], parg.keybinds['key_4']]):
                    x, y = mouse.get_position()  
                    self.game_window.set_mouse_pos(self.x,self.y, rel_to = 4)
                    time.sleep(0.05)   
                    mouse.click()
                    time.sleep(0.05)        
                    mouse.move(x, y) 
# =============================================================================
#                       TIMER SECONDS
# =============================================================================

    def Ontimer_sec(self):          
        if self.stopwatch_toggle_current == 0:
            self.stopwatch_time = 0
            self.update_stopwatch(False, self.stopwatch_time)
            
        elif self.stopwatch_toggle_current == 1:
            self.update_stopwatch(True, self.stopwatch_time)
            self.stopwatch_time += 1
        
        if self.shadow_evade_state == 0:
            self.update_shadow_evade(False, self.shadow_evade_state)  
       
        elif self.shadow_evade_state == 1:
            self.update_shadow_evade(True, self.shadow_evade_state)
            self.shadow_evade_timer -= 1    
            if self.shadow_evade_timer <= 0:
                self.shadow_evade_state = 0
                
        if self.shadow_twin_state == 0:
            self.update_shadow_twin(False, self.shadow_twin_state)  
       
        elif self.shadow_twin_state == 1:
            self.update_shadow_twin(True, self.shadow_twin_state)
            self.shadow_twin_timer -= 1    
            if self.shadow_twin_timer <= 0:
                self.shadow_twin_state = 0                
            
            
        if self.game_window.is_game_active_by_hwnd():
            self.refresh_tab()
        self.close()
# =============================================================================
#                       TIMER MILISECONDS
# =============================================================================    
    def Ontimer_msec(self):  
        # close app when game closed
        if not self.nwn_launcher.get_if_process_running():
            self.MainWindow.close()
       
        # parse log and update kills label    
        data = self.log_parser.get_data()
        if data[0]:
            kills, treasures = data[1]
            self.update_boss_kills(kills)
            self.update_treasures(treasures)           
        
        # capture screen
        self.capture = self.capture
        
        # update main char label
        x1, y1, x2, y2 = self.game_window.rect_health
        chunk_self     = self.capture[ y1: y2, x1:x2]
        
        # update party char labels      
        x1, y1, x2, y2 = self.game_window.rect_party_members
        chunk  = self.capture[ y1: y2, x1:x2]
        members = Calc.get_party_members(chunk)

        x1, y1, x2, y2 = self.game_window.rect_healt_party
        chunk  = self.capture[ y1: y2, x1:x2]        
        members = Calc.get_party_health(chunk_self, chunk, members)
        position_to_heal = self.update_party(members, self.party_members)

        if position_to_heal:            
            self.x, self.y = parg.pos_to_heal[position_to_heal]  
            
        # update auto heal label
        self.update_auto_heal()  
        
        self.update_dmg_counter()
        
# =============================================================================
#                                  MAIN                         
# =============================================================================
def main(argv):
    account_to_select = [None]
    app = QtWidgets.QApplication(argv)
    config_window = Config_Window(par.accounts, account_to_select)
    if ( not app.exec_() ): 
        current_account = par.accounts[account_to_select[0]] 
        if current_account['overlay']:
            MainWindow = QtWidgets.QMainWindow()
            ui = Ui_MainWindow()            
            ui.setupUi(MainWindow, current_account)
            MainWindow.show()            
            hwnd = ui.nwn_launcher.hwnd
            win32gui.SetForegroundWindow(hwnd)
            sys.exit(app.exec_())
        else:
            nwn_launcher = lla.Nwn_launcher(current_account)
            nwn_launcher.prepare_all()
            nwn_launcher.run_game()
            nwn_launcher.adjust_game() 

if __name__ == "__main__":    
    main(sys.argv)

   


