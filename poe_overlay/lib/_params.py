"""params module"""

import os

LIGHT  = "rgb(200, 200, 200)"
NORMAL = "rgb(150, 150, 150)"
DARK   = "rgb(100, 100, 100)"


remap_mouse = {
    "wheel_forward"       : {"active": True,"timeout": 2, "flasks": [[4, 5]]},
    "wheel_backward"      : {"active": True,"timeout": 2},
    "use_skill_repeatedly": {"active": False,"timeout": 1, "toggle": True},
}

remap_keyboard = {
    "fast_click_left_with_ctrl_down" : {"active": True, "hotkey": "f4"},
    "fast_click_left_with_shift_down": {"active": True, "hotkey": "f5"},
    "use_portal_scroll"              : {"active": True, "hotkey": "`"},
    "use_skill_repeatedly"           : {"active": True, "hotkey": "space", "timeout": 10},
}

params = {
    "autoheal"             : {"active": True, "low_lim": 13, "high_lim": 60, "timeout": 1000, "keys": [1, 2, 3]},
    "target_app_name"      : "Path of Exile",
    "path_frame_buttons_ui": rf"{os.path.dirname(os.path.dirname(__file__))}\res\frame_buttons.ui",
    "path_icon_running"    : rf"{os.path.dirname(os.path.dirname(__file__))}\res\running.png",
    "path_icon_stopped"    : rf"{os.path.dirname(os.path.dirname(__file__))}\res\stopped.png",
    "frame_scan"           : {"geometry": [5, 29, 1910, 1120], "css": "QLabel {background-color: transparent;border: 2px solid red;color: white;font-size: 14px;}"},
    "frame_health_bar"     : {"geometry": [105, 910, 15, 180], "css": "QLabel {background-color: transparent;border: 2px solid red;color: white;font-size: 14px;}"},
    "frame_health_value"   : {"geometry": [240, 910, 70, 70], "css": "QLabel {background-color: rgba(14, 255, 255, 210);color: white;font: 18 24pt 'MS Shell Dlg 2';}"},
    "frame_stop_watch"     : {"geometry": [340, 950, 80, 30], "css": "QLabel {background-color: rgba(14, 255, 255, 210);color: white;font: 18 24pt 'MS Shell Dlg 2';}"},
    "frame_buttons"        : {
        "geometry": [600, 1100, None, None],
        "css"     : f"QFrame{{background-color: {DARK};}} QWidget{{background-color: {DARK};}} QPushButton{{background-color: {DARK};font: 10pt 'MS Shell Dlg 2';}}",
    },
    "button_inactive": f"background-color: {DARK}",
    "button_active"  : f"background-color: {NORMAL}",
}
