"""background process module, run in loop, evaluate health values"""

import numpy as np

import pov_monitor_grabber as lmg
from pov_healt_bar_evaluator import HealthBarEvaluator

def capture_screen(capture_ar, states_ar, window_geometry, frame_health_bar):
    """captures screen state"""

    hbevaluator = HealthBarEvaluator(frame_health_bar)
    capture_ar = np.frombuffer(capture_ar.get_obj(), dtype=np.uint8).reshape((window_geometry[3], window_geometry[2], 4))
    states_ar = np.frombuffer(states_ar.get_obj(), dtype=np.uint)
    monitor_grabber = lmg.MonitorGrabber(window_geometry)

    while states_ar.item(0):
        capture_ar[:, :, :] = monitor_grabber.grab_geometry(window_geometry)
        health_value, _mask, _controll_ar = hbevaluator.evaluate_health_bar(capture_ar)
        states_ar[5] = health_value



# if __name__ == "__main__":
    # import ctypes as c
    # import multiprocessing as mp
#     window_geometry = [0, 0, 1900, 1135]
#     states_ar = mp.Array(c.c_uint, 10)
#     capture_ar = mp.Array(c.c_ubyte, window_geometry[3] * window_geometry[2] * 4)
#     states_ar[0] = 1
#     capture_screen(capture_ar, states_ar, window_geometry)

    # print('health' , y)
#     states[5] = y

# cv.imshow('frame',snapshot)

# # cv.moveWindow('',0,0)
# cv.waitKey(40)
# time.sleep(2)
# cv.destroyAllWindows()
