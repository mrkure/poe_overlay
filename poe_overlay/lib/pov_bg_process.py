"""background process module, run in loop, evaluate health values"""

import numpy as np

import pov_monitor_grabber as mg
from pov_capture_evaluator import CaptureEvaluator


def capture_screen(capture_ar, states_ar, params):
    """captures screen state"""

    window_geometry  = params["frame_scan"]["geometry"]
    frame_health_bar = params["frame_health_bar"]["geometry"]
    frame_mana_bar   = params["frame_mana_bar"]["geometry"]
    capture_ar       = np.frombuffer(capture_ar.get_obj(), dtype=np.uint8).reshape((window_geometry[3], window_geometry[2], 4))
    states_ar        = np.frombuffer(states_ar.get_obj(), dtype=np.uint)
    monitor_grabber  = mg.MonitorGrabber(window_geometry)

    while states_ar.item(0):
        capture_ar[:, :, :] = monitor_grabber.grab_geometry(window_geometry)
        health_value, _, _, _ = CaptureEvaluator.evaluate_health_bar(capture_ar, frame_health_bar)
        states_ar[5] = health_value

        mana_value, _, _, _ = CaptureEvaluator.evaluate_mana_bar(capture_ar, frame_mana_bar)
        states_ar[6] = mana_value
        # print(mana_value)