#!/usr/bin/env python

import os
import ctypes
import platform
import hou
import htoa

_libext = {'windows'  :'.dll',
           'microsoft':'.dll',
           'linux'    :'.so',
           'darwin'   :'.dylib'}

try:
    dso_path = os.path.join(htoa.folder, 'arnold', 'plugins', 'volume_vdb' + _libext[platform.system().lower()])
    volume_vdb_dso = ctypes.CDLL(dso_path)
    volume_vdb_dso.vdbGridNames.argtypes = [ctypes.c_char_p]
    volume_vdb_dso.vdbGridNames.restype = ctypes.c_char_p
    volume_vdb_dso.vdbGridBounds.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    volume_vdb_dso.vdbGridBounds.restype = ctypes.c_char_p
except:
    volume_vdb_dso = None
    
def gridMenu(filename):
    if not volume_vdb_dso:
        return []
    
    gridnames = volume_vdb_dso.vdbGridNames(filename).split()
    return [x for y in zip(gridnames, gridnames) for x in y]

def gridBounds(filename, gridname):
    if not volume_vdb_dso:
        return []
    
    return [float(x) for x in volume_vdb_dso.vdbGridBounds(filename, gridname).split()]
