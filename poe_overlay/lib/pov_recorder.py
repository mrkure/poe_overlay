"""recorder module"""

import os
import time
import json
import threading
from pathlib import Path

import mouse
import keyboard


class Recorder:
    """recorder class"""

    def __init__(self, params):
        self.jsons = {}
        self.workers = {}
        self.params = params
        self.events = []
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
                        # 'x': event.x,
                        # 'y': event.y
                    }
                )
            elif isinstance(event, mouse.WheelEvent):
                event_data.update(
                    {
                        "event_type": "wheel",
                        "delta": event.delta,
                        # 'x': event.x,
                        # 'y': event.y
                    }
                )

            self.events.append(event_data)

        self._mouse_hook = mouse.hook(handler)

    def _record_keyboard(self):
        while self.recording:
            event = keyboard.read_event()
            self.events.append({"type": "keyboard", "time": self._now(), "event_type": event.event_type, "name": event.name})

    def _stop_on_esc(self):
        keyboard.wait("esc")
        self.recording = False
        print("\n[Stopped recording]")

    def record(self):
        """record"""
        self.recording = True
        self._start_time = time.time()
        self.events = []

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

    def save(self, filename):
        """save record"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=2)
        print(f"[Saved {len(self.events)} events to {filename}]")

    def load(self, filename):
        """load all records"""
        with open(filename, "r", encoding="utf-8") as f:
            self.events = json.load(f)
        print(f"[Loaded {len(self.events)} events from {filename}]")

    def read_records_json(self):
        """load config"""
        json_files = [str(f) for f in Path(r"c:\_software\poe_overlay\poe_overlay").glob("*.json")]
        for file in json_files:
            with open(file, "r", encoding="utf-8") as f:
                self.jsons[os.path.basename(file).replace(".json", "")] = json.load(f)

    def hook_all(self):
        """hook_all"""
        if not self.hooked:
            for key, value in self.jsons.items():
                worker = {"hotkey": key.split("-")[1], "name": key.split("-")[2], "events": value}
                print(f"{'adding record':<20}  {worker['hotkey']:<25}: {worker['name']}")
                _id = keyboard.add_hotkey(worker["hotkey"], self.replay, args=(worker,))
                worker["id"] = _id
                self.workers[key] = worker
            self.hooked = True

    def unhook_all(self):
        """unhook all workers"""
        if self.hooked:
            for worker in self.workers.values():
                print(f"{'removing record':<20}  {worker['hotkey']:<15}: {worker['function'].__name__}")
                keyboard.remove_hotkey(worker["id"])
                worker["running"] = False
            self.hooked = False

    def replay(self, worker):
        """replay record"""
        print(f"\nReplaying {worker['name']} {len(worker['events'])} events...")
        self.events.sort(key=lambda e: e["time"])
        start_replay = time.time()

        for e in worker["events"]:
            wait_time = e["time"] - (time.time() - start_replay)
            if wait_time > 0:
                time.sleep(wait_time)

            if e["type"] == "mouse":
                # print("mouse")
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
        mouse.move(850, 500)
        print("[Replay complete]")
