# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 22:46:14 2022

@author: 42073
"""

import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QToolTip, QMessageBox, QLabel)

class Window2(QMainWindow):                           # <===
    submitted = QtCore.pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window22222")
        self.pushButton = QPushButton("Start", self)
        self.pushButton.clicked.connect(self.on_submit) 
        self.setWindowFlags ( QtCore.Qt.WindowStaysOnTopHint )   
        self.activateWindow()
        self.setFocus()
        self.show()
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
    def on_submit(self):
        self.submitted.emit('aaa')
        
test = [5]        
class Window(QMainWindow):
    def __init__(self, test):
        super().__init__()
        # self.window2()
        self.title = "First Window"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        
        self.pushButton = QPushButton("Start", self)
        self.pushButton.move(275, 200)
        self.pushButton.setToolTip("<h3>Start the Session</h3>")
        test[0] = 8
        self.pushButton.clicked.connect(self.window2)              # <===

        self.main_window()

    def main_window(self):
        self.label = QLabel("Manager", self)
        self.label.move(285, 175)
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()
        
    def window2(self):                                             # <===
        self.w = Window2()
        self.w.submitted.connect(self.update)
        self.w.show()
        self.hide()
        
    @QtCore.pyqtSlot(str)
    def update(self, message):
        self.pushButton.setText(message)
import sys  
      
def mainn(argv):
    app = QApplication(sys.argv)
    
    window = Window(test)
    # if ( not window.exec_() ):  # in C++, this would be dlg->exec()
    #      sys.exit(0)
    # window2 = Window2()
    if ( not app.exec_() ):  # in C++, this would be dlg->exec()
        print('exit')
        # app = QApplication(sys.argv)
        window2 = Window2()
        if ( not app.exec_() ):
            print(test[0])
            sys.exit(0)
        
    print(5)
    sys.exit(app.exec())
if __name__ == "__main__":
    # a= 4
    mainn(sys.argv) 
    # mainn(sys.argv) 
    # a= 5
    # print('a')
    
    
    
    
    
    
    
    
    
    
    
    
    