#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
(C) 2015 Turnro.com

build_units.py, automatic generate metaunits.json for TurnroGmapEditor.
Internally, it will compare the current metaunits.json file and the units files there,
new unit file will be added into it, deleted unit will be deleted from metaunits.json.

Put this file at the base folder of TurnroGmapEditor's workspace.
'''
import sys
import json
import os.path as path
import os
from pip._vendor.distlib.metadata import _LINE_PREFIX

def readOutOldMeta(basePath):
    f_meta = open(path.join(basePath, "metaunits.json"), "r")
    data_lines = f_meta.readlines()
    whole_line = ""
    for _line in data_lines:
        whole_line += _line

    f_meta.close()
    jobj = json.loads(whole_line)
    return jobj

def findOutMaxId(old_meta):
    max_id = 0
    for _unit in old_meta["units"]:
        max_id = max(max_id, _unit["uid"])
    return max_id

def searchFunc(arg, dirname, filenames):
    if dirname[-5:] == "units":
        for _file_name in filenames:
            if ".c3b" in _file_name:
                _obj = {}
                _obj["file"] = "units/"+_file_name
                arg["units"].append(_obj)

def searchOutNewMeta(basePath):
    jobj = {}
    jobj["units"] = []
    path.walk(basePath, searchFunc, jobj)
    return jobj
    
def build(basePath):
    
    old_meta = readOutOldMeta(basePath)
    next_id = findOutMaxId(old_meta) + 1
    new_meta = searchOutNewMeta(basePath)
    for _old_unit in old_meta["units"]:
        for _new_unit in new_meta["units"]:
            if _new_unit["file"] == _old_unit["file"]:
                _new_unit["uid"] = _old_unit["uid"]
                _new_unit["scale"] = _old_unit["scale"]
                _new_unit["face"] = _old_unit["face"]
                if "unreal" in _old_unit:
                    _new_unit["unreal"] = _old_unit["unreal"]

    for _new_unit in new_meta["units"]:
        if "uid" in _new_unit:
            pass
        else:
            _new_unit["uid"] = next_id
            next_id = next_id + 1
            _new_unit["face"] = 0
            _new_unit["unreal"] = 0
            _new_unit["scale"] = 0.1
    new_meta_data = json.dumps(new_meta, indent = True)
    f_out = open(path.join(basePath, "metaunits.json"), "w")
    f_out.write(new_meta_data)
    print new_meta_data
    f_out.close()

if __name__ == "__main__":
    basePath = '''/Users/chenbingfeng/Documents/TurnroGmapEditor'''
    build(basePath)
    pass

