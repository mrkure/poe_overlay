# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 13:24:50 2023

@author: CAZ2BJ
"""
dic_css = {}

#%% GRAY
light  = 'rgb(200, 200, 200)'
normal = 'rgb(150, 150, 150)'
dark   = 'rgb(100, 100, 100)'
css = f"""         
    QWidget{{
        background-color: {dark};}} 
        
    QFrame{{
        background-color: {dark};}} 

    QLineEdit {{
        background-color: {normal};
        font: 10pt "MS Shell Dlg 2";}}  

    QPushButton{{
        background-color: {dark};
        font: 10pt "MS Shell Dlg 2";}} 
    
    QPushButton#pushButtonRec{{
        background-color: {dark};
        font: 10pt "MS Shell Dlg 2";}}  

    QPushButton#pushButtonStop{{
        background-color: {dark};
        font: 10pt "MS Shell Dlg 2";}} 

    QPushButton#pushButtonClose{{
        background-color: {dark};
        font: 10pt "MS Shell Dlg 2";}} 
    
    """   
dic_css['gray'] = css
