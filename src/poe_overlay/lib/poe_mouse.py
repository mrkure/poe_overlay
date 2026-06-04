"""mouse hook module"""

import threading
import inspect
import mouse  # type: ignore
import keyboard
import poe_overlay.lib.poe_tools as tools
import pandas as pd


class MouseManager:
    """mouse manager"""

    def __init__(self, mouse_functions):
        self.workers = {}
        self.hooked = False
        self.get_workers(mouse_functions)

    def _print_workers(self):
        print("-" * 30, " MOUSE ", "-" * 30)
        df = pd.DataFrame([worker for (_, worker) in self.workers.items()])
        df = df[[i for i in df.columns if i[0] != "_"]]
        cols_to_front = ["name", "hotkey", "active"]
        df = df[cols_to_front + [col for col in df.columns if col not in cols_to_front]]
        df = df.fillna("")
        print(df, "\n")

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
                worker = self.workers["click_middle_button"]
            else:
                return
        else:
            return
        if not worker["active"] or worker["_paused"]:
            return
        if not worker["_running"]:
            print(f"Starting...{worker['name']}")
            worker["_running"] = True
            forward_thread = threading.Thread(target=worker["_function"], args=(worker,), daemon=True)
            forward_thread.start()
        else:
            if worker.get("toggle", False):
                print(f"Stopping...{worker['name']}")
                worker["_running"] = False

    def wait_for_exit(self, exit_key: str = "esc") -> None:
        """test function"""
        print(f"Press {', '.join(key for key in self.workers.keys())} to toggle tasks. Press {exit_key} to quit.")
        keyboard.wait(exit_key)

    def hook_all(self):
        """hook mouse"""

        if not self.hooked:
            self._print_workers()
            # for _, worker in self.workers.items():
            # if worker["active"]:
            # print(f"{'adding mouse':<20}{tools.print_dic(worker)}")
            mouse.hook(self._toggle_worker)
            self.hooked = True

    def unhook_all(self):
        """unhook mouse"""
        if self.hooked:
            print("mouse unhooked ...")
            # for _, worker in self.workers.items():
            #     print(f"{'removing mouse':<20}{worker['name']}")
            #     worker["_running"] = False
            mouse.unhook_all()
            self.hooked = False

    def get_workers(self, mouse_functions):
        """map functions to worker dictionaries"""
        for name, func in inspect.getmembers(mouse_functions, inspect.isfunction):
            worker = func(None)
            # worker["hotkey"] = "".join([i[0] for i in name.split("_")])
            worker["name"] = name
            worker["_paused"] = False
            worker["_function"] = func
            worker["_running"] = False
            worker["_thread"] = None
            worker["_flasks_pointer"] = 0
            self.workers[worker["name"]] = worker


if __name__ == "__main__":
    from poe_workers import MouseWorkers

    mo_manager = MouseManager(MouseWorkers)
    mo_manager.hook_all()
    mo_manager.wait_for_exit()
    mo_manager.unhook_all()
