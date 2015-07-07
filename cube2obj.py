#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
(C) 2015 chenbingfeng Turnro.com 湍流游戏

cube2obj transfers .cube file to .obj file. 
It's part of cube animation solution.
'''
import sys
import json
import os.path as path
from PIL import Image, ImageDraw

CUBE_WIDTH = 1.0000
TEXTURE_WIDTH = 128

def genVertexLinesWithPos(pos, ci, f_out, n):
    assert(ci >=0 and ci < 100)
    tex_step = 1.0 / TEXTURE_WIDTH
    vertex_template = [
        0.500000,  0.500000,  0.500000, 
        -0.500000,  0.500000,  0.500000, 
        -0.500000, -0.500000,  0.500000, 
        0.500000, -0.500000,  0.500000, 
        
        0.500000,  0.500000,  0.500000,  
        0.500000,  0.500000, -0.500000, 
        -0.500000,  0.500000, -0.500000, 
        -0.500000,  0.500000,  0.500000, 
        
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
        0.500000, -0.500000, -0.500000, 
        0.500000,  0.500000, -0.500000, 
        
        -0.500000,  0.500000,  0.500000, 
        -0.500000,  0.500000, -0.500000,
        -0.500000, -0.500000, -0.500000, 
        -0.500000, -0.500000,  0.500000,
        
        0.000000, 0.000000, 0.500000,
        0.000000, 0.500000, 0.000000,
        0.000000, 0.000000, -0.500000,
        0.000000, -0.500000, 0.000000,
        0.500000, 0.000000, 0.000000,
        -0.500000, 0.000000, 0.000000
         ]
    for i in xrange(len(vertex_template)/3):
        f_out.write('''v %s %s %s\n''' % (pos[0] + CUBE_WIDTH * vertex_template[3*i],
                                          pos[1] + CUBE_WIDTH * vertex_template[3*i + 1],
                                          pos[2] + CUBE_WIDTH * vertex_template[3*i + 2]))
    f_out.write('''vt %s %s\n''' % (tex_step * (ci + 0.5), 1.0))
    f_out.write('''vt %s %s\n''' % (tex_step * (ci + 0.5), 0.0))
    
    index_template = [24, 0, 1,
                      24, 1, 2,
                      24, 2, 3,
                      24, 3, 0,
                      
                      25, 4, 5,
                      25, 5, 6,
                      25, 6, 7,
                      25, 7, 4,
                      
                      26, 8, 9,
                      26, 9, 10,
                      26, 10, 11,
                      26, 11, 8,
                      
                      27, 12, 13,
                      27, 13, 14,
                      27, 14, 15,
                      27, 15, 12,
                      
                      28, 16, 17,
                      28, 17, 18,
                      28, 18, 19,
                      28, 19, 16,
                      
                      29, 20, 21,
                      29, 21, 22,
                      29, 22, 23,
                      29, 23, 20]
    for i in xrange(len(index_template)/3):
        f_out.write('''f %s/%s %s/%s %s/%s\n''' % (n*30+1 +index_template[3*i], 2*n+1, 
                                                   n*30+1 +index_template[3*i + 1], 2*n+2,
                                                   n*30+1 +index_template[3*i + 2], 2*n+2));
                                        
MLT_TEMPLATE = '''newmtl material0
Ka 1.000000 1.000000 1.000000
Kd 1.000000 1.000000 1.000000
Ks 0.000000 0.000000 0.000000
Tr 1.000000
illum 1
Ns 0.000000
map_Kd %s
'''
        
def genMtl(fn):
    fn_mtl = fn +".mtl"
    print fn_mtl
    f_out = open(fn_mtl, "w")
    f_out.write(MLT_TEMPLATE % (path.basename(fn) + ".png"))
    f_out.close()

def genObj(fn):
    #check
    if not path.isfile(fn):
        print "cubefile not exist %s" % fn
        return
    
    print fn
    file_in = open(fn, 'r')
    fn_out = path.join(path.dirname(fn), path.basename(fn)+".obj")
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
    file_out.write('''mtllib %s\n''' % (path.basename(fn) + ".mtl"))
    file_out.write('''usemtl material0\n''')
    for _cube in cubes:
        pos = _cube["pos"]
        ci = _cube["mid"]
        genVertexLinesWithPos(pos, ci, file_out, n)
        n += 1
    
    file_out.close()

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

def genColorMap(fn,fn_mapname):
    if not path.isfile(fn):
        print 'metafile not exists %s' % fn
        return None
    f_in = open(fn, "r")
    data_in = ""
    for _line in f_in.readlines():
        data_in += _line
    jobj = json.loads(data_in)
    
    img = Image.new("RGBA", (TEXTURE_WIDTH,TEXTURE_WIDTH), color=(256,0,0,256))
    draw = ImageDraw.Draw(img)
#     draw.ellipse((25,25,75,75), fill=(255,0,0,100))
    for _meta in jobj["list"]:
        x = _meta["id"]
        color = _meta["color"]
        assert( x >=0 and x < TEXTURE_WIDTH)
        #GL UV coordinate from left-bottom.
        for _y in xrange(TEXTURE_WIDTH):
            draw.point((x, _y), fill=(int(256*color[0]),
                                      int(256*color[1]),
                                      int(256*color[2]),
                                      int(256*color[3])))
    img.save(fn_mapname, 'PNG')

def cube2obj(fn):
    print fn, path.dirname(fn), path.basename(fn)
    fn_meta = path.join(path.dirname(fn), "metacubes.json")
    fn_mapname = fn + ".png"
    genColorMap(fn_meta, fn_mapname)
    genObj(fn)
    genMtl(fn)
    


if __name__ == "__main__":
    if len(sys.argv) == 2:
        fn = sys.argv[1]
        cube2obj(fn)
    elif len(sys.argv) == 3:
        CUBE_WIDTH = float(sys.argv[1])
        cube2obj(sys.argv[2])
    else:
        print "Usage:\n  cube2obj  [CUBE_WIDTH]  xxx.cube"
    pass
    
