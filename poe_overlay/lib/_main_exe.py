# -*- coding: utf-8 -*-

import os
import sys
import time
import ctypes as c
import multiprocessing as mp
from multiprocessing import Process

import win32gui
import numpy as np
import keyboard
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QPushButton

from params import params
import lib_bg_thread as bgt
import lib_recorder as lrec
from lib_mouse import mo_manager
from lib_keyboard import kb_manager
from mk_css import dic_css
from PyQt5.QtCore import QPoint, QTimer

ui_path_buttons = f"{os.path.split(os.path.dirname(__file__))[0]}/res/window_buttons2.ui"
ui_path_main = f"{os.path.split(os.path.dirname(__file__))[0]}/res/window_main.ui"
icon_path = f"{os.path.split(os.path.dirname(__file__))[0]}/res/icons8-photo-gallery-64.png"
target_app_name = "Path of Exile"


class ButtonsWindow(QtWidgets.QWidget):
    """buttons window"""

    submitted = qtc.pyqtSignal(str)  # custom signal definition, static variable shared by all instances of the class

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(ui_path_buttons, self)
        self.setWindowFlags(qtc.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.Tool)
        self.hooked = False
        self.setStyleSheet(dic_css['gray'])
        # print(self.pushButton_unhooked.palette().button().color().name())
        for widget in self.children():
            if isinstance(widget, QPushButton):
                widget.clicked.connect(self.on_button_clicked)
                # widget.setStyleSheet(params["button_inactive"])

    def on_button_clicked(self):
        """emit signal in button click, to main window -> send name of button clicked"""
        self.submitted.emit(self.sender().text())

    def mousePressEvent(self, evt):
        self.oldPos = evt.globalPos()

    def mouseMoveEvent(self, evt):
        if self.underMouse():
            delta = QPoint(evt.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = evt.globalPos()    


class CustomWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Window")
        x, y, w, h = params["health_bar_geo"]
        self.setGeometry(qtc.QRect(x, y, w, h))  # x, y, width, height

        # Create label at position (50, 80)
        self.label = QtWidgets.QLabel("Hello from Custom Window", self)
        self.label.setGeometry(0,0,w,h)
        # self.label.move(50, 80)  # x, y
        # self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.WindowTransparentForInput | qtc.Qt.Tool)
        self.setWindowFlags(qtc.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.Tool)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)
        self.label.setStyleSheet("""
            QLabel {

                border: 2px solid red;
                color: white;
                font-size: 14px;
            }
        """)
        self.label3 = QtWidgets.QLabel("Hello from Custom Window", self)
        self.label3.setGeometry(115, 950,   15,  180)
        # self.label.move(50, 80)  # x, y
        # self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.WindowTransparentForInput | qtc.Qt.Tool)

        self.label3.setStyleSheet("""
            QLabel {

                border: 2px solid red;
                color: white;
                font-size: 14px;
            }
        """)

        [115, 950,   15,  180]
class CustomWindow2(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Window")
        x, y, w, h = params["window_geo"]
        self.setGeometry(qtc.QRect(x, y, w, h))  # x, y, width, height

        # Create label at position (50, 80)
        self.label = QtWidgets.QLabel("Hello from Custom Window", self)
        self.label.setGeometry(0,0,w,h)
        # self.label.move(50, 80)  # x, y
        # self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.WindowTransparentForInput | qtc.Qt.Tool)
        self.setWindowFlags(qtc.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.Tool)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)
        self.label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: 2px solid red;
                color: white;
                font-size: 14px;
            }
        """)

        self.label3 = QtWidgets.QLabel("Hello from Custom Window", self)
        self.label3.setGeometry(115, 950,   15,  180)
        # self.label.move(50, 80)  # x, y
        # self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.WindowTransparentForInput | qtc.Qt.Tool)

        self.label3.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: 2px solid red;
                color: white;
                font-size: 14px;
            }
        """)     

