"""keyboard hook module"""

import inspect
import threading
from typing import Dict

import keyboard
import pov_tools as tools



class KeyboardManager:
    """hooks keyboard to use shortcuts and run tasks"""

    def __init__(self, keyboard_functions):
        self.hooked = False
        self.workers = []
        self.get_workers(keyboard_functions)

    def add_task(self, worker: Dict) -> None:
        """add task to keyboard hooks using key shortcut

        Args:
            hotkey (str): hotkey
            func (Callable): dictionary with shortcut, function and thread
        """

        _id = keyboard.add_hotkey(worker["hotkey"], self._toggle_worker, args=(worker,))
        worker["_id"] = _id

    def _toggle_worker(self, worker: dict) -> None:
        """thread manager, start or close (virtually) function

        Args:
            hotkey (str): _description_
        """
        if not worker["active"]:
            return
        if not worker["_running"]:
            print(f"[{worker['hotkey']}] Starting...{worker['name']}")
            worker["_running"] = True
            thread = threading.Thread(target=worker["_function"], args=(worker,), daemon=True)
            worker["_thread"] = thread
            thread.start()
        else:
            print(f"[{worker['hotkey']}] Stopping...{worker['name']}")
            worker["_running"] = False

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
            for worker in self.workers:
                if worker["active"]:
                    print(f"{'adding keyboard':<20}{tools.remove_dict_keys_with_underscore(worker)}")
                    self.add_task(worker)
            self.hooked = True

    def unhook_all(self):
        """unhook all workers"""
        if self.hooked:
            for worker in self.workers:
                if worker["active"]:
                    print(f"{'removing keyboard':<20}{worker['name']}")
                    keyboard.remove_hotkey(worker["_id"])
                    worker["_running"] = False
                self.hooked = False

    def get_workers(self, keyboard_functions):
        """map functions to worker dictionaries"""
        for name, func in inspect.getmembers(keyboard_functions, inspect.isfunction):
            worker = func(None)
            worker["name"] = name
            worker["_function"] = func
            worker["_running"] = False
            worker["_thread"] = None
            self.workers.append(worker)



if __name__ == "__main__":
    from pov_workers import KeyboardWorkers
    kb_manager = KeyboardManager(KeyboardWorkers)
    kb_manager.hook_all()
    kb_manager.wait_for_exit()
    kb_manager.unhook_all()
    kb_manager.hook_all()
    kb_manager.wait_for_exit()
    kb_manager.unhook_all()
