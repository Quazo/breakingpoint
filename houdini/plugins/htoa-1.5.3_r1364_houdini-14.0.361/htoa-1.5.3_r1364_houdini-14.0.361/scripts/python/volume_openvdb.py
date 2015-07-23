#!/usr/bin/env python

import os
import ctypes
import platform
import hou
from arnold import *
import htoa

_libext = {'windows'  :'.dll',
           'microsoft':'.dll',
           'linux'    :'.so',
           'darwin'   :'.dylib'}

try:
    dso_path = os.path.join(htoa.folder, 'arnold', 'procedurals', htoa.dso_prefix + 'volume_openvdb' + _libext[platform.system().lower()])
    dso = ctypes.CDLL(dso_path)
    
    dso.channelNames.argtypes = [ctypes.c_char_p]
    dso.channelNames.restype = POINTER(AtArray)
    
    dso.channelBBox.argtypes = [ctypes.c_char_p, POINTER(AtArray)]
    dso.channelBBox.restype = AtBBox
    
    dso.minVoxelSize.argtypes = [ctypes.c_char_p, POINTER(AtArray)]
    dso.minVoxelSize.restype = ctypes.c_float
except:
    dso = None
    
def channelMenu(filename):
    if not dso:
        return []
    
    channel_array = dso.channelNames(filename)
    channel_names = [AiArrayGetStr(channel_array, i) for i in xrange(channel_array.contents.nelements)]
    return [x for y in zip(channel_names, channel_names) for x in y]

def channelBounds(filename, channel_names):
    if not dso:
        return []
    
    # space separated names is acceptable
    if isinstance(channel_names, basestring):
        channel_names = channel_names.split()
    
    # expand list with clusters that match the beginning of the grid name
    all_channel_array = dso.channelNames(filename)
    all_channel_names = [AiArrayGetStr(all_channel_array, i) for i in xrange(all_channel_array.contents.nelements)]

    for chan in channel_names:
        channel_names.extend(filter(lambda x: x != chan and x.startswith(chan), all_channel_names))
    
    channel_array = AiArrayAllocate(len(channel_names), 1, AI_TYPE_STRING)
    for i in xrange(channel_array.contents.nelements):
        AiArraySetStr(channel_array, i, channel_names[i])
    
    bbox = dso.channelBBox(filename, channel_array)
    return [bbox.min.x, bbox.min.y, bbox.min.z, bbox.max.x, bbox.max.y, bbox.max.z]

def autoStepSizeCallback():
    if hou.parm('ar_step_size_type').evalAsString() != 'auto':
        return
    
    filename = hou.parm('ar_filename').evalAsString()
    channel_names = hou.parm('ar_grids').evalAsString().split()

    channel_array = AiArrayAllocate(len(channel_names), 1, AI_TYPE_STRING)
    for i in xrange(channel_array.contents.nelements):
        AiArraySetStr(channel_array, i, channel_names[i])

    voxel_size = dso.minVoxelSize(filename, channel_array)
    hou.parm('ar_step_size').set(voxel_size if voxel_size != 0 else 0.02)
    