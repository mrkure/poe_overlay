# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 15:43:03 2022

@author: 42073
"""
import numpy as np

class Calc:
    def get_health(arr):
        # arr = arr[:,0, 2]
        red_and_black = len(arr)
        red           = len(arr[arr == 255])
        return int(red/red_and_black*100) -100
    
    def get_party_member(arr, num):
        i = 66*num
        ared   = arr[0+i:24+i, ::, 2]        
        minn   = min( min(ared[-1,:]), min(ared[-1,:]))
        maxx   = max( max(ared[-1,:]), max(ared[-1,:]))
        if ared[1,1] + ared[-2,-2]+ ared[1,-2]+ ared[-2, 1] == 0: 
            if minn  > 145 and maxx < 151:
                if np.sum(ared[3:16, 3:16]) > 100:
                    return [True, True]
                return [True, False]    
        return [False,False]   

    def get_party_members(arr):
        members = []
        for i in range(8):
            x = Calc.get_party_member(arr, i)
            if x[0] == False:
                return members
            else:
                members.append(x)
        return members
     
    def get_party_health(arr_self, arr, members):
        members_new = []
        health = Calc.get_health(arr_self)
        members_new.append([True, True, health])
        redd   = arr[:,:, 2]
        for num, member in enumerate(members):
            i = 66*num
            res = redd[186 +  i: 236 + i]    
            red_and_black = len(res)
            red           = len(res[res > 0])
            members_new.append([member[0], member[1], int(red/red_and_black*100)])
        return members_new
