"""background process module, run in loop, evaluate health values"""

import numpy as np

import poe_overlay.lib.poe_monitor_grabber_bettercam as mg
from poe_overlay.lib.poe_capture_evaluator import CaptureEvaluator
from poe_overlay.lib.poe_widgets import  WidgetsParams

def capture_screen(capture_ar, states_ar, params: WidgetsParams):
    """captures screen state"""
    window_geometry = params.frame_scan.region
    frame_health_bar = params.frame_health_bar.regionrel
    frame_mana_bar = params.frame_mana_bar.regionrel
    capture_ar = np.frombuffer(capture_ar.get_obj(), dtype=np.uint8).reshape((params.frame_scan.h, params.frame_scan.w, 3))
    states_ar = np.frombuffer(states_ar.get_obj(), dtype=np.uint32)
    monitor_grabber = mg.MonitorGrabber(window_geometry)
    while states_ar.item(0):
        capture_ar[:, :, :] = monitor_grabber.grab_geometry(window_geometry)
        health_value, _, _, _ = CaptureEvaluator.evaluate_health_bar(capture_ar, frame_health_bar)
        states_ar[5] = health_value
        mana_value, _, _, _ = CaptureEvaluator.evaluate_mana_bar(capture_ar, frame_mana_bar)
        states_ar[6] = mana_value
