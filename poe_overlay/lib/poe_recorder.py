"""recorder module"""

import os
import time
import json
import threading
from pathlib import Path

import mouse
import keyboard
import pandas as pd


class Recorder:
    """recorder class"""

    def __init__(self, settings):
        self.jsons = []
        self.workers = []
        self.settings = settings
        self.current_recording = []
        self.recording = False
        self._start_time = None
        self._mouse_hook = None
        self.hooked = False
        self.recording_end_callback = None

    def set_recording_end_callback(self, func):
        """set_recording_end_callback"""
        self.recording_end_callback = func

    def _now(self):
        return time.time() - self._start_time  # type: ignore

    def _record_mouse(self):
        def handler(event):
            if not self.recording:
                return

            event_data = {
                "type": "mouse",
                "time": self._now(),
            }

            if isinstance(event, mouse.MoveEvent):
                event_data.update({"event_type": "move", "x": event.x, "y": event.y})
            elif isinstance(event, mouse.ButtonEvent):
                event_data.update(
                    {
                        "event_type": event.event_type,  # 'down' or 'up'
                        "button": event.button,
                    }
                )
            elif isinstance(event, mouse.WheelEvent):
                event_data.update(
                    {
                        "event_type": "wheel",
                        "delta": event.delta,
                    }
                )

            self.current_recording.append(event_data)

        self._mouse_hook = mouse.hook(handler)

    def _record_keyboard(self):
        while self.recording:
            event = keyboard.read_event()
            self.current_recording.append({"type": "keyboard", "time": self._now(), "event_type": event.event_type, "name": event.name})

    def _stop_on_esc(self):
        keyboard.wait("esc")
        self.recording = False
        print("\n[Stopped recording]")

    def record(self):
        """record"""
        self.recording = True
        self._start_time = time.time()
        self.current_recording = []

        print("Recording... Press ESC to stop.")

        # Start mouse hook and keyboard thread
        self._record_mouse()
        keyboard_thread = threading.Thread(target=self._record_keyboard, daemon=True)
        stop_thread = threading.Thread(target=self._stop_on_esc, daemon=True)

        keyboard_thread.start()
        stop_thread.start()

        stop_thread.join()  # Wait for ESC

        mouse.unhook(self._mouse_hook)  # Clean up mouse hook
        if self.recording_end_callback:
            self.recording_end_callback()

    def save(self, recorder_widget):
        """save record"""
        filename = f"{recorder_widget.lineEdit_save.text()}.json"
        mouse_move_delay = float(recorder_widget.lineEdit_mouse_move_delay.text())
        other_keys_delay = float(recorder_widget.lineEdit_other_keys_delay.text())
        repeat = int(recorder_widget.lineEdit_repeat.text())
        save_path = f"{self.settings['base_dir']}/{self.settings['paths']['path_profiles']}/{self.settings['active_profile_name']}/{filename}"

        self.current_recording.sort(key=lambda e: e["time"])
        for num, e in enumerate(self.current_recording):
            e["time_diff"] = 0
            if num > 0:
                e["time_diff"] = e["time"] - self.current_recording[num - 1]["time"]
            try:
                e["next_event"] = self.current_recording[num + 1]["type"] + "_" + self.current_recording[num + 1]["event_type"]
            except:
                e["next_event"] = None

        recording_dic = {"_filename": filename, "mouse_move_delay": mouse_move_delay, "other_keys_delay": other_keys_delay, "repeat": repeat, "_events": self.current_recording}

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(recording_dic, f, indent=4)

        print(f"[Saved {len(self.current_recording)} events to {filename}]")

    def read_records_json(self):
        """load config"""

        dirr = f"{self.settings['base_dir']}/{self.settings['paths']['path_profiles']}/{self.settings['active_profile_name']}"
        json_files = [str(f) for f in Path(dirr).glob("*.json")]
        for file in json_files:
            if ".json" in file and len(file.split("-")) > 1:
                with open(file, "r", encoding="utf-8") as f:
                    key = os.path.basename(file).replace(".json", "")
                    worker = json.load(f)
                    worker["hotkey"] = key.split("-")[0]
                    worker["name"] = key.split("-")[1]
                    self.workers.append(worker)

    def _print_workers(self):
        print("-" * 30, " RECORDER ", "-" * 30)
        df = pd.DataFrame([worker for worker in self.workers])
        df = df[[i for i in df.columns if i[0] != "_"]]
        if df.empty:
            print("\n")
            return
        cols_to_front = ["name", "hotkey"]
        df = df[cols_to_front + [col for col in df.columns if col not in cols_to_front]]
        df = df.fillna("")
        print(df, "\n")

    def hook_all(self):
        """hook_all"""
        if not self.hooked:
            self._print_workers()
            for worker in self.workers:
                _id = keyboard.add_hotkey(worker["hotkey"], self.replay, args=(worker,))
                worker["_id"] = _id
            self.hooked = True

    def unhook_all(self):
        """unhook all workers"""
        if self.hooked:
            print("recorder unhooked ...")
            for worker in self.workers:
                keyboard.remove_hotkey(worker["_id"])
                worker["_running"] = False
            self.hooked = False

    def replay(self, worker):
        """replay record"""
        print(f"\nReplaying {worker['name']} {len(worker['_events'])} events...")
        init_pos = mouse.get_position()

        for _ in range(worker["repeat"]):
            for e in worker["_events"]:
                if e["type"] == "mouse":
                    if e["event_type"] == "move":
                        mouse.move(e["x"], e["y"])
                    elif e["event_type"] == "down":
                        mouse.press(e["button"])
                    elif e["event_type"] == "up":
                        mouse.release(e["button"])

                elif e["type"] == "keyboard":
                    if e["event_type"] == "down":
                        keyboard.press(e["name"])
                    elif e["event_type"] == "up":
                        keyboard.release(e["name"])
                else:
                    pass

                x, y = mouse.get_position()
                if e["next_event"] == "mouse_move":
                    time.sleep(worker["mouse_move_delay"])
                else:
                    time.sleep(worker["other_keys_delay"])
                xx, yy = mouse.get_position()

                # interrupt on mouse move during replaying
                if abs(x - xx) > 30 or abs(y - yy) > 30:
                    print("Replay interrupted:", abs(x - xx), abs(y - yy))
                    keyboard.release("ctrl")
                    keyboard.release("shift")
                    mouse.release("left")
                    mouse.release("right")
                    mouse.move(*init_pos)
                    return

        mouse.move(*init_pos)
        print("[Replay complete]")