class MainWindow(QtWidgets.QWidget):
    """main window class invisible window on the whole monitor"""

    # _______________________________________ INIT _______________________________________
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # uic.loadUi(ui_path_main, self)
        self.buttons_window = ButtonsWindow()

        self._setup_multprocessing_shared_memory()
        self._setup_buttons_window()
        self._setup_main_window()
        self._setup_timers()
        # self.custom_window = CustomWindow()
        # self.custom_window.show()
        self.custom_window2 = CustomWindow2()
        self.custom_window2.show()
        self.recorder = lrec.Recorder()
        self.mymouse = mo_manager
        self.my_keyboard = kb_manager

        self.hwndMain = win32gui.FindWindow(None, target_app_name)  # set foreground window check

        # DRIVER VARIABLES
        self.health_time_last = 0
        self.flask_pointer = 2
        self.a = True
        self.healing_timeout = 0
        self.increment = 0
        self.stopwatch_running = False
        self.game_active = False
        self.game_active_last = False
        self.healing_hooked = False

        self.second = 0
        self.minute = 0
        self.hour = 0

    # _______________________________________ INIT SETUP _______________________________________
    def _setup_buttons_window(self):
        """SET BUTTONS WINDOW, create, connect signal and show it"""
        self.buttons_window.submitted.connect(self.on_button_clicked)
        self.buttons_window.move(600, 1100)
        self.buttons_window.show()

    def _setup_main_window(self):
        """# SET MAIN SCAN WINDOW, create, connect signal and show it"""
        # (x, y, w, h) = params["window_geo"]
        # self.move(x, y)
        # self.resize(w, h)
        # self.setAttribute(qtc.Qt.WA_TranslucentBackground, True)
        # self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.WindowTransparentForInput | qtc.Qt.Tool)
        # self.setWindowIcon(qtg.QIcon(icon_path))
        # self.setWindowTitle("POE Overlay")

        # GEOMETRY, STYLESHEETS
        # print(params["health_bar_css"])
        # self.label.setStyleSheet(params["health_bar_css"])
        # self.label.setGeometry(qtc.QRect(*params["health_bar_geo"]))
        # self.label2.setStyleSheet(params["stopwatch_css"])
        # self.label2.setGeometry(qtc.QRect(*params["stopwatch_geo"]))
        # self.label2.hide()
        # self.frame.setStyleSheet(params["frame_css"])
        # self.label.show()

        # self.show()

    def _setup_multprocessing_shared_memory(self):
        """setup_multprocessing_shared_memory"""
        (x, y, w, h) = params["window_geo"]
        self.mp_capture = mp.Array(c.c_ubyte, h * w * 4)
        self.capture = np.frombuffer(self.mp_capture.get_obj(), dtype=np.uint8).reshape((h, w, 4))
        self.mp_states = mp.Array(c.c_uint, 10)
        self.states = np.frombuffer(self.mp_states.get_obj(), dtype=np.uint)
        self.p = Process(target=bgt.capture_screen, args=(self.mp_capture, self.mp_states, [x, y, w, h]), daemon=True)
        self.states[0] = 1
        self.p.start()

    def _setup_timers(self):
        """setup_timers"""
        self.timer_10_msec = qtc.QTimer()
        self.timer_10_msec.timeout.connect(self.on_10_ms_timer)
        self.timer_10_msec.start(10)

        self.timer_1000_msec = qtc.QTimer()
        self.timer_1000_msec.timeout.connect(self.on_1000_ms_timer)
        self.timer_1000_msec.start(1000)
        self.timers = [self.timer_10_msec, self.timer_1000_msec]

    # _______________________________________ CALLBACKS _______________________________________
    def on_1000_ms_timer(self):
        """on_1000_ms_timer"""
        self.toggle_app_state_based_on_topmost_window()
        if self.stopwatch_running:
            self.update_stopwatch()

    def on_10_ms_timer(self):
        """on_10_ms_timer"""
        self.healing_timeout += 10
        self.heal_on_condition()

    @qtc.pyqtSlot(str)  # optional for type safety
    def on_button_clicked(self, string):
        """on_button_clicked - signal slot to buttons window"""

        self.bring_target_window_on_top()

        if string == "Hooked":
            self.buttons_window.pushButton_hooked.setStyleSheet(params["button_active"])
            self.buttons_window.pushButton_unhooked.setStyleSheet(params["button_inactive"])
            self.recorder.hook_all()
            self.mymouse.hook_all()
            self.my_keyboard.hook_all()

        elif string == "Unhooked":
            self.buttons_window.pushButton_hooked.setStyleSheet(params["button_inactive"])
            self.buttons_window.pushButton_unhooked.setStyleSheet(params["button_active"])
            self.recorder.unhook_all()
            self.mymouse.unhook_all()
            self.my_keyboard.unhook_all()

        elif string == "Start Record":
            self.buttons_window.pushButton_start_record.setStyleSheet(params["button_active"])
            self.recorder.start_recording()
            print("rec started")

        elif string == "Stop Record":
            self.buttons_window.pushButton_start_record.setStyleSheet(params["button_inactive"])
            self.recorder.stop_recording()
            print("rec stopped")

        elif string == "Play Record":
            self.recorder.play_recording()

        elif string == "Stopwatch":
            if not self.stopwatch_running:
                self.buttons_window.pushButton_stopwatch.setStyleSheet(params["button_active"])
                self.minute, self.second, self.hour = 0, 0, 0
                # self.label2.show()
                self.stopwatch_running = True
            else:
                self.buttons_window.pushButton_stopwatch.setStyleSheet(params["button_inactive"])
                self.stopwatch_running = False
                # self.label2.setText("")
                # self.label2.hide()

        elif string == "Close":
            self.buttons_window.close()
            self.recorder.unhook_all()
            self.mymouse.unhook_all()
            self.my_keyboard.unhook_all()
            for timer in self.timers:
                timer.stop()
            self.close()

        else:
            pass
        print(string)

    def bring_target_window_on_top(self):
        """brings target window app to the top"""
        try:
            keyboard.press("alt")
            if self.hwndMain == 0:
                self.hwndMain = win32gui.FindWindow(None, target_app_name)
            win32gui.SetForegroundWindow(self.hwndMain)
            keyboard.release("alt")
        except:
            keyboard.release("alt")

    # _______________________________________ METHODS _______________________________________

    def toggle_app_state_based_on_topmost_window(self):
        """hook, unhook all components, set visual state of button frame if target window is topmost or not"""
        self.game_active_last = self.game_active
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == target_app_name:
            self.game_active = True
        else:
            self.game_active = False
        if not self.game_active and self.game_active_last:
            self.buttons_window.pushButton_hooked.setStyleSheet(params["button_inactive"])
            self.buttons_window.pushButton_unhooked.setStyleSheet(params["button_active"])
            self.recorder.unhook_all()
            self.mymouse.unhook_all()
            self.my_keyboard.unhook_all()

        if self.game_active and not self.game_active_last:
            self.buttons_window.pushButton_hooked.setStyleSheet(params["button_active"])
            self.buttons_window.pushButton_unhooked.setStyleSheet(params["button_inactive"])
            self.recorder.hook_all()
            self.mymouse.hook_all()
            self.my_keyboard.hook_all()

    def heal_on_condition(self):
        """heal logic"""
        health_value = self.states[5]
        # self.label.setText(str(health_value))
        if health_value < 60 and health_value > 13 and self.game_active:
            if self.healing_timeout >= 500:  # 500 ms
                print(f"healing after {self.healing_timeout / 1000} s")
                keyboard.press("1")
                time.sleep(0.05)
                keyboard.release("1")
                self.healing_timeout = 0

    def update_stopwatch(self):
        """update_stopwatch"""
        if self.second < 59:
            self.second += 1
        else:
            if self.minute < 59:
                self.second = 0
                self.minute += 1
            elif self.minute == 59 and self.hour < 24:
                self.hour += 1
                self.minute = 0
                self.second = 0
            else:
                pass
        # self.label2.setText(f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}")
        return

    def close_windows(self):
        """close windows"""
        self.buttons_window.close()
        for timer in self.timers:
            timer.stop()
        self.p.kill()
        self.close()

    # _______________________________________ METHODS _______________________________________
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStyleFactory
import sys


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    w = MainWindow()
    # Set Fusion style globally
    app.setStyle(QStyleFactory.create("Fusion"))
    sys.exit(app.exec_())
