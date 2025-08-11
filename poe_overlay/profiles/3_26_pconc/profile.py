"""workers module"""

import time
import random
from itertools import count
import mouse
import keyboard


class KeyboardWorkers:
    """functions for keyboard automation"""

    @staticmethod
    def use_portal_scroll(worker, params={"hotkey": "`", "active": True}):
        """use portal scroll"""
        if not worker:
            return params
        delay = 0.1
        time.sleep(delay)
        keyboard.send("i")
        time.sleep(delay)
        mouse.move(1872, 891)
        time.sleep(delay)
        mouse.right_click()
        time.sleep(delay)
        keyboard.send("i")
        time.sleep(delay)
        mouse.move(961, 440)
        time.sleep(delay)
        mouse.click()
        worker["_running"] = False

    @staticmethod
    def fast_click_left_with_ctrl_down(worker, params={"hotkey": "f4", "active": True, "togle": True}):
        """move items - fast click left with ctrl down"""
        if not worker:
            return params
        sleep = 1
        keyboard.press("ctrl")
        time.sleep(sleep)
        for i in range(10):
            if not worker["_running"]:
                keyboard.release("ctrl")
                break
            print(f"sending ctrl+click {i}")
            mouse.click()
            time.sleep(sleep)
        keyboard.release("ctrl")
        worker["_running"] = False

    @staticmethod
    def fast_click_left_with_shift_down(worker, params={"hotkey": "f5", "active": True, "togle": True}):
        """move items - fast click left with ctrl down"""
        if not worker:
            return params
        sleep = 0.03
        keyboard.press("shift")
        time.sleep(sleep)
        for i in range(200):
            if not worker["_running"]:
                keyboard.release("shift")
                break
            print(f"sending shift+click {i}")
            mouse.click()
            time.sleep(sleep)
        keyboard.release("shift")
        worker["_running"] = False

    @staticmethod
    def use_skill_repeatedly(worker, params={"active": True, "hotkey": "space", "timeout": 10}):
        """use skill repeatidly - for example molten shell"""
        if not worker:
            return params
        for i in count():  # infinite loop
            if not worker["_running"]:
                break
            if i == 0 or i % worker["timeout"] == 0:  # trigger on first iteration and when delay%i == 0
                # code here
                keyboard.send("space")
                time.sleep(1)
                keyboard.send("y")
                time.sleep(random.randint(1, 500) / 500)
            time.sleep(1)
        worker["_running"] = False

    @staticmethod
    def flask_use_rotation(worker, params={"active": False, "hotkey": "x", "timeout": 10}):
        """keyboard flask rotation"""
        if not worker:
            params["_flasks_pointer"] = 0
            return params
        delay = 0.1
        for key_to_send in worker["flasks"][worker["_flasks_pointer"]]:
            keyboard.send(str(key_to_send))
            time.sleep(delay)
        worker["_flasks_pointer"] += 1
        if worker["_flasks_pointer"] == len(worker["flasks"]):
            worker["_flasks_pointer"] = 0
        worker["_running"] = False


class MouseWorkers:
    """functions for mouse automation"""

    @staticmethod
    def wheel_forward(worker, params={"active": True, "timeout": 1, "flasks": [[8,9]]}):
        """wheel_forward"""
        if not worker:
            params["_flasks_pointer"] = 0
            return params

        while worker["_running"]:
            for key_to_send in worker["flasks"][worker["_flasks_pointer"]]:
                keyboard.send(str(key_to_send))
                time.sleep(0.1)
            worker["_flasks_pointer"] += 1
            if worker["_flasks_pointer"] == len(worker["flasks"]):
                worker["_flasks_pointer"] = 0
            time.sleep(worker["timeout"])
            worker["_running"] = False

    @staticmethod
    def wheel_backward(worker, params={"active": True, "timeout": 2}):
        """wheel_forward"""
        if not worker:
            return params
        while worker["_running"]:
            keyboard.send("u")
            time.sleep(1)
            keyboard.send("u")
            time.sleep(1)
            time.sleep(worker["timeout"])
            worker["_running"] = False

    @staticmethod
    def click_middle_button(worker, params={"active": True, "timeout": 2, "toggle": True}):
        """use skill repeatidly - for example molten shell"""
        if not worker:
            return params
        for i in count():  # infinite loop
            if not worker["_running"]:
                break
            if i == 0 or i % worker["timeout"] == 0:  # trigger on first iteration and when delay%i == 0
                # code here
                keyboard.send("9")
                time.sleep(random.randint(1, 500) / 500)
            time.sleep(1)
        # worker["_running"] = False


