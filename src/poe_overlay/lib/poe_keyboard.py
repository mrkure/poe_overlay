"""keyboard hook module"""

import inspect
import threading
from typing import Dict

import keyboard
import poe_overlay.lib.poe_tools as tools
import pandas as pd


class KeyboardManager:
    """hooks keyboard to use shortcuts and run tasks"""

    def __init__(self, keyboard_functions):
        self.hooked = False
        self.workers = []
        self.get_workers(keyboard_functions)

    def _print_workers(self):
        print("-" * 30, " KEYBOARD ", "-" * 30)
        df = pd.DataFrame([worker for worker in self.workers])
        df = df[[i for i in df.columns if i[0] != "_"]]
        cols_to_front = ["name", "hotkey", "active"]
        df = df[cols_to_front + [col for col in df.columns if col not in cols_to_front]]
        df = df.fillna("")
        print(df, "\n")

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
            self._print_workers()
            for worker in self.workers:
                if worker["active"]:
                    self.add_task(worker)
            self.hooked = True

    def unhook_all(self):
        """unhook all workers"""
        if self.hooked:
            print("keyboard unhooked ...")
            for worker in self.workers:
                if worker["active"]:
                    # print(f"{'removing keyboard':<20}{worker['name']}")
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

    def pause_all(self):
        """pause"""
        for worker in self.workers:
            worker["_paused"] = True

    def unpause_all(self):
        """pause"""
        for worker in self.workers:
            worker["_paused"] = False


if __name__ == "__main__":
    from poe_workers import KeyboardWorkers

    kb_manager = KeyboardManager(KeyboardWorkers)
    kb_manager.hook_all()
    kb_manager.wait_for_exit()
    kb_manager.unhook_all()
    kb_manager.hook_all()
    kb_manager.wait_for_exit()
    kb_manager.unhook_all()
