"""main logic module"""

import os
import ctypes as c
import multiprocessing as mp
from multiprocessing import Process
from pathlib import Path

import win32gui  # type: ignore
import keyboard  # type: ignore
import numpy as np  # type: ignore

from PySide6 import QtCore as qtc  # type: ignore
from PySide6 import QtWidgets  # type: ignore
from PySide6.QtWidgets import QApplication

import poe_tools as tools
import poe_bg_process as bgp
from poe_mouse import MouseManager
from poe_keyboard import KeyboardManager
from poe_widgets import ButtonsWidget, FrameWidget, RecorderWidget
from poe_recorder import Recorder


class Driver(QtWidgets.QWidget):
    """main window class invisible window on the whole monitor
    class has to inherit from QWidget, to be able to work with signals"""

    # _______________________________________ INIT _______________________________________
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.ImportedModule = tools.load_profile_module(self.settings)
        self.params = self.ImportedModule.params
        self.params["active_profile_name"] = settings["active_profile_name"]

        self._init_buttons_widget()
        self._init_recorder_widget()
        self._init_frames_widgets()
        self._init_multiprocessing_shared_memory()
        self._init_timers()
        self._init_rec_mouse_keyboard()

        self.hwndMain = win32gui.FindWindow(None, self.settings["target_app_name"])  # set foreground window check

        # DRIVER VARIABLES
        self.game_active = False
        self.game_active_last = False

    # _______________________________________ INIT  _______________________________________
    def _init_buttons_widget(self):
        """setup buttons frame connect signal and show"""
        self.buttons_window = ButtonsWidget(self.params, self.settings)
        self.buttons_window.connect_buttons(self.on_button_window_button_clicked)
        self.buttons_window.connect_toolbuttons(self.on_button_window_toolbutton_state_changed)
        # self.buttons_window.move(*self.params["frame_buttons"]["geometry"][0:2])

        base_dir = Path(f"{self.settings['base_dir']}/{self.settings['paths']['path_profiles']}")
        dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name != "all"]

        for item in dirs:
            self.buttons_window.comboBox_profile.addItem(os.path.basename(item), userData=item)
            self.buttons_window.comboBox_profile.setCurrentIndex(self.buttons_window.comboBox_profile.findText(self.settings["active_profile_name"]))

        self.buttons_window.show()

    def _init_recorder_widget(self):
        self.recorder_widget = RecorderWidget(self.params)

    def _init_frames_widgets(self):
        """setup various frames on screen"""
        self.frame_scan_area = FrameWidget(self.params["frame_scan"], self.params["frame_scan"], outer_frame=True)
        if self.buttons_window.toolButton_scan_area.isChecked():
            self.frame_scan_area.show()
        self.frame_health_bar = FrameWidget(self.params["frame_scan"], self.params["frame_health_bar"], outer_frame=False)
        if self.buttons_window.toolButton_health_bar.isChecked():
            self.frame_health_bar.show()
        self.frame_health_value = FrameWidget(self.params["frame_scan"], self.params["frame_health_value"], outer_frame=False)
        if self.buttons_window.toolButton_health_value.isChecked():
            self.frame_health_value.show()

        self.frame_mana_bar = FrameWidget(self.params["frame_scan"], self.params["frame_mana_bar"], outer_frame=False)
        if self.buttons_window.toolButton_mana_bar.isChecked():
            self.frame_mana_bar.show()
        self.frame_mana_value = FrameWidget(self.params["frame_scan"], self.params["frame_mana_value"], outer_frame=False)
        if self.buttons_window.toolButton_mana_value.isChecked():
            self.frame_mana_value.show()

    def _init_multiprocessing_shared_memory(self):
        """setup_multprocessing_shared_memory"""
        w, h = self.params["frame_scan"]["geometry"][2:]
        self.mp_capture = mp.Array(c.c_ubyte, h * w * 4)
        self.capture = np.frombuffer(self.mp_capture.get_obj(), dtype=np.uint8).reshape((h, w, 4))  # type: ignore
        self.mp_states = mp.Array(c.c_uint, 10)
        self.states = np.frombuffer(self.mp_states.get_obj(), dtype=np.uint32)  # type: ignore
        self.p = Process(target=bgp.capture_screen, args=(self.mp_capture, self.mp_states, self.params), daemon=True)
        self.states[0] = 1
        self.p.start()

    def _init_timers(self):
        """setup_timers"""
        self.timer_10_msec = qtc.QTimer()
        self.timer_10_msec.timeout.connect(self.on_10_ms_timer)
        self.timer_10_msec.start(10)

        self.timer_1000_msec = qtc.QTimer()
        self.timer_1000_msec.timeout.connect(self.on_1000_ms_timer)
        self.timer_1000_msec.start(1000)
        self.timers = [self.timer_10_msec, self.timer_1000_msec]

    def _init_rec_mouse_keyboard(self):
        """_init_rec_mouse_keyboard"""
        # recorder
        self.recorder = Recorder(self.settings)
        self.recorder.set_recording_end_callback(self.recorder_widget.show)
        self.recorder.read_records_json()
        # mouse
        self.mymouse = MouseManager(self.ImportedModule.MouseWorkers)
        # keyboard
        self.my_keyboard = KeyboardManager(self.ImportedModule.KeyboardWorkers)

    # _______________________________________ CALLBACKS _______________________________________
    def on_1000_ms_timer(self):
        """on_1000_ms_timer"""
        self.toggle_app_state_based_on_topmost_window()

    def on_10_ms_timer(self):
        """on_10_ms_timer"""
        self.ImportedModule.AutomationWorkers.autoheal(self.frame_health_value, self.states[5], self.game_active)
        self.ImportedModule.AutomationWorkers.automana(self.frame_mana_value, self.states[6], self.game_active)

    def on_button_window_button_clicked(self):
        """callback method, react to buttons press on buttons frame"""
        string = self.sender().text()

        self.bring_target_window_on_top()

        if string == "Hooked":
            self.hook_all()

        elif string == "Unhooked":
            self.unhook_all()

        elif string == "Record":
            self.buttons_window.set_visual_style_unhooked()
            QApplication.processEvents()
            self.my_keyboard.unhook_all()
            self.mymouse.unhook_all()
            self.recorder.unhook_all()
            self.ImportedModule.AutomationWorkers.unhook_all()
            self.recorder.record()

        elif string == "X":
            self.buttons_window.close()
            self.unhook_all()
            for timer in self.timers:
                timer.stop()
            self.close()

    def on_button_window_toolbutton_state_changed(self):
        """callback method, react to toolbutton press on buttons frame"""
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
        if name == "Hv":
            if self.sender().isChecked():
                self.frame_health_value.show()
            else:
                self.frame_health_value.hide()
        if name == "M":
            if self.sender().isChecked():
                self.frame_mana_bar.show()
            else:
                self.frame_mana_bar.hide()
        if name == "Mv":
            if self.sender().isChecked():
                self.frame_mana_value.show()
            else:
                self.frame_mana_value.hide()

    # _______________________________________ METHODS _______________________________________

    def bring_target_window_on_top(self):
        """brings target window app to the top"""
        try:
            keyboard.press("alt")
            if self.hwndMain == 0:
                self.hwndMain = win32gui.FindWindow(None, self.settings["target_app_name"])
            win32gui.SetForegroundWindow(self.hwndMain)
            keyboard.release("alt")
        except:
            keyboard.release("alt")

    def toggle_app_state_based_on_topmost_window(self):
        """hook, unhook all components, set visual state of button frame if target window is topmost or not"""
        self.game_active_last = self.game_active
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == self.settings["target_app_name"]:
            self.game_active = True
        else:
            self.game_active = False
        if not self.game_active and self.game_active_last:
            self.unhook_all()

        if self.game_active and not self.game_active_last:
            self.hook_all()

    def hook_all(self):
        """hook_all"""
        [print() for i in range(30)]
        self.buttons_window.set_visual_style_hooked()
        QApplication.processEvents()
        self.mymouse.hook_all()
        self.my_keyboard.hook_all()
        self.recorder.hook_all()
        self.ImportedModule.AutomationWorkers.hook_all()

    def unhook_all(self):
        """unhook_all"""
        self.buttons_window.set_visual_style_unhooked()
        QApplication.processEvents()
        self.mymouse.unhook_all()
        self.my_keyboard.unhook_all()
        self.recorder.unhook_all()
        self.ImportedModule.AutomationWorkers.unhook_all()

    def close_windows(self):
        """close windows"""
        self.buttons_window.close()
        for timer in self.timers:
            timer.stop()
        self.unhook_all()
        self.p.kill()
        self.close()

