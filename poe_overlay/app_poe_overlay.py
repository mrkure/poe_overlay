"""poe overlay tray module"""

import os
import sys
import subprocess

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QAction, QMenu, QApplication

from lib._main import Driver
import lib.pov_tools as tools

SELF_DIR_PATH = os.path.dirname(__file__)
SETTINGS_PATH = rf"{os.path.dirname(__file__)}\res\_settings.toml"

class PoeOverlayTray(QSystemTrayIcon, QWidget):
    """poe overlay tray class"""

    def __init__(self):
        super().__init__()
        self.settings = tools.read_config_toml(SETTINGS_PATH)
        self.settings["base_dir"] = SELF_DIR_PATH
        self.icon_running = QIcon(self.settings["paths"]["path_icon_running"])
        self.icon_stopped = QIcon(self.settings["paths"]["path_icon_stopped"])
        self.menu = QMenu()
        self.setContextMenu(self.menu)
        self.setIcon(self.icon_running)
        self.option_close = QAction("Close")
        self.menu.addAction(self.option_close)
        self.option_close.triggered.connect(self.on_close)
        self.activated.connect(self.on_tray_click)
        self.running = True
        self.setVisible(True)
        self.setup_windows()

    # _______________________________________ CALLBACKS _______________________________________
    def on_combobox_profile_index_change(self):
        """on_combobox_profile_index_change -> reload windows"""
        self.settings["active_profile_name"] = self.main.buttons_window.comboBox_profile.currentText()
        tools.write_configs_toml(SETTINGS_PATH, self.settings)
        self.setup_windows()

    def on_buttons_window_reload_button_clicked(self):
        """on_buttons_window_reload_button_clicked"""
        self.setup_windows()

    def on_recorder_widget_line_edit_save_enter_pressed(self):
        """on_recorder_widget_line_edit_save_enter_pressed -> save recording"""
        if len(self.main.recorder_widget.lineEdit_save.text().split("-")) == 2:
            self.main.recorder.save(self.main.recorder_widget)
            self.main.recorder_widget.hide()
            self.setup_windows()
        else:
            print("Cannot save, wrong name format")

    def on_buttons_window_edit_button_clicked(self):
        """reload window"""
        path = rf"{SELF_DIR_PATH}/{self.settings['paths']['path_profiles']}/{self.settings['active_profile_name']}/profile.py"
        subprocess.run(["code", path], check=False, shell=True)

        self.setup_windows()

    def on_buttons_window_close_button_clicked(self):
        """on_buttons_window_close_button_clicked"""
        tools.write_configs_toml(SETTINGS_PATH, self.settings)
        self.main.close_windows()

    def on_tray_click(self, button):
        """close or create main window app"""
        if str(button) == "3":  # left button
            if self.running:
                self.setIcon(self.icon_stopped)
                self.running = False
                self.main.close_windows()

            elif not self.running:
                self.setIcon(self.icon_running)
                self.running = True
                self.main = Driver(self.settings)

    def on_close(self):
        """close app"""
        self.main.close_windows()
        self.hide()
        sys.exit(0)

    # _______________________________________ METHODS _______________________________________

    def setup_windows(self):
        """reactivate windows"""
        tools.write_configs_toml(SETTINGS_PATH, self.settings)

        try:
            self.main.close_windows()
        except:
            pass
        self.main = Driver(self.settings)
        self.main.buttons_window.pushButton_close.clicked.connect(self.on_buttons_window_close_button_clicked)
        self.main.buttons_window.pushButton_edit.clicked.connect(self.on_buttons_window_edit_button_clicked)
        self.main.buttons_window.pushButton_reload.clicked.connect(self.on_buttons_window_reload_button_clicked)
        self.main.buttons_window.comboBox_profile.currentIndexChanged.connect(self.on_combobox_profile_index_change)
        self.main.recorder_widget.lineEdit_save.returnPressed.connect(self.on_recorder_widget_line_edit_save_enter_pressed)
        # self.main.recorder.on_saved(self.pprint)

        
    def load_settings(self):
        """load_settings"""
        tools.read_config_toml(SETTINGS_PATH)

if __name__ == "__main__":
    app = QApplication([])
    tray_app_trade_whisper = PoeOverlayTray()
    app.setStyle("fusion")
    app.exec()
