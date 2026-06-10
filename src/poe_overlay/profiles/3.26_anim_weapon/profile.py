"""workers module"""
import time, random, mouse, keyboard
from itertools import count
# fmt: off

color          = "green"
autoheal       = {"active": True, "keys": [[1]], "low_lim": 13, "high_lim": 80, "timeout": 1000}
automana       = {"active": True, "keys": [[5]], "low_lim": 13, "high_lim": 80, "timeout": 1000}
mouse_forward  = {"hotkey": "wf","active": True, "timeout": 1, "flasks": [[2],[3],[4]]}
mouse_backward = {"hotkey": "wb","active": True, "timeout": 2}

widget_params = {
    "frame_scan"        : {"geometry": [   5,  800,  1915, 1150], "css": "QLabel {background-color: transparent;border: 2px solid red;color: white;font-size: 14px;}"},
    "frame_buttons"     : {"geometry": [600, 1000,   650,  1050], "css": f"QWidget{{background-color: {color};}} QComboBox,QPushButton{{background-color: {color};font: 10pt 'MS Shell Dlg 2';}}", "button_active": f"background-color: light{color}","button_inactive": f"background-color: {color}"},
    "frame_health_bar"  : {"geometry": [ 115, 930,   130, 1110], "css": "QLabel {background-color: transparent;border: 1px solid red;color: white;font-size: 14px;}"},
    "frame_mana_value"  : {"geometry": [1600, 910,  1670,  980], "css": "QLabel {background-color: rgba(14, 255, 255, 210);color: white;font: 18 24pt 'MS Shell Dlg 2';}"},
    "frame_health_value": {"geometry": [ 240, 910,   310,  980], "css": "QLabel {background-color: rgba(14, 255, 255, 210);color: white;font: 18 24pt 'MS Shell Dlg 2';}"},
    "frame_mana_bar"    : {"geometry": [1780, 930,  1795, 1110], "css": "QLabel {background-color: transparent;border: 1px solid blue;color: white;font-size: 14px;}"},
}
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
    def click_left_with_ctrl_down(worker, params={"hotkey": "f4", "active": True, "togle": True}):
        """move items - fast click left with ctrl down"""
        if not worker:
            return params
        sleep = 0.03
        keyboard.press("ctrl")
        time.sleep(sleep)
        for i in range(200):
            if not worker["_running"]:
                keyboard.release("ctrl")
                break
            print(f"sending ctrl+click {i}")
            mouse.click()
            time.sleep(sleep)
        keyboard.release("ctrl")
        worker["_running"] = False

    @staticmethod
    def click_left_with_shift_down(worker, params={"hotkey": "f5", "active": True, "togle": True}):
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
    def use_skill_repeatedly(worker, params={"active": False, "hotkey": "space", "timeout": 10}):
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
    def wheel_forward(worker, params=mouse_forward):
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
    def wheel_backward(worker, params=mouse_backward):
        """wheel_forward"""
        if not worker:
            return params
        while worker["_running"]:
            keyboard.send("f2")
            time.sleep(0.01)
            keyboard.send("f3")
            time.sleep(1)
            worker["_running"] = False

    @staticmethod
    def click_middle_button(worker, params={"hotkey": "cmb","active": False, "timeout": 2, "toggle": True}):
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
        if not AutomationWorkers.hooked:
            print("-" * 30, " AUTOMATION ", "-" * 30)  
            AutomationWorkers.hooked = True
            AutomationWorkers.autoheal(None, None, None, pprint=True)
            AutomationWorkers.automana(None, None, None, pprint=True)
            print()
        
    @staticmethod
    def unhook_all():
        """hook_all"""
        if AutomationWorkers.hooked:
            AutomationWorkers.hooked = False
            print("automation unhooked ... ")

    @staticmethod
    def autoheal(widget, heal_value, game_active, pprint=False, params=autoheal):
        """wheel_forward"""
        if pprint:
            print(f"{'Autoheal started':<20}{params}")
            return
        # print("autoheal")
        AutomationWorkers.heal_timeout += 10
        # print(params["low_lim"] , heal_value , params["high_lim"], game_active , params["active"], AutomationWorkers.hooked)
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
    def automana(widget, mana_value, game_active, pprint=False, params=automana):
        """wheel_forward"""
        if pprint:
            print(f"{'Automana started':<20}{params}")
            return
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