class AutomationWorkers:
    """Automation - reaction to frame scan"""

    mana_pointer, mana_timeout, hooked = 0, 1, 0
    heal_pointer, heal_timeout = 0, 1

    @staticmethod
    def hook_all():
        """hook_all"""
        AutomationWorkers.hooked = True
        AutomationWorkers.autoheal(None, None, None, pprint=True)
        AutomationWorkers.automana(None, None, None, pprint=True)

    @staticmethod
    def unhook_all():
        """hook_all"""
        AutomationWorkers.hooked = False
        print("automation unhooked ... ")

    @staticmethod
    def autoheal(widget, heal_value, game_active, pprint=False, params={"active": True, "keys": [[1, 2], [3]], "low_lim": 13, "high_lim": 60, "timeout": 1}):
        """wheel_forward"""
        if pprint:
            return params
        AutomationWorkers.heal_timeout += 10
        widget.label.setText(str(heal_value))
        if (params["low_lim"] < heal_value < params["high_lim"]) and game_active and params["active"] and AutomationWorkers.hooked:
            if AutomationWorkers.heal_timeout >= params["timeout"]:  # ms
                print("Autoheal activated")
                for key_to_send in params["keys"][AutomationWorkers.heal_pointer]:
                    keyboard.send(str(key_to_send))
                    time.sleep(0.05)
                AutomationWorkers.heal_pointer += 1
                if AutomationWorkers.heal_pointer == len(params["keys"]):
                    AutomationWorkers.heal_pointer = 0
                AutomationWorkers.heal_timeout = 0

    @staticmethod
    def automana(widget, mana_value, game_active, pprint=False, params={"active": True, "keys": [[1, 2], [3]], "low_lim": 13, "high_lim": 60, "timeout": 1}):
        """wheel_forward"""
        if pprint:
            return params
        AutomationWorkers.mana_timeout += 10
        widget.label.setText(str(mana_value))
        if (params["low_lim"] < mana_value < params["high_lim"]) and game_active and params["active"] and AutomationWorkers.hooked:
            if AutomationWorkers.mana_timeout >= params["timeout"]:  # ms
                print("Automana activated")
                for key_to_send in params["keys"][AutomationWorkers.mana_pointer]:
                    keyboard.send(str(key_to_send))
                    time.sleep(0.05)
                AutomationWorkers.mana_pointer += 1
                if AutomationWorkers.mana_pointer == len(params["keys"]):
                    AutomationWorkers.mana_pointer = 0
                AutomationWorkers.mana_timeout = 0

NORMAL = "green"
LIGHT = f"light{NORMAL}"
DARK = f"dark{NORMAL}"

params = {
    "paths": {
        "target_app_name": "Path of Exilepconc",
        "path_frame_buttons_ui": "res\\frame_buttons.ui",
        "path_frame_recorder_ui": "res\\frame_recorder.ui",
        "path_icon_running": "res\\running.png",
        "path_icon_stopped": "res\\stopped.png",
    },
    "frame_buttons": {
        "geometry": [600, 1000, 0, 0],
        "css": f"QFrame{{background-color: red;}} QWidget{{background-color: {DARK};}} QPushButton{{background-color: {DARK};font: 10pt 'MS Shell Dlg 2';}}",
        "button_active": f"background-color: {NORMAL}",
        "button_inactive": f"background-color: {DARK}",
    },
    "frame_health_bar": {"geometry": [105, 910, 15, 180], "css": "QLabel {background-color: transparent;border: 1px solid red;color: white;font-size: 14px;}"},
    "frame_health_value": {"geometry": [240, 910, 70, 70], "css": "QLabel {background-color: rgba(14, 255, 255, 210);color: white;font: 18 24pt 'MS Shell Dlg 2';}"},
    "frame_mana_bar": {"geometry": [1600, 910, 15, 180], "css": "QLabel {background-color: transparent;border: 1px solid blue;color: white;font-size: 14px;}"},
    "frame_mana_value": {"geometry": [1500, 910, 70, 70], "css": "QLabel {background-color: rgba(14, 255, 255, 210);color: white;font: 18 24pt 'MS Shell Dlg 2';}"},
    "frame_scan": {"geometry": [5, 29, 1910, 1120], "css": "QLabel {background-color: transparent;border: 2px solid red;color: white;font-size: 14px;}"},
}
