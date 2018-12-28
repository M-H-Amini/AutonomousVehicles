# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 21:56:38 2018

@author: MHA
"""
import numpy as np
import multiprocessing

def hi():
    for i in range(10):
        print('hi')

if __name__=='__main__':
    p = multiprocessing.Process(target=hi)
    p.start()
    p.join()