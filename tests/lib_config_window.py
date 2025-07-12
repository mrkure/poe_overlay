# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 20:44:21 2022

@author: 42073
"""
import sys
import params_accounts as par
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QPushButton

myFont=QtGui.QFont('Arial', 15)
myFont.setBold(True)


class Config_Window(QMainWindow):                       
    def __init__(self,params, result):
        self.result = result
        super().__init__()
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setWindowTitle("Config window")
        self.setWindowFlags ( QtCore.Qt.WindowStaysOnTopHint )  

        for num, (key, val) in enumerate(params.items()):
            self.button1 = QPushButton(self)
            self.button1.setText(key)
            self.button1.setGeometry(20, 20 + num*70, 300, 60) #x,y,w,h
            self.button1.setStyleSheet("background-color: rgba(235, 186, 52, 200);") 
            self.button1.setFont(myFont) 
            self.button1.clicked.connect(self.on_click) 
            self.button1.show()
        self.resize(340,num*80+ 50)
        self.move(750,350)
        self.show()

    def on_click(self, obj):
        rbt = self.sender()
        self.result[0] = rbt.text()
        self.close()
     
if __name__ == "__main__":  
    result = [None]
    params = par.accounts
    app = QtWidgets.QApplication(sys.argv)
    config_window = Config_Window(params, result)
    if ( not app.exec_() ): 
        print(result[0])
    
    
    
    
    
    
    