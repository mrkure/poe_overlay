"""capture evaluator module"""
import time
import numpy as np  # type: ignore
import cv2 as cv  # type: ignore

from PyQt5 import QtCore as qtc  # type: ignore
from PyQt5 import QtWidgets  # type: ignore
from PyQt5.QtWidgets import QApplication, QVBoxLayout  # type: ignore

import pov_monitor_grabber as lmg

class CaptureEvaluator:
    """health bar evaluator"""
    DEBUG = False

    @staticmethod
    def evaluate_health_bar(capture, frame, treshold=20, hue=[176, 180], sat=[180, 255], value=[50, 255]):  # pylint: disable=W0102
        """evaluates health bar"""
        x, y, w, h = frame[0], frame[1], frame[2], frame[3]
        frame_captured = capture[y : y + h, x : x + w, :]
        hsv = cv.cvtColor(frame_captured, cv.COLOR_BGR2HSV)
        if CaptureEvaluator.DEBUG:
            print("--------------HSV---------------")
            print(hsv)
            time.sleep(1)
        lower_red = np.array([hue[0], sat[0], value[0]])
        upper_red = np.array([hue[1], sat[1], value[1]])
        mask = cv.inRange(hsv, lower_red, upper_red)
        res_ar = np.mean(mask, axis=1)
        res_ar[res_ar < treshold] = 0
        health_bar_percentage = int(len(res_ar[res_ar > 0]) / len(res_ar) * 100)
        if CaptureEvaluator.DEBUG:
            print("--------------MASK---------------")
            print(mask)
            time.sleep(1)
        controll_ar = np.ones((len(res_ar), 10))
        controll_ar = controll_ar * res_ar[:, None]
        y = -0.1521 * health_bar_percentage + 11.847 + health_bar_percentage

        return y, mask, controll_ar, frame_captured

    @staticmethod
    def evaluate_mana_bar(capture, frame, treshold=100, hue=[90, 130], sat=[170, 255], value=[50, 255]):  # pylint: disable=W0102
        """evaluates health bar"""
        x, y, w, h = frame[0], frame[1], frame[2], frame[3]
        frame_captured = capture[y : y + h, x : x + w, :]
        hsv = cv.cvtColor(frame_captured, cv.COLOR_BGR2HSV)  # translate bgr to hsv
        if CaptureEvaluator.DEBUG:
            print("--------------HSV---------------")
            print(hsv)
            time.sleep(1)
        lower_blue = np.array([hue[0], sat[0], value[0]])
        upper_blue = np.array([hue[1], sat[1], value[1]])
        mask = cv.inRange(hsv, lower_blue, upper_blue)  # mask based on requirments, in limits results in 255, out limits results in 0
        if CaptureEvaluator.DEBUG:
            print("--------------MASK---------------")
            print(mask)
            time.sleep(1)
        res_ar = np.mean(mask, axis=1)  # create mean for each row -> one value for each row
        res_ar[res_ar < treshold] = 0  # zero each row if mean value is less than treshold
        mana_bar_percentage = int(len(res_ar[res_ar > 0]) / len(res_ar) * 100)  # total zero pixels divided by total pixels in percent

        controll_ar = np.ones((len(res_ar), 10))  # extend res_ar to 10 pixels wide to get better visibility
        controll_ar = controll_ar * res_ar[:, None]
        y = -0.1521 * mana_bar_percentage + 11.847 + mana_bar_percentage  # custom recalculation of results

        return y, mask, controll_ar, frame_captured


# ___________________________________________TESTING____________________________________________________
class FrameWidget(QtWidgets.QWidget):
    """frame widget to display various frames on screen"""

    def __init__(self, frame_scan, frame, outer_frame, css):
        super().__init__()
        self.setWindowFlags(qtc.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.Tool)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)

        x, y, w, h = frame_scan
        xl, yl, wl, hl = frame

        if outer_frame:
            xl, yl, wl, hl = 0, 0, w, h
            self.setGeometry(qtc.QRect(x + xl, y + yl, wl, hl))  # x, y, width, height
        else:  # for inner frames, resize geometry by 2 pixels to each side, because borders 2pix wide are drawn inside geometry and move up and left by one pixel
            self.setFixedSize(wl + 2, hl + 2)
            self.move(xl - 1, yl - 1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QtWidgets.QLabel(self)
        self.label.setStyleSheet(css)
        layout.addWidget(self.label)


class Main(QtWidgets.QWidget):
    """main window class invisible window on the whole monitor
    class has to inherit from QWidget, to be able to work with signals"""

    # _______________________________________ INIT _______________________________________
    def __init__(self, frame_scan, frame_health_bar, frame_mana_bar):
        self.frame_scan = frame_scan
        self.frame_health_bar = frame_health_bar
        self.frame_mana_bar = frame_mana_bar
        super().__init__()
        self.setWindowFlags(qtc.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.Tool)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)
        self.wscan = FrameWidget(frame_scan, frame_scan, True, "QWidget {background-color: transparent;border: 2px solid red;color: white;font-size: 14px;}")
        self.wscan.show()
        self.whealth = FrameWidget(frame_scan, frame_health_bar, False, "QWidget {background-color: transparent;border: 1px solid red;color: white;font-size: 14px;}")
        self.whealth.show()
        self.wmana = FrameWidget(frame_scan, frame_mana_bar, False, "QWidget {background-color: transparent;border: 1px solid blue;color: white;font-size: 14px;}")
        self.wmana.show()
        self.show()
        self.scan()

    def scan(self):
        """scan testing method"""
        grabber = lmg.MonitorGrabber(None)
        capeval = CaptureEvaluator

        x = 0
        while True:
            # grab - r,b,g,o
            grab = grabber.grab_geometry(self.frame_scan)
            result, mask, res_ar, frame_captured = capeval.evaluate_health_bar(grab, self.frame_health_bar)
            mresult, mmask, mres_ar, mframe_captured = capeval.evaluate_mana_bar(grab, self.frame_mana_bar)
            print(f"health: {int(result)}, mana: {int(mresult)}")
            cv.imshow("capture health", frame_captured)
            cv.imshow("mask health", mask)
            cv.imshow("result health", res_ar)

            cv.imshow("capture mana", mframe_captured)
            cv.imshow("mask mana", mmask)
            cv.imshow("result mana", mres_ar)

            if not x:
                cv.moveWindow("capture health", 2300, 0)
                cv.moveWindow("mask health", 2700, 0)
                cv.moveWindow("result health", 3100, 0)

                cv.moveWindow("capture mana", 2300, 300)
                cv.moveWindow("mask mana", 2700, 300)
                cv.moveWindow("result mana", 3100, 300)
            x += 1
            # Wait 40 milliseconds; break if ESC is pressed
            if cv.waitKey(4) & 0xFF == 27:
                break

        cv.destroyAllWindows()

        self.wscan.close()
        self.whealth.close()
        self.wmana.close()
        self.close()


if __name__ == "__main__":
    # START TESTING -> STOP TESTING USING ESC KEY
    CaptureEvaluator.DEBUG = True
    frame_scan = [0, 0, 1900, 1000]  # whole window frame
    frame_health_bar = [115, 800, 15, 150]  # relative frame to frame_scan
    frame_mana_bar = [1600, 800, 5, 2]  # relativo frame to frame_scan

    app = QApplication([])
    tray_app_trade_whisper = Main(frame_scan, frame_health_bar, frame_mana_bar)
    app.setStyle("fusion")
    app.exec()
