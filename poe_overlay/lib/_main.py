"""main logic module"""

import time
import ctypes as c
import multiprocessing as mp
from multiprocessing import Process

import win32gui  # type: ignore
import keyboard  # type: ignore
import numpy as np  # type: ignore

from PyQt5 import QtCore as qtc  # type: ignore
from PyQt5 import QtWidgets  # type: ignore

import pov_bg_process as bgp
from pov_mouse import MouseManager
from pov_keyboard import KeyboardManager
from pov_widgets import ButtonsWidget, FrameWidget


class Driver(QtWidgets.QWidget):
    """main window class invisible window on the whole monitor
    class has to inherit from QWidget, to be able to work with signals"""

    # _______________________________________ INIT _______________________________________
    def __init__(self, params):
        super().__init__()

        self.params = params

        self._setup_buttons_window()
        self._setup_multprocessing_shared_memory()
        self.setup_frames()
        self._setup_timers()

        self.mymouse = MouseManager(self.params["remap_mouse"].copy())
        self.my_keyboard = KeyboardManager(self.params["remap_keyboard"].copy())
        self.hwndMain = win32gui.FindWindow(None, self.params["paths"]["target_app_name"])  # set foreground window check

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
        self.reload_counter = 0

    # _______________________________________ INIT SETUP _______________________________________
    def _setup_buttons_window(self):
        """setup buttons frame connect signal and show"""
        self.buttons_window = ButtonsWidget(self.params)
        self.buttons_window.connect_buttons(self.on_button_window_button_clicked)
        self.buttons_window.connect_checkboxes(self.on_button_window_checkbox_state_changed)
        self.buttons_window.move(*self.params["frame_buttons"]["geometry"][0:2])

        self.buttons_window.show()

    def setup_frames(self):
        """setup various frames on screen"""
        self.frame_scan_area = FrameWidget(self.params["frame_scan"], self.params["frame_scan"], outer_frame=True)
        if self.buttons_window.checkBox_scan_area.isChecked():
            self.frame_scan_area.show()
        self.frame_health_bar = FrameWidget(self.params["frame_scan"], self.params["frame_health_bar"], outer_frame=False)
        if self.buttons_window.checkBox_health_bar.isChecked():
            self.frame_health_bar.show()
        self.frame_health_value = FrameWidget(self.params["frame_scan"], self.params["frame_health_value"], outer_frame=False)
        self.frame_health_value.label.setText("X")
        if self.buttons_window.checkBox_health_value.isChecked():
            self.frame_health_value.show()

    def _setup_multprocessing_shared_memory(self):
        """setup_multprocessing_shared_memory"""
        w, h = self.params["frame_scan"]["geometry"][2:]
        self.mp_capture = mp.Array(c.c_ubyte, h * w * 4)
        self.capture = np.frombuffer(self.mp_capture.get_obj(), dtype=np.uint8).reshape((h, w, 4))  # type: ignore
        self.mp_states = mp.Array(c.c_uint, 10)
        self.states = np.frombuffer(self.mp_states.get_obj(), dtype=np.uint)  # type: ignore
        self.p = Process(target=bgp.capture_screen, args=(self.mp_capture, self.mp_states, self.params["frame_scan"]["geometry"], self.params["frame_health_bar"]["geometry"]), daemon=True)
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

    def on_10_ms_timer(self):
        """on_10_ms_timer"""
        self.healing_timeout += 10
        self.heal_on_condition()

    def on_button_window_button_clicked(self):
        """callback method, react to buttons press on buttons frame"""
        string = self.sender().text()

        self.bring_target_window_on_top()

        if string == "Hooked":
            self.buttons_window.set_visual_style_hooked()
            self.mymouse.hook_all()
            self.my_keyboard.hook_all()

        elif string == "Unhooked":
            self.buttons_window.set_visual_style_unhooked()
            self.mymouse.unhook_all()
            self.my_keyboard.unhook_all()

        elif string == "Close":
            self.buttons_window.close()
            self.mymouse.unhook_all()
            self.my_keyboard.unhook_all()
            for timer in self.timers:
                timer.stop()
            self.close()

        print(string)

    def on_button_window_checkbox_state_changed(self):
        """callback method, react to checkbox press on buttons frame"""
        self.bring_target_window_on_top()

        name = self.sender().text()
        if name == "S":
            if self.sender().isChecked():
                self.frame_scan_area.show()
            else:
                self.frame_scan_area.hide()
        if name == "H":
            if self.sender().isChecked():
                self.frame_health_bar.show()
            else:
                self.frame_health_bar.hide()
        if name == "V":
            if self.sender().isChecked():
                self.frame_health_value.show()
            else:
                self.frame_health_value.hide()

    # _______________________________________ METHODS _______________________________________

    def bring_target_window_on_top(self):
        """brings target window app to the top"""
        try:
            keyboard.press("alt")
            if self.hwndMain == 0:
                self.hwndMain = win32gui.FindWindow(None, self.params["paths"]["target_app_name"])
            win32gui.SetForegroundWindow(self.hwndMain)
            keyboard.release("alt")
        except:
            keyboard.release("alt")

    def toggle_app_state_based_on_topmost_window(self):
        """hook, unhook all components, set visual state of button frame if target window is topmost or not"""
        self.game_active_last = self.game_active
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == self.params["paths"]["target_app_name"]:
            self.game_active = True
        else:
            self.game_active = False
        if not self.game_active and self.game_active_last:
            self.buttons_window.set_visual_style_unhooked()
            self.mymouse.unhook_all()
            self.my_keyboard.unhook_all()

        if self.game_active and not self.game_active_last:
            self.buttons_window.set_visual_style_hooked()
            self.mymouse.hook_all()
            self.my_keyboard.hook_all()

    def heal_on_condition(self):
        """heal logic"""
        health_value = self.states[5]
        self.frame_health_value.label.setText(str(health_value))
        if health_value < self.params["autoheal"]["low_lim"] and health_value > self.params["autoheal"]["high_lim"] and self.game_active:
            if self.healing_timeout >= self.params["autoheal"]["timeout"]:  # ms
                for key in self.params["autoheal"]["keys"]:
                    keyboard.press(key)
                    time.sleep(0.05)
                    keyboard.release("key")
                self.healing_timeout = 0

    def close_windows(self):
        """close windows"""
        self.buttons_window.close()
        for timer in self.timers:
            timer.stop()
        self.mymouse.unhook_all()
        self.my_keyboard.unhook_all()
        time.sleep(1)
        self.p.kill()
        self.close()
