"""params module"""

import os

LIGHT  = "rgb(200, 200, 200)"
NORMAL = "rgb(150, 150, 150)"
DARK   = "rgb(100, 100, 100)"

params = {
    "use_aura_buffs_sequence"        : "f1",
    "fast_click_left_with_ctrl_down" : "f4",
    "fast_click_left_with_shift_down": "f5",
    "use_portal_scroll"              : "`",
    "caps lock"                      : "6",

    "path_frame_buttons_ui": rf"{os.path.dirname(os.path.dirname(__file__))}\res\frame_buttons.ui",
    "path_icon_running"    : rf"{os.path.dirname(os.path.dirname(__file__))}\res\running.png",
    "path_icon_stopped"    : rf"{os.path.dirname(os.path.dirname(__file__))}\res\stopped.png",

    "frame_scan"        : {"geometry": [5, 29, 1910, 1120], "css": "QLabel {background-color: transparent;border: 2px solid red;color: white;font-size: 14px;}"},
    "frame_health_bar"  : {"geometry": [105, 910, 15, 180], "css": "QLabel {background-color: transparent;border: 2px solid red;color: white;font-size: 14px;}"},
    "frame_health_value": {"geometry": [240, 910, 70, 70], "css": "QLabel {background-color: rgba(14, 255, 255, 210);color: white;font: 18 24pt 'MS Shell Dlg 2';}"},
    "frame_stop_watch"  : {"geometry": [340, 950, 80, 30], "css": "QLabel {background-color: rgba(14, 255, 255, 210);color: white;font: 18 24pt 'MS Shell Dlg 2';}"},
    "frame_buttons"     : {"geometry":[600,1100, None, None], "css": f"QFrame{{background-color: {DARK};}} QWidget{{background-color: {DARK};}} QPushButton{{background-color: {DARK};font: 10pt 'MS Shell Dlg 2';}}"},
    "button_inactive"   : f"background-color: {DARK}",
    "button_active"     : f"background-color: {NORMAL}",

}
