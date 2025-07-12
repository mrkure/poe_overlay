# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 16:03:13 2022

@author: mrkure
"""

# from mklib.lib_io import mkIO
# mkIO.activate_env(1, 'work', __file__,1)
import os, sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QAction, QMenu, QApplication
import lib._main_exe as me
# from mk_css import dic_css

class TrayAppTradeWhisper(QSystemTrayIcon, QWidget):
    def __init__(self):
        super(QSystemTrayIcon, self).__init__()
        super(QWidget, self).__init__()


        self.icon_running = QIcon(rf"{os.path.dirname(__file__)}\res\running.png")
        self.icon_stopped = QIcon(rf"{os.path.dirname(__file__)}\res\stopped.png")
        # self.setStyleSheet(dic_css['gray'])
        self.menu = QMenu()
        self.setContextMenu(self.menu)
        self.setIcon(self.icon_running)
        self.option_close = QAction("Close")
        self.menu.addAction(self.option_close)
        self.running = True
        self.setVisible(True)

        # %% TRAY SIGNALS
        self.option_close.triggered.connect(self.on_close)
        self.activated.connect(self.on_click)

        # %% MAIN WINDOW
        self.create_main_window()

    def create_main_window(self):
        self.main = me.MainWindow()
        # self.main.showMaximized()

    # %% CALLBACKS

    # close or create main window app
    def on_click(self, button):
        # if left button clicked
        if str(button) == "3":
            if self.running:
                self.setIcon(self.icon_stopped)
                self.running = False
                self.main.close_windows()

            elif not self.running:
                self.setIcon(self.icon_running)
                self.running = True
                self.main = me.MainWindow()
                # self.main.showMaximized()

    # close tray app
    def on_close(self):
        self.main.close_windows()
        self.hide()
        sys.exit(0)


# %% MAIN
if __name__ == "__main__":
    app = QApplication([])
    tray_app_trade_whisper = TrayAppTradeWhisper()
    app.setStyle("fusion")
    app.exec()
