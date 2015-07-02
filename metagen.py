#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
(C) 2015 chenbingfeng Turnro.com 湍流游戏

Generate meta-cube series
'''

import sys
import json
import os.path
'''
{
    "list":
    [
        {
            "id":0,
            "name":"virtual",
            "unreal":1,
            "color":[0.2,0.2,0.2,1.0]
        }
    ]
}
'''

def gen(n):
    step = 1.0 / (n-1)
    print n, step
    cubes = []
    cid = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                cube = {}
                cube["id"] = cid
                cid += 1
                cube["name"] = "auto gen"
                cube["color"] = [i*step, j*step, k*step, 1.0]
                cubes.append(cube)
    
    jall = {}
    jall["list"] = cubes
    jstr = json.dumps(jall)
    return jstr

def genfile(n):
    jstr = gen(n)
    f_out = open("metacubes.json"+str(n), "w")
    f_out.write(jstr)
    f_out.close()

if __name__ == "__main__":
    genfile(4)
    genfile(5)
    genfile(3)
    pass