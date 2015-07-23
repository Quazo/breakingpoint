# $Id: ipr.py 1315 2015-05-26 17:52:29Z kik $

import os
import ctypes
import platform
import json

from arnold import *

import hou

import htoa
import htoa.log as log

# Delta actions
NONE                       = 0
CREATE                     = 1
UPDATE                     = 2
UPDATE_OBJ                 = 3
UPDATE_FULL                = 4
DELETE                     = 5
TEXTURE_INVALIDATE         = 6
SKYDOME_TEXTURE_INVALIDATE = 7
UNIVERSE_CACHE_FLUSH       = 8

_array_cast = {
                 AI_TYPE_BOOLEAN  : c_bool,
                 AI_TYPE_BYTE     : c_byte,
                 AI_TYPE_FLOAT    : c_float,
                 AI_TYPE_INT      : c_int,
                 AI_TYPE_UINT     : c_uint,
                 AI_TYPE_POINT2   : c_float,
                 AI_TYPE_POINT    : c_float,
                 AI_TYPE_VECTOR   : c_float,
                 AI_TYPE_RGB      : c_float,
                 AI_TYPE_RGBA     : c_float,
                 AI_TYPE_MATRIX   : c_float,
                 AI_TYPE_STRING   : c_char_p,
                 AI_TYPE_ENUM     : c_int,
                 AI_TYPE_NODE     : c_void_p,
#                  AI_TYPE_ARRAY    : None,
#                  AI_TYPE_POINTER  : None,
#                  AI_TYPE_NONE     : None,
#                  AI_TYPE_UNDEFINED: None,
               }

_array_cardinality = {
                        AI_TYPE_BOOLEAN  : 1,
                        AI_TYPE_BYTE     : 1,
                        AI_TYPE_FLOAT    : 1,
                        AI_TYPE_INT      : 1,
                        AI_TYPE_UINT     : 1,
                        AI_TYPE_POINT2   : 2,
                        AI_TYPE_POINT    : 3,
                        AI_TYPE_VECTOR   : 3,
                        AI_TYPE_RGB      : 3,
                        AI_TYPE_RGBA     : 4,
                        AI_TYPE_MATRIX   : 16,
                        AI_TYPE_STRING   : 1,
                        AI_TYPE_ENUM     : 1,
                        AI_TYPE_NODE     : 1,
#                         AI_TYPE_ARRAY    : None,
#                         AI_TYPE_POINTER  : None,
#                         AI_TYPE_NONE     : None,
#                         AI_TYPE_UNDEFINED: None,
                      }

_array_element = { 
                   AI_TYPE_BOOLEAN  : lambda x: x,
                   AI_TYPE_BYTE     : lambda x: x,
                   AI_TYPE_FLOAT    : lambda x: x,
                   AI_TYPE_INT      : lambda x: x,
                   AI_TYPE_UINT     : lambda x: x,
                   AI_TYPE_POINT2   : lambda x: x,
                   AI_TYPE_POINT    : lambda x: x,
                   AI_TYPE_VECTOR   : lambda x: x,
                   AI_TYPE_RGB      : lambda x: x,
                   AI_TYPE_RGBA     : lambda x: x,
                   AI_TYPE_MATRIX   : lambda x: x,
                   AI_TYPE_STRING   : lambda x: x,
                   AI_TYPE_ENUM     : lambda x: x,
                   AI_TYPE_NODE     : lambda x: AiNodeGetName(x),
#                    AI_TYPE_ARRAY    : None,
#                    AI_TYPE_POINTER  : None,
#                    AI_TYPE_NONE     : None,
#                    AI_TYPE_UNDEFINED: None,
                 }

def _parmDefaultArray(parm_entry):
    array = AiParamGetDefault(parm_entry).contents.ARRAY.contents
    return [_array_element[array.type](cast(array.data, POINTER(_array_cast[array.type]))[i]) for i in xrange(array.nkeys * array.nelements * _array_cardinality[array.type])]

