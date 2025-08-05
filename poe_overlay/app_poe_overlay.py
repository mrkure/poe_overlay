"""poe overlay tray module"""

import os
import sys
import subprocess
from pathlib import Path
import toml

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QAction, QMenu, QApplication

from lib._main import Driver
from lib._params import params


class PoeOverlayTray(QSystemTrayIcon, QWidget):
    """poe overlay tray class"""

    def __init__(self):
        super().__init__()
        self.icon_running = QIcon(params["paths"]["path_icon_running"])
        self.icon_stopped = QIcon(params["paths"]["path_icon_stopped"])
        self.menu = QMenu()
        self.setContextMenu(self.menu)
        self.setIcon(self.icon_running)
        self.option_close = QAction("Close")
        self.menu.addAction(self.option_close)
        self.option_close.triggered.connect(self.on_close)
        self.activated.connect(self.on_tray_click)
        self.running = True
        self.setVisible(True)
        self.configs = {}
        self.CONFIG_PATH = rf"{os.path.dirname(__file__)}"
        self.setup_windows()

    # _______________________________________ CALLBACKS _______________________________________
    def on_combobox_profile_index_change(self):
        """on_combobox_profile_index_change -> reload windows"""
        path = self.main.buttons_window.comboBox_profile.itemData(self.main.buttons_window.comboBox_profile.currentIndex())
        for _, value in self.configs.items():
            value["active"] = False
        self.configs[path]["active"] = True
        self.write_configs_toml()
        self.setup_windows()

    def on_recorder_widget_line_edit_save_enter_pressed(self):
        """on_recorder_widget_line_edit_save_enter_pressed -> save recording"""
        text = self.main.recorder_widget.lineEdit_save.text()
        if len(text.split("-")) == 3:
            self.main.recorder.save(f"{text}.json")
            self.main.recorder_widget.hide()
            self.setup_windows()
        else :
            print("Cannot save, wrong name format")
            self.main.recorder_widget.hide()
    def on_buttons_window_edit_button_clicked(self):
        """reload window"""
        key = None
        for key, value in self.configs.items():
            if value["active"]:
                break
        if key:
            subprocess.run(["notepad", key], check=False)
            self.read_configs_toml()
            self.setup_windows()

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
                self.main = Driver(self.configs)

    def on_close(self):
        """close app"""
        self.main.close_windows()
        self.hide()
        sys.exit(0)

    # _______________________________________ METHODS _______________________________________

    def setup_windows(self):
        """reactivate windows"""
        try:
            self.main.close_windows()
        except:
            pass
        self.read_configs_toml()
        self.main = Driver(self.configs)
        self.main.buttons_window.pushButton_edit.clicked.connect(self.on_buttons_window_edit_button_clicked)
        self.main.buttons_window.comboBox_profile.currentIndexChanged.connect(self.on_combobox_profile_index_change)
        self.main.recorder_widget.lineEdit_save.returnPressed.connect(self.on_recorder_widget_line_edit_save_enter_pressed)
        # self.main.recorder.on_saved(self.pprint)

    def read_configs_toml(self):
        """load config"""
        toml_files = [str(f) for f in Path(self.CONFIG_PATH).glob("*.toml")]
        for file in toml_files:
            with open(file, "r", encoding="utf-8") as f:
                self.configs[file] = toml.load(f)

    def write_configs_toml(self):
        """writes path to currently active toml config"""

        def remove_keys_recursive(obj, keys_to_remove):
            if isinstance(obj, dict):
                return {k: remove_keys_recursive(v, keys_to_remove) for k, v in obj.items() if k not in keys_to_remove}
            elif isinstance(obj, list):
                return [remove_keys_recursive(item, keys_to_remove) for item in obj]
            else:
                return obj

        for key, value in self.configs.items():
            config = remove_keys_recursive(value, ["function", "id", "flasks_pointer", "running"])
            with open(key, "w", encoding="utf-8") as f:
                toml.dump(config, f)


if __name__ == "__main__":
    app = QApplication([])
    tray_app_trade_whisper = PoeOverlayTray()
    app.setStyle("fusion")
    app.exec()
