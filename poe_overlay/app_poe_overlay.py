"""poe overlay tray module"""

import os
import sys
import subprocess

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QAction, QMenu, QApplication

from lib._main import Driver
import lib.poe_tools as tools

SELF_DIR_PATH = os.path.dirname(__file__)
SETTINGS_PATH = rf"{os.path.dirname(__file__)}\res\_settings.toml"


class PoeOverlayTray(QSystemTrayIcon, QWidget):
    """poe overlay tray class"""

    def __init__(self):
        super().__init__()
        self.settings = tools.load_settings_toml(SETTINGS_PATH, SELF_DIR_PATH)
        self._init_tray()
        self._init_driver()

    # _______________________________________ METHODS _______________________________________

    def _init_tray(self):
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

    def _init_driver(self):
        self.driver = Driver(self.settings)
        self.driver.buttons_window.pushButton_close.clicked.connect(self.on_buttons_window_close_button_clicked)
        self.driver.buttons_window.pushButton_edit.clicked.connect(self.on_buttons_window_edit_button_clicked)
        self.driver.buttons_window.pushButton_reload.clicked.connect(self.on_buttons_window_reload_button_clicked)
        self.driver.buttons_window.comboBox_profile.currentIndexChanged.connect(self.on_combobox_profile_change)
        self.driver.recorder_widget.lineEdit_save.returnPressed.connect(self.on_recorder_widget_line_edit_save_enter_pressed)

    def _reload_driver(self):
        tools.write_settings_toml(SETTINGS_PATH, self.settings)
        self.driver.close_windows()
        self._init_driver()

    # _______________________________________ CALLBACKS _______________________________________
    def on_combobox_profile_change(self):
        """on_combobox_profile_index_change -> reload windows"""
        self.settings["active_profile_name"] = self.driver.buttons_window.comboBox_profile.currentText()
        tools.write_settings_toml(SETTINGS_PATH, self.settings)
        self._reload_driver()

    def on_buttons_window_reload_button_clicked(self):
        """on_buttons_window_reload_button_clicked"""
        self._reload_driver()

    def on_recorder_widget_line_edit_save_enter_pressed(self):
        """on_recorder_widget_line_edit_save_enter_pressed -> save recording"""
        if len(self.driver.recorder_widget.lineEdit_save.text().split("-")) == 2:
            self.driver.recorder.save(self.driver.recorder_widget)
            self.driver.recorder_widget.hide()
            self._reload_driver()
        else:
            print("Cannot save, wrong name format")

    def on_buttons_window_edit_button_clicked(self):
        """reload window"""
        path = rf"{SELF_DIR_PATH}/{self.settings['paths']['path_profiles']}/{self.settings['active_profile_name']}/profile.py"
        self.driver.unhook_all()
        subprocess.run(f'code --wait "{path}"', check=False, shell=True)
        self._reload_driver()

    def on_buttons_window_close_button_clicked(self):
        """on_buttons_window_close_button_clicked"""
        tools.write_settings_toml(SETTINGS_PATH, self.settings)
        self.driver.close_windows()

    def on_tray_click(self, button):
        """close or create main window app"""
        if str(button) == "3":  # left button
            if self.running:
                self.setIcon(self.icon_stopped)
                self.running = False
                self.driver.close_windows()

            elif not self.running:
                self.setIcon(self.icon_running)
                self.running = True
                self.driver = Driver(self.settings)

    def on_close(self):
        """close app"""
        self.driver.close_windows()
        self.hide()
        sys.exit(0)


if __name__ == "__main__":
    app = QApplication([])
    tray_app_trade_whisper = PoeOverlayTray()
    app.setStyle("fusion")
    app.exec()
