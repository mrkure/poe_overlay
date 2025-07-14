"""mouse hook module"""

import time
import threading
import random
from itertools import count

import mouse
import keyboard
from _params import remap_mouse

class MouseManager:
    """mouse manager"""

    def __init__(self, workers):
        self.workers = workers
        self.hooked = False
        self.complete_workers_data()

    def _toggle_worker(self, event):
        if hasattr(event, "delta"):
            if event.delta == 1.0:  # on wheel forward
                worker = self.workers["wheel_forward"]
            elif event.delta == -1.0:  # on wheel backward
                worker = self.workers["wheel_backward"]
            else:
                return
        elif hasattr(event, "button"):
            if event.button == "middle" and event.event_type == "down":
                worker = self.workers["use_skill_repeatidly"]
            else:
                return
        else:
            return
        if not worker["active"]:
            return
        if not worker["running"]:
            print(f"[{worker['hotkey']}] Starting...{worker['function'].__name__}")
            worker["running"] = True
            forward_thread = threading.Thread(target=worker["function"], args=(worker,), daemon=True)
            forward_thread.start()
        else:
            if worker.get("toggle", False):
                print(f"[{worker['hotkey']}] Stopping...{worker['function'].__name__}")
                worker["running"] = False

    def wait_for_exit(self, exit_key: str = "esc") -> None:
        """test function"""
        print(f"Press {', '.join(key for key in self.workers.keys())} to toggle tasks. Press {exit_key} to quit.")
        keyboard.wait(exit_key)

    def hook_all(self):
        """hook mouse"""
        if not self.hooked:
            for worker in self.workers.values():
                print(f"{'adding mouse':<20}  {worker['hotkey']:<15}: {worker['function'].__name__}")
            mouse.hook(self._toggle_worker)
            self.hooked = True

    def unhook_all(self):
        """unhook mouse"""
        if self.hooked:
            for worker in self.workers.values():
                print(f"{'removing mouse':<20}  {worker['hotkey']:<15}: {worker['function'].__name__}")
                worker["running"] = False
            mouse.unhook_all()
            self.hooked = False

    def complete_workers_data(self):
        """map functions to worker dictionaries"""
        self.workers["wheel_forward"]["function"] = MouseFunctions.wheel_forward
        self.workers["wheel_backward"]["function"] = MouseFunctions.wheel_backward
        self.workers["use_skill_repeatedly"]["function"] = MouseFunctions.use_skill_repeatedly

        for key, value in self.workers.items():
            value["hotkey"] = key
            value["running"] = False
            value["thread"] = None
            value["flasks_pointer"] = 0

class MouseFunctions:
    """MouseFunctions"""

    @staticmethod
    def wheel_forward(worker):
        """wheel_forward"""
        while worker["running"]:
            for key_to_send in worker["flasks"][worker["flasks_pointer"]]:
                keyboard.send(str(key_to_send))
                time.sleep(0.1)
            worker["flasks_pointer"] += 1
            if worker["flasks_pointer"] == len(worker["flasks"]):
                worker["flasks_pointer"] = 0
            time.sleep(worker["timeout"])
            worker["running"] = False

    @staticmethod
    def wheel_backward(worker):
        """wheel_forward"""
        while worker["running"]:
            keyboard.send("u")
            time.sleep(1)
            keyboard.send("u")
            time.sleep(1)
            time.sleep(worker["timeout"])
            worker["running"] = False

    @staticmethod
    def use_skill_repeatedly(worker):
        """use skill repeatidly - for example molten shell"""
        for i in count():  # infinite loop
            if not worker["running"]:
                break
            if i == 0 or i % worker["timeout"] == 0:  # trigger on first iteration and when delay%i == 0
                # code here
                keyboard.send("9")
                time.sleep(random.randint(1, 500) / 500)
            time.sleep(1)
        worker["running"] = False


if __name__ == "__main__":
    mo_manager = MouseManager(remap_mouse)
    mo_manager.hook_all()
    mo_manager.wait_for_exit()
    mo_manager.unhook_all()
