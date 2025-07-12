# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 20:32:31 2022

@author: mrkure
"""
light  = 'rgb(200, 200, 200)'
normal = 'rgb(150, 150, 150)'
dark   = 'rgb(100, 100, 100)'
params = {
    'use_aura_buffs_sequence'        : 'f1',
    'fast_click_left_with_ctrl_down' : 'f4',
    'fast_click_left_with_shift_down': 'f5',
    'use_portal_scroll'              : '`',
    'caps lock'                      : '6',                                                                              # remapping caps lock to u
    'window_geo'                     : [0, 24, 1920, 1135],                                                              # x, y, w, h
    'frame_css'                      : "background-color: rgba(255, 0, 0, 0)",
    'health_bar_geo'                 : [240, 910, 70, 70],
    'health_bar_css'                 : "background-color: rgba(14, 255, 255, 210);" "font: 18 24pt \"MS Shell Dlg 2\";", # fontsize - XXpt
    'stopwatch_geo'                  : [340, 950, 80, 30],
    'stopwatch_css'                  : "background-color: rgba(14, 255, 255, 210);" "font: 18 14pt \"MS Shell Dlg 2\";", # fontsize - XXpt
    'button_inactive'                : f"background-color: {dark}",
    'button_active'                  : f"background-color: {normal}",
}
