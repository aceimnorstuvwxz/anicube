#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
(C) 2015 chenbingfeng Turnro.com 湍流游戏

cube2obj transfers .cube file to .obj file. 
It's part of cube animation solution.
'''
import sys
import json
import os

CUBE_WIDTH = 0.8

def genVertexLinesWithPos(pos, f_out, n):
    vertex_template = [
        0.500000,  0.500000,  0.500000, 
        -0.500000,  0.500000,  0.500000, 
        -0.500000, -0.500000,  0.500000, 
        0.500000, -0.500000,  0.500000, 
        0.500000,  0.500000,  0.500000,  
        0.500000,  0.500000, -0.500000, 
        -0.500000,  0.500000,  0.500000, 
        -0.500000,  0.500000, -0.500000, 
        0.500000, -0.500000, -0.500000, 
        -0.500000, -0.500000, -0.500000,
        -0.500000,  0.500000, -0.500000,
        0.500000,  0.500000, -0.500000, 
        0.500000, -0.500000,  0.500000, 
        -0.500000, -0.500000,  0.500000, 
        -0.500000, -0.500000, -0.500000, 
        0.500000, -0.500000, -0.500000, 
        0.500000,  0.500000,  0.500000, 
        0.500000, -0.500000,  0.500000, 
        0.500000,  0.500000, -0.500000, 
        0.500000, -0.500000, -0.500000, 
        -0.500000,  0.500000,  0.500000, 
        -0.500000, -0.500000, -0.500000, 
        -0.500000, -0.500000,  0.500000, 
        -0.500000,  0.500000, -0.500000]
    for i in xrange(len(vertex_template)/3):
        f_out.write('''v %s %s %s\n''' % (pos[0] + CUBE_WIDTH * vertex_template[3*i],
                                          pos[1] + CUBE_WIDTH * vertex_template[3*i + 1],
                                          pos[2] + CUBE_WIDTH * vertex_template[3*i + 2]))
    
    index_template = [0,   1,   2,   0,   2,   3,   4,   5,   6,   6,   5,   7,
        8,   9,  10,   8,  10,  11,  12,  13,  14,  12,  14,  15,
        16,  17,  18,  17,  19,  18,  20,  21,  22,  21,  20,  23]
    for i in xrange(len(index_template)/3):
        f_out.write('''f %s %s %s\n''' % (n*24+1 +index_template[3*i], 
                                          n*24+1 +index_template[3*i + 1],
                                          n*24+1 +index_template[3*i + 2]));

def cube2obj(fn):
    #check
    if not os.path.isfile(fn):
        print "file not exist"
        return
    
    print fn
    file_in = open(fn, 'r')
    fn_out = os.path.join(os.path.dirname(fn), os.path.basename(fn)+".obj")
    print fn_out
    src_lines = file_in.readlines()
    file_in.close()
    src_data = ""
    for _line in src_lines:
        src_data += _line
    
    jobj = json.loads(src_data)
    cubes = jobj["list"]
    file_out = open(fn_out, "w")
    n = 0
    for _cube in cubes:
        pos = _cube["pos"]
        genVertexLinesWithPos(pos, file_out, n)
        n += 1
    
    file_out.close()




if __name__ == "__main__":
    if len(sys.argv) == 2:
        fn = sys.argv[1]
        cube2obj(fn)
    else:
        print "Usage:\n    cube2obj xxx.cube"
    pass
    