_parm_default_function = { 
                           AI_TYPE_BOOLEAN  : lambda x: AiParamGetDefault(x).contents.BOOL,
                           AI_TYPE_BYTE     : lambda x: AiParamGetDefault(x).contents.BYTE,
                           AI_TYPE_FLOAT    : lambda x: AiParamGetDefault(x).contents.FLT,
                           AI_TYPE_INT      : lambda x: AiParamGetDefault(x).contents.INT,
                           AI_TYPE_UINT     : lambda x: AiParamGetDefault(x).contents.UINT,
                           AI_TYPE_POINT2   : lambda x: [AiParamGetDefault(x).contents.PNT.__getattribute__(c) for c in ('x', 'y')],
                           AI_TYPE_POINT    : lambda x: [AiParamGetDefault(x).contents.PNT.__getattribute__(c) for c in ('x', 'y', 'z')],
                           AI_TYPE_VECTOR   : lambda x: [AiParamGetDefault(x).contents.VEC.__getattribute__(c) for c in ('x', 'y', 'z')],
                           AI_TYPE_RGB      : lambda x: [AiParamGetDefault(x).contents.RGB.__getattribute__(c) for c in ('r', 'g', 'b')],
                           AI_TYPE_RGBA     : lambda x: [AiParamGetDefault(x).contents.RGBA.__getattribute__(c) for c in ('r', 'g', 'b', 'a')],
                           AI_TYPE_MATRIX   : lambda x: [AiParamGetDefault(x).contents.pMTX.__getattribute__(c) for c in ['a' + str(i) + str(j) for i in xrange(4) for j in xrange(4)]],
                           AI_TYPE_STRING   : lambda x: AiParamGetDefault(x).contents.STR,
                           AI_TYPE_ENUM     : lambda x: AiEnumGetString(AiParamGetEnum(x), AiParamGetDefault(x).contents.INT),
                           AI_TYPE_ARRAY    : lambda x: _parmDefaultArray(x),
                           AI_TYPE_POINTER  : lambda x: None,
                           AI_TYPE_NODE     : lambda x: None,
                           AI_TYPE_NONE     : lambda x: None,
                           AI_TYPE_UNDEFINED: lambda x: None,
                         }

def parmDefault(parm_entry):
    return _parm_default_function[AiParamGetType(parm_entry)](parm_entry)

def _parmGetMatrix(node, parm):
    '''Get MATRIX value as a list'''
    mtx = AtMatrix()
    AiNodeGetMatrix(node, parm, mtx)
    return [mtx.__getattribute__(c) for c in ['a' + str(i) + str(j) for i in xrange(4) for j in xrange(4)]]

def _parmGetArray(node, parm):
    array = AiNodeGetArray(node, parm).contents
    value = {}
    value['nkeys'] = array.nkeys
    value['nelts'] = array.nelements
    value['type'] = array.type
    value['data'] = [_array_element[array.type](cast(array.data, POINTER(_array_cast[array.type]))[i]) for i in xrange(array.nkeys * array.nelements * _array_cardinality[array.type])]
    return value

_parm_get = { 
              AI_TYPE_BOOLEAN  : lambda node, parm: AiNodeGetBool(node, parm),
              AI_TYPE_BYTE     : lambda node, parm: AiNodeGetByte(node, parm),
              AI_TYPE_FLOAT    : lambda node, parm: AiNodeGetFlt (node, parm),
              AI_TYPE_INT      : lambda node, parm: AiNodeGetInt (node, parm),
              AI_TYPE_UINT     : lambda node, parm: AiNodeGetUInt(node, parm),
              AI_TYPE_STRING   : lambda node, parm: AiNodeGetStr (node, parm),
              AI_TYPE_ENUM     : lambda node, parm: AiNodeGetStr (node, parm),
              AI_TYPE_NODE     : lambda node, parm: AiNodeGetName(cast(AiNodeGetPtr(node, parm), POINTER(AtNode))),
              AI_TYPE_MATRIX   : lambda node, parm: _parmGetMatrix(node, parm),
              AI_TYPE_POINT2   : lambda node, parm: [v.__getattribute__(c) for v in [AiNodeGetPnt2(node, parm)] for c in ('x', 'y')],
              AI_TYPE_POINT    : lambda node, parm: [v.__getattribute__(c) for v in [AiNodeGetPnt (node, parm)] for c in ('x', 'y', 'z')],
              AI_TYPE_VECTOR   : lambda node, parm: [v.__getattribute__(c) for v in [AiNodeGetVec (node, parm)] for c in ('x', 'y', 'z')],
              AI_TYPE_RGB      : lambda node, parm: [v.__getattribute__(c) for v in [AiNodeGetRGB (node, parm)] for c in ('r', 'g', 'b')],
              AI_TYPE_RGBA     : lambda node, parm: [v.__getattribute__(c) for v in [AiNodeGetRGBA(node, parm)] for c in ('r', 'g', 'b', 'a')],
              AI_TYPE_ARRAY    : lambda node, parm: _parmGetArray(node, parm),
              AI_TYPE_NONE     : lambda node, parm: None,
              AI_TYPE_POINTER  : lambda node, parm: None,
              AI_TYPE_UNDEFINED: lambda node, parm: None,
            }

