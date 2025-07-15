"""poe overlay tray module"""

import os
import sys
import subprocess

import toml

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QAction, QMenu, QApplication

from lib._main import Driver
from lib._params import params


class PoeOverlayTray(QSystemTrayIcon, QWidget):
    """poe overlay tray class"""

    def __init__(self):
        super().__init__()
        self.CONFIG_PATH = rf"{os.path.dirname(__file__)}\config.toml"
        self.params = self.read_config_toml()
        self.icon_running = QIcon(os.path.join(os.path.dirname(__file__),params["paths"]["path_icon_running"]))
        self.icon_stopped = QIcon(os.path.join(os.path.dirname(__file__),params["paths"]["path_icon_stopped"]))
        self.menu = QMenu()
        self.setContextMenu(self.menu)
        self.setIcon(self.icon_running)
        self.option_close = QAction("Close")
        self.menu.addAction(self.option_close)
        self.running = True
        self.setVisible(True)
        self.option_close.triggered.connect(self.on_close)
        self.activated.connect(self.on_tray_click)
        self.main = Driver(self.params)

        self.main.buttons_window.pushButton_reload.clicked.connect(self.on_buttons_window_reload_button_clicked)

    # _______________________________________ CALLBACKS _______________________________________

    def on_buttons_window_reload_button_clicked(self):
        """reload window"""
        subprocess.run(["notepad", self.CONFIG_PATH], check=False)
        self.params = self.read_config_toml()
        self.main.close_windows()
        self.main = Driver(self.params)
        self.main.buttons_window.pushButton_reload.clicked.connect(self.on_buttons_window_reload_button_clicked)

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
                self.main = Driver(self.params)

    def on_close(self):
        """close app"""
        self.main.close_windows()
        self.hide()
        sys.exit(0)

    # _______________________________________ METHODS _______________________________________

    def read_config_toml(self):
        """load config"""
        with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
            config = toml.load(f)
            return config


if __name__ == "__main__":
    app = QApplication([])
    tray_app_trade_whisper = PoeOverlayTray()
    app.setStyle("fusion")
    app.exec()
