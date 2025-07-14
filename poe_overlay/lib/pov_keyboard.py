"""keyboard hook module"""

import random
import threading
import time
from itertools import count
from typing import Dict

import mouse
import keyboard
from _params import remap_keyboard


class KeyboardManager:
    """hooks keyboard to use shortcuts and run tasks"""

    def __init__(self, workers):
        self.workers = workers
        self.hooked = False
        self.complete_workers_data()

    def add_task(self, worker: Dict) -> None:
        """add task to keyboard hooks using key shortcut

        Args:
            hotkey (str): hotkey
            func (Callable): dictionary with shortcut, function and thread
        """

        _id = keyboard.add_hotkey(worker["hotkey"], self._toggle_worker, args=(worker,))
        worker["id"] = _id

    def _toggle_worker(self, worker: dict) -> None:
        """thread manager, start or close (virtually) function

        Args:
            hotkey (str): _description_
        """
        if not worker["active"]:
            return
        if not worker["running"]:
            print(f"[{worker['hotkey']}] Starting...{worker['function'].__name__}")
            worker["running"] = True
            thread = threading.Thread(target=worker["function"], args=(worker,), daemon=True)
            worker["thread"] = thread
            thread.start()
        else:
            print(f"[{worker['hotkey']}] Stopping...{worker['function'].__name__}")
            worker["running"] = False

    def wait_for_exit(self, exit_key: str = "esc") -> None:
        """test function

        Args:
            exit_key (str, optional): _description_. Defaults to "esc".
        """
        print(f"Press {', '.join(worker['hotkey'] for worker in self.workers)} to toggle tasks. Press {exit_key} to quit.")
        keyboard.wait(exit_key)

    def hook_all(self):
        """hook all shortcuts"""
        if not self.hooked:
            # keyboard.remap_key("caps lock", params["caps lock"])
            for worker in self.workers.values():
                print(f"{'adding keyboard':<20} {worker['hotkey']:<15}: {worker['function'].__name__}")
                self.add_task(worker)
            self.hooked = True

    def unhook_all(self):
        """unhook all workers"""
        if self.hooked:
            for worker in self.workers.values():
                print(f"{'removing keyboard':<20}  {worker['hotkey']:<15}: {worker['function'].__name__}")
                keyboard.remove_hotkey(worker["id"])
                worker["running"] = False
        self.hooked = False

    def complete_workers_data(self):
        """map functions to worker dictionaries"""
        self.workers["fast_click_left_with_ctrl_down"]["function"] = KeyboardFunctions.fast_click_left_with_ctrl_down
        self.workers["fast_click_left_with_shift_down"]["function"] = KeyboardFunctions.fast_click_left_with_shift_down
        self.workers["use_skill_repeatedly"]["function"] = KeyboardFunctions.use_skill_repeatedly
        self.workers["use_portal_scroll"]["function"] = KeyboardFunctions.use_portal_scroll

        for worker in self.workers.values():
            worker["running"] = False
            worker["thread"] = None


class KeyboardFunctions:
    """functions for keyboard automation"""

    @staticmethod
    def use_portal_scroll(worker: dict, delay: float = 0.1):
        """use portal scroll"""
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
        worker["running"] = False

    @staticmethod
    def fast_click_left_with_ctrl_down(worker: dict, sleep: float = 0.03):
        """move items - fast click left with ctrl down"""
        keyboard.press("ctrl")
        time.sleep(sleep)
        for i in range(200):
            if not worker["running"]:
                keyboard.release("ctrl")
                break
            print(f"sending ctrl+click {i}")
            mouse.click()
            time.sleep(sleep)
        keyboard.release("ctrl")
        worker["running"] = False

    @staticmethod
    def fast_click_left_with_shift_down(worker: dict, sleep: float = 0.03):
        """use items - fast click left with shift down"""
        keyboard.press("shift")
        time.sleep(sleep)
        for i in range(200):
            if not worker["running"]:
                keyboard.release("shift")
                break
            print(f"sending shift+click {i}")
            mouse.click()
            time.sleep(sleep)
        keyboard.release("shift")
        worker["running"] = False

    @staticmethod
    def use_skill_repeatedly(worker: dict, delay=10):
        """use skill repeatidly - for example molten shell"""
        for i in count():  # infinite loop
            if not worker["running"]:
                break
            if i == 0 or i % worker["timeout"] == 0:  # trigger on first iteration and when delay%i == 0
                # code here
                keyboard.send("space")
                time.sleep(1)
                keyboard.send("y")
                time.sleep(random.randint(1, 500) / 500)
            time.sleep(1)
        worker["running"] = False

    @staticmethod
    def flask_use_rotation(worker: dict, delay=0.1):
        """keyboard flask rotation"""
        for key_to_send in worker["flasks"][worker["flasks_pointer"]]:
            keyboard.send(str(key_to_send))
            time.sleep(delay)
        worker["flasks_pointer"] += 1
        if worker["flasks_pointer"] == len(worker["flasks"]):
            worker["flasks_pointer"] = 0
        worker["running"] = False


kb_manager = KeyboardManager(remap_keyboard)


if __name__ == "__main__":
    kb_manager.hook_all()
    kb_manager.wait_for_exit()
    kb_manager.unhook_all()
    kb_manager.hook_all()
    kb_manager.wait_for_exit()
