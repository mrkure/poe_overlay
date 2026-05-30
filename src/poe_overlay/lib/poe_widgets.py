"""gui elements module"""

import os
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QToolButton, QPushButton, QDesktopWidget
from PyQt5 import QtCore as qtc  # type: ignore
from PyQt5 import QtWidgets, uic  # type: ignore


class ButtonsWidget(QtWidgets.QWidget):
    """buttons window"""

    def __init__(self, profile, settings):
        super().__init__()
        self.profile = profile
        self.settings = settings
        uic.loadUi(f"{self.settings['base_dir']}/{self.settings['paths']['path_frame_buttons_ui']}", self)
        self.setWindowFlags(qtc.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.Tool)
        self.move(*self.settings.get("widget_buttons_position", [0, 0]))
        self.pushButton_toggle_checkboxes_visibility.clicked.connect(self._on_button_slider_clicked)
        self.checkboxes_hidden = True
        self.oldPos = None
        self.setStyleSheet(self.profile["frame_buttons"]["css"])
        self._init_checkbox_states()
        self.adjustSize()

    def _init_checkbox_states(self):
        """_init_checkbox_states: set states of checkboxes based on settings"""
        for widget in self.children():
            if isinstance(widget, QToolButton):
                widget.setChecked(self.settings["checkboxes"][widget.text()])
                widget.hide()

    def _on_button_slider_clicked(self):
        for widget in self.children():
            if isinstance(widget, QToolButton):
                if self.checkboxes_hidden:
                    widget.show()
                else:
                    widget.hide()
        self.adjustSize()
        self.checkboxes_hidden = not self.checkboxes_hidden

    def _on_checkbox_clicked(self):
        """on_checkbox_clicked: write state to settings"""
        if "checkboxes" not in self.settings:
            self.settings["checkboxes"] = {}
        self.settings["checkboxes"][self.sender().text()] = self.sender().isChecked()

    def connect_buttons(self, function):
        """connect_buttons"""
        for widget in self.children():
            if isinstance(widget, QPushButton):
                widget.clicked.connect(function)

    def connect_toolbuttons(self, function):
        """connect_checkboxes"""
        for widget in self.children():
            if isinstance(widget, QToolButton):
                widget.clicked.connect(function)
                widget.clicked.connect(self._on_checkbox_clicked)

    def set_visual_style_hooked(self):
        """set hooked visual state of hooked and unhooked buttons"""
        self.pushButton_hooked.setStyleSheet(self.profile["frame_buttons"]["button_active"])
        self.pushButton_unhooked.setStyleSheet(self.profile["frame_buttons"]["button_inactive"])

    def set_visual_style_unhooked(self):
        """set hooked visual state of hooked and unhooked buttons"""
        self.pushButton_hooked.setStyleSheet(self.profile["frame_buttons"]["button_inactive"])
        self.pushButton_unhooked.setStyleSheet(self.profile["frame_buttons"]["button_active"])

    def mousePressEvent(self, evt):
        """press event to move app

        Args:
            evt (_type_): event
        """
        self.oldPos = evt.globalPos()

    def mouseMoveEvent(self, evt):
        """move event to move app

        Args:
            evt (_type_): event
        """
        if self.underMouse():
            delta = QPoint(evt.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = evt.globalPos()
            self.settings["widget_buttons_position"] = [self.pos().x(), self.pos().y()]


class FrameWidget(QtWidgets.QWidget):
    """frame widget to display various frames on screen"""

    def __init__(self, frame_scan, frame, outer_frame):
        super().__init__()
        self.setWindowFlags(qtc.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.Tool)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)

        x, y, w, h = frame_scan["geometry"]
        xl, yl, wl, hl = frame["geometry"]
        css = frame["css"]
        if outer_frame:
            xl, yl, wl, hl = 0, 0, w, h
            css = frame_scan["css"]

        self.setGeometry(qtc.QRect(x + xl, y + yl, wl, hl))  # x, y, width, height
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(0, 0, wl, hl)
        self.label.setStyleSheet(css)
        self.label.setAlignment(Qt.AlignCenter)


class RecorderWidget(QtWidgets.QFrame):
    """save window"""

    def __init__(self, params):
        super().__init__()
        self.params = params
        # print((os.path.join(os.path.dirname(os.path.dirname(__file__))), params["paths"]["path_frame_buttons_ui"])
        uic.loadUi(os.path.join(os.path.dirname(os.path.dirname(__file__)), params["paths"]["path_frame_recorder_ui"]), self)
        self.setWindowFlags(qtc.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.Tool)
        self.center()
        # self.line_edit_save.returnPressed.connect(self.on_enter_pressed)
        # self.show()

    def center(self):
        """center widget"""
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