def parmGet(node, parm, arnold_type):
    return _parm_get[arnold_type](node, parm)

def delta(node, action=UPDATE_FULL, skip=[]):
    '''Return a delta representing the node
    '''
    node_entry = AiNodeGetNodeEntry(node)
    parm_iter = AiNodeEntryGetParamIterator(node_entry)
    parameters = {}

    while not AiParamIteratorFinished(parm_iter):
        parm_entry = AiParamIteratorGetNext(parm_iter)
        parm_name = AiParamGetName(parm_entry)
        if parm_name in skip:
            continue
        
        arnold_type = AiParamGetType(parm_entry)
        value = parmGet(node, parm_name, arnold_type)
        
        # skip setting the parameter if its value is default
        if action == CREATE and value == parmDefault(parm_entry):
            continue
            
        # add the parameter
        parameters[parm_name] = { 'type': arnold_type, 'value': value }
    
    # build the delta
    delta = {}
    delta['action'] = action
    delta['entry'] = AiNodeEntryGetName(node_entry)
    delta['name'] = AiNodeGetName(node)
    delta['parameters'] = parameters
    return delta

# expose some htoa_ipr dso functions
dso_prefix = {'windows': '', 'linux': 'lib', 'darwin': 'lib'}
dso_extension = {'windows': '.dll', 'linux': '.so', 'darwin': '.dylib'}

os_name = platform.system().lower()
dso_path = os.path.join(htoa.folder, 'scripts', 'bin',  '%shtoa_ipr%s' % (dso_prefix[os_name], dso_extension[os_name]))
ipr_dso = ctypes.CDLL(dso_path)

ipr_dso.HaDeltaPublisherPort.restype = ctypes.c_int
    
def deltaPublisherPort():
    return ipr_dso.HaDeltaPublisherPort()

ipr_dso.HaDeltaPublisherSend.argtypes = [ctypes.c_char_p]
ipr_dso.HaDeltaPublisherSend.restype = ctypes.c_int

def deltaPublisherSend(msg):
    return ipr_dso.HaDeltaPublisherSend(msg)

def publish(json_delta):
    deltaPublisherSend(json.dumps(json_delta))
    
def textureInvalidate(filename):
    '''Invalidate a texture by filename
    '''
    delta = {}
    delta['action'] = TEXTURE_INVALIDATE
    delta['parameters'] = {'filename': {'type': AI_TYPE_STRING, 'value': filename}}
    publish(delta)
    
def skydomeTextureInvalidate(filename):
    ''' Invalidate a skydome texture by filename. This is different from
    textureInvalidate() because you need to also invalidate the skydome
    importance tables.
    '''
    delta = {}
    delta['action'] = SKYDOME_TEXTURE_INVALIDATE
    delta['parameters'] = {'filename': {'type': AI_TYPE_STRING, 'value': filename}}
    publish(delta)

def universeCacheFlush(cache_flags):
    '''Invalidate Arnold caches as per AiUniverseCacheFlush()
    '''
    delta = {}
    delta['action'] = UNIVERSE_CACHE_FLUSH
    delta['parameters'] = {'cache_flags': {'type': AI_TYPE_INT, 'value': cache_flags}}
    publish(delta)
