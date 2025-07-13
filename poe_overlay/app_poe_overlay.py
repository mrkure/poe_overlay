"""poe overlay tray module"""

import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QAction, QMenu, QApplication

from lib._main import Driver
from lib._params import params


class PoeOverlayTray(QSystemTrayIcon, QWidget):
    """poe overlay tray class"""
    def __init__(self):
        super().__init__()

        self.icon_running = QIcon(params["path_icon_running"])
        self.icon_stopped = QIcon(params["path_icon_stopped"])
        self.menu = QMenu()
        self.setContextMenu(self.menu)
        self.setIcon(self.icon_running)
        self.option_close = QAction("Close")
        self.menu.addAction(self.option_close)
        self.running = True
        self.setVisible(True)
        self.option_close.triggered.connect(self.on_close)
        self.activated.connect(self.on_click)

        self.main = Driver()

    # _______________________________________ CALLBACKS _______________________________________

    def on_click(self, button):
        """close or create main window app"""
        if str(button) == "3":  # left button
            if self.running:
                self.setIcon(self.icon_stopped)
                self.running = False
                self.main.close_windows()

            elif not self.running:
                self.setIcon(self.icon_running)
                self.running = True
                self.main = Driver()

    def on_close(self):
        """close app"""
        self.main.close_windows()
        self.hide()
        sys.exit(0)


if __name__ == "__main__":
    app = QApplication([])
    tray_app_trade_whisper = PoeOverlayTray()
    app.setStyle("fusion")
    app.exec()
