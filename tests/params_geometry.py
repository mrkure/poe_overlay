# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 15:39:11 2022

@author: 42073
"""
# x, y, x2, y2 coordinates starting with upper left a ending with bottom right position
# recangles for color parser
rect_health           =  75,    3,  74, 103, 4
rect_healt_party      =  76,    0,  75, 800, 4
rect_party_members    =  42,  186,  22, 800, 4
# rectangles for gui positions
rect_auto_heal_on_off   =  0,   35,  75,   0, 2
rect_dmg_counter_on_off =  76,   35,  151,   0, 2
rect_stopwatch        = 442,   35, 542,   0, 2 
# rect_shadow_evade     = 442,   300, 542,   270, 2 
# rect_shadow_twin     = 550,   300, 650,   270, 2 
rect_shadow_evade     = 840,   300, 940,   270, 2 
rect_shadow_twin     = 960,   300, 1060,   270, 2 

rect_boss_kills       = 370,    0, 920, 999, 1 # y2 position not used calculated by rows number

pos_to_heal  = {
                1 :[42,58],    # Player
                2 :[59,211],   # Party members
                3 :[59,275],
                4 :[59,347],
                5 :[59,410],
                6 :[59,475],
                7 :[59,540],
                8 :[59,605],
                9 :[59,670],
                10:[59,735],    
                }

keybinds      = {
                'key_1':'f1',
                'key_2':'f2',
                'key_3':'f3',
                'key_4':'f4',
                'shadow_evade': 'f4',
                'shadow_twin':'f5',
                'toggle_stopwatch':'+',
                'toggle_keybinds_on_off':'-',
                'start_stop_dps_counter':'*'
                }
