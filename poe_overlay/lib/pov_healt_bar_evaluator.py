# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 21:21:48 2022

@author: mrkure
"""

import numpy as np # type: ignore
import cv2 as cv  # type: ignore

class HealthBarEvaluator:
    """health bar evaluator"""

    def __init__(self, health_area):
        self.x, self.y, self.w, self.h = (
            health_area[0],
            health_area[1],
            health_area[2],
            health_area[3],
        )

    def evaluate_health_bar(self, capture, treshold=20, hue=[176, 180], sat=[180, 255], value=[50, 255]): # pylint: disable=W0102
        """evaluates health bar"""
        x, y, w, h = self.x, self.y, self.w, self.h
        hsv = cv.cvtColor(capture[y : y + h, x : x + w, :], cv.COLOR_BGR2HSV)
        lower_red = np.array([hue[0], sat[0], value[0]])
        upper_red = np.array([hue[1], sat[1], value[1]])
        mask = cv.inRange(hsv, lower_red, upper_red)
        res_ar = np.mean(mask, axis=1)
        res_ar[res_ar < treshold] = 0
        health_bar_percentage = int(len(res_ar[res_ar > 0]) / len(res_ar) * 100)

        controll_ar = np.ones((len(res_ar), 10))
        controll_ar = controll_ar * res_ar[:, None]
        y = -0.1521 * health_bar_percentage + 11.847 + health_bar_percentage

        return y, mask, controll_ar


# if __name__ == "__main__":
#     import time
#     import lib_monitor_grabber as lmg

#     grab_area = [0, 0, 1920, 1140]
#     health_area = [115, 950, 15, 180]

#     grabber = lmg.MonitorGrabber(None)
#     health_bar_eval = HealthBarEvaluator(health_area)

#     start = time.time()
#     count = 1
#     for i in range(count):
#         # grab - r,b,g,o
#         grab = grabber.grab_geometry(grab_area)
#         result, mask, res_ar = health_bar_eval.evaluate_health_bar(grab)
#         print(result)
#         cv.imshow("frame", mask)
#         cv.moveWindow("frame", -400, 800)
#         cv.imshow("2", res_ar)
#         cv.moveWindow("2", -200, 800)
#         cv.waitKey(40)
#         time.sleep(0.5)
#         # cv.destroyAllWindows()
#     end = time.time()
#     print(count / (end - start))
