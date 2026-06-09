"""gui elements module"""

import os
from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QToolButton, QPushButton, QCheckBox, QComboBox, QLineEdit, QWidget
from PySide6 import QtCore as qtc  # type: ignore
from PySide6 import QtWidgets  # type: ignore
from PySide6.QtWidgets import QApplication  # Import klidně přímo sem, pokud není nahoře
from PySide6.QtUiTools import QUiLoader  # <--- Tohle nahrazuje uic
from PySide6.QtCore import QFile, QIODevice
from poe_overlay.profiles.anim_weapon.profile import WidgetParams



class ButtonsWidget(QtWidgets.QWidget):
    """buttons window"""
    pushButton_toggle_checkboxes_visibility: QPushButton
    pushButton_close: QPushButton
    pushButton_edit: QPushButton
    pushButton_reload: QPushButton

    pushButton_hooked: QPushButton
    pushButton_unhooked: QPushButton
    toolButton_scan_area: QToolButton
    toolButton_health_bar: QToolButton
    toolButton_health_value: QToolButton
    toolButton_mana_bar: QToolButton
    toolButton_mana_value: QToolButton    
    comboBox_profile: QComboBox
    def __init__(self, params: WidgetParams, settings):
        super().__init__()
        self.params = params
        self.settings = settings
  
        ui_file = QFile(f"{self.settings['base_dir']}/{self.settings['paths']['path_frame_buttons_ui']}")
        if ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            loader = QUiLoader()
            self.ui = loader.load(ui_file, self)
            ui_file.close()

            # TRIK: Vezmeme všechny děti z načteného UI a namontujeme je přímo na self
        for widget in self.ui.findChildren(QWidget):
            if widget.objectName():
                setattr(self, widget.objectName(), widget)

        # self.setWindowFlags(qtc.Qt.WindowType.WindowStaysOnTopHint)
        # self.setWindowFlags(qtc.Qt.WindowType.FramelessWindowHint | qtc.Qt.WindowType.WindowStaysOnTopHint | qtc.Qt.WindowType.Tool)
        self.move(*self.settings.get("widget_buttons_position", [0, 0]))
        # self.pushButton_toggle_checkboxes_visibility.clicked.connect(self._on_button_slider_clicked)
        # self.checkboxes_hidden = True
        self.oldPos = None
        NORMAL = "green"
        css = f"QWidget{{background-color: {NORMAL};}} QComboBox,QPushButton{{background-color: {NORMAL};font: 10pt 'MS Shell Dlg 2';}}"
        self.setStyleSheet(css)
        self._init_checkbox_states()
        self.adjustSize()

    def _init_checkbox_states(self):
        """_init_checkbox_states: set states of checkboxes based on settings"""
        for widget in self.children():
            if isinstance(widget, QToolButton):
                widget.setChecked(self.settings["checkboxes"][widget.text()])
                widget.hide()

    def _on_button_slider_clicked(self):
        print("clicked")
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
        if isinstance(self.sender , QCheckBox):
            self.settings["checkboxes"][self.sender.text()] = self.sender.isChecked()

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
        self.pushButton_hooked.setStyleSheet(self.params.button_active)
        self.pushButton_unhooked.setStyleSheet(self.params.button_inactive)

    def set_visual_style_unhooked(self):
        """set hooked visual state of hooked and unhooked buttons"""
        self.pushButton_hooked.setStyleSheet(self.params.button_inactive)
        self.pushButton_unhooked.setStyleSheet(self.params.button_active)

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

    def __init__(self, params: WidgetParams):
        super().__init__()
        self.setWindowFlags(qtc.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(qtc.Qt.WindowType.FramelessWindowHint | qtc.Qt.WindowType.WindowStaysOnTopHint | qtc.Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(qtc.QRect(*params.regionwh))
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(0, 0, params.w, params.h)
        self.label.setStyleSheet(params.css)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)


class RecorderWidget(QtWidgets.QFrame):
    """save window"""
    lineEdit_save: QLineEdit

    def __init__(self, params, settings):
        super().__init__()
        self.settings = settings
        self.params = params
# ui_file = QFile(f"{self.settings['base_dir']}/{self.settings['paths']['path_frame_buttons_ui']}")
        ui_file = QFile(f"{self.settings['base_dir']}/{self.settings['paths']['path_frame_recorder_ui']}")
        if ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            loader = QUiLoader()
            self.ui = loader.load(ui_file, self)
            ui_file.close()
        for widget in self.ui.findChildren(QWidget):
            if widget.objectName():
                setattr(self, widget.objectName(), widget)
        self.setWindowFlags(qtc.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(qtc.Qt.WindowType.FramelessWindowHint | qtc.Qt.WindowType.WindowStaysOnTopHint | qtc.Qt.WindowType.Tool)
        self.center()

    def center(self):
        """center widget"""
        frame_geometry = self.frameGeometry()
        screen = QApplication.primaryScreen()
        if screen:
            screen_center = screen.availableGeometry().center()
            frame_geometry.moveCenter(screen_center)
            self.move(frame_geometry.topLeft())
