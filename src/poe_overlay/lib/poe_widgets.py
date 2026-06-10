"""gui elements module"""

from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QToolButton, QPushButton, QComboBox, QLineEdit
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class WidgetParams:
    def __init__(self, widgets, name):       
        xs1, ys1, _, _ = widgets["frame_scan"]["geometry"]
        self.name   = name
        self.css    = widgets[name]["css"]
        self.x1    = widgets[name]["geometry"][0] 
        self.y1    = widgets[name]["geometry"][1] 
        self.x2    = widgets[name]["geometry"][2] 
        self.y2    = widgets[name]["geometry"][3] 
        self.w      = self.x2 - self.x1
        self.h      = self.y2 - self.y1
        self.region = (self.x1, self.y1, self.x2, self.y2) 
        self.regionwh = (self.x1, self.y1, self.w, self.h)  

        self.x1rel    = widgets[name]["geometry"][0] - xs1
        self.y1rel    = widgets[name]["geometry"][1] - ys1
        self.x2rel    = widgets[name]["geometry"][2] - xs1
        self.y2rel    = widgets[name]["geometry"][3] - ys1

        self.regionrel = (self.x1rel, self.y1rel, self.x2rel, self.y2rel) 
        self.regionwhrel = (self.x1rel, self.y1rel, self.w, self.h)  

        self.button_active = widgets[name].get("button_active", "")
        self.button_inactive = widgets[name].get("button_inactive", "") 
        self.validate()

    def validate(self):
        assert 0 <= self.x1 <= 1920 and self.x1 < self.x2, f"{self.name} x1 out of bounds"
        assert 0 <= self.x2 <= 1920 and self.x1 < self.x2, f"{self.name} x2 out of bounds"
        assert 0 <= self.y1 <= 1200 and self.y1 < self.y2, f"{self.name} y1 out of bounds"
        assert 0 <= self.y2 <= 1200 and self.y1 < self.y2, f"{self.name} y2 out of bounds"      

class WidgetsParams:
    def __init__(self, widget_params):
        self.active_profile_name = ""
        self.frame_scan         = WidgetParams(widget_params, "frame_scan")
        self.frame_buttons         = WidgetParams(widget_params, "frame_buttons")        
        self.frame_health_bar   = WidgetParams(widget_params, "frame_health_bar")
        self.frame_mana_value   = WidgetParams(widget_params, "frame_mana_value")
        self.frame_health_value = WidgetParams(widget_params, "frame_health_value")
        self.frame_mana_bar     = WidgetParams(widget_params, "frame_mana_bar")

class CustomUiLoader(QUiLoader):
            def createWidget(self, class_name, parent=None, name=""):
                # Pokud už widget s tímto jménem existuje (což je naše třída),
                # použijeme ji, místo abychom vytvářeli nové prázdné okno
                if parent is None and name:
                    return self.baseinstance
                return super().createWidget(class_name, parent, name)
            

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

        if ui_file.open(QFile.ReadOnly):  
            loader = CustomUiLoader()
            loader.baseinstance = self
            loader.load(ui_file) 
            ui_file.close()

        self.setWindowFlags(qtc.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(qtc.Qt.WindowType.FramelessWindowHint | qtc.Qt.WindowType.WindowStaysOnTopHint | qtc.Qt.WindowType.Tool)
        self.move(*self.settings.get("widget_buttons_position", [0, 0]))
        self.pushButton_toggle_checkboxes_visibility.clicked.connect(self._on_button_slider_clicked)
        self.checkboxes_hidden = True
        self.oldPos = None
        self.setStyleSheet(self.params.css)
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
        if isinstance(self.sender() , QToolButton):
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
        ui_file = QFile(f"{self.settings['base_dir']}/{self.settings['paths']['path_frame_recorder_ui']}")
        if ui_file.open(QFile.ReadOnly):  
            loader = CustomUiLoader()
            loader.baseinstance = self
            loader.load(ui_file) 
            ui_file.close()
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
