# $Id: parms.py 964 2014-09-15 13:59:12Z kik $

from arnold import *

## Global flag to force the setting of parameters 
HA_NODE_FORCE_SET = False

## Function map for HaArrayGet()
_array_get_function = { AI_TYPE_BYTE    : AiArrayGetByte,
                        AI_TYPE_INT     : AiArrayGetInt,
                        AI_TYPE_UINT    : AiArrayGetUInt,
                        AI_TYPE_BOOLEAN : AiArrayGetBool,
                        AI_TYPE_FLOAT   : AiArrayGetFlt,
                        AI_TYPE_RGB     : AiArrayGetRGB,
                        AI_TYPE_RGBA    : AiArrayGetRGBA,
                        AI_TYPE_VECTOR  : AiArrayGetVec,
                        AI_TYPE_POINT   : AiArrayGetPnt,
                        AI_TYPE_POINT2  : AiArrayGetPnt2,
                        AI_TYPE_STRING  : AiArrayGetStr,
                        AI_TYPE_POINTER : AiArrayGetPtr,
                        AI_TYPE_NODE    : AiArrayGetPtr,
                        AI_TYPE_ARRAY   : AiArrayGetArray,
                        AI_TYPE_ENUM    : AiArrayGetInt }

def HaArrayGet(array, i):
    if array.type == AI_TYPE_MATRIX:
        mtx = AtMatrix()
        AiArrayGetMtx(array, i, mtx)
        return mtx
    
    return _array_get_function[array.type](array, i)
    
def HaArrayConvertFloat(samples):
    '''Convert a float list into an Arnold array'''
    return AiArrayConvert(1, len(samples), AI_TYPE_FLOAT, (c_float*len(samples))(*samples))

def HaNodeGetDefault(node, parm):
    node_entry = AiNodeGetNodeEntry(node)
    parm_entry = AiNodeEntryLookUpParameter(node_entry, parm)
    parm_default = AiParamGetDefault(parm_entry)
    if parm_default:
        return parm_entry, parm_default.contents
    else:
        return parm_entry, None

def HaNodeSetByte(node, parm, value, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetByte(node, parm, value)
        return
    
    parm_entry, def_value = HaNodeGetDefault(node, parm)
    
    # parameter is an array
    if AiParamGetType(parm_entry) == AI_TYPE_ARRAY:
        array = def_value.ARRAY.contents
        if array.nelements == array.nkeys == 1 and value == HaArrayGet(array, 0):
            return
        
    # check default value
    if def_value and value == def_value.BYTE: return
    AiNodeSetByte(node, parm, value)
    
def HaNodeSetInt(node, parm, value, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetInt(node, parm, value)
        return
    
    parm_entry, def_value = HaNodeGetDefault(node, parm)
    
    # parameter is an array
    if AiParamGetType(parm_entry) == AI_TYPE_ARRAY:
        array = def_value.ARRAY.contents
        if array.nelements == array.nkeys == 1 and value == HaArrayGet(array, 0):
            return
        
    # check default value
    if def_value and value == def_value.INT: return
    AiNodeSetInt(node, parm, value)
    
def HaNodeSetUInt(node, parm, value, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetUInt(node, parm, value)
        return
    
    parm_entry, def_value = HaNodeGetDefault(node, parm)
    
    # parameter is an array
    if AiParamGetType(parm_entry) == AI_TYPE_ARRAY:
        array = def_value.ARRAY.contents
        if array.nelements == array.nkeys == 1 and value == HaArrayGet(array, 0):
            return
        
    # check default value
    if def_value and value == def_value.UINT: return
    AiNodeSetUInt(node, parm, value)
    
def HaNodeSetBool(node, parm, value, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetBool(node, parm, value)
        return
    
    parm_entry, def_value = HaNodeGetDefault(node, parm)
    
    # parameter is an array
    if AiParamGetType(parm_entry) == AI_TYPE_ARRAY:
        array = def_value.ARRAY.contents
        if array.nelements == array.nkeys == 1 and value == HaArrayGet(array, 0):
            return
        
    # check default value
    if def_value and value == def_value.BOOL: return
    AiNodeSetBool(node, parm, value)
    
def HaNodeSetFlt(node, parm, value, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetFlt(node, parm, value)
        return

    parm_entry, def_value = HaNodeGetDefault(node, parm)
    
    # parameter is an array
    if AiParamGetType(parm_entry) == AI_TYPE_ARRAY:
        array = def_value.ARRAY.contents
        if array.nelements == array.nkeys == 1 and value == HaArrayGet(array, 0):
            return
        
    # check default value
    if def_value and value == def_value.FLT: return
    AiNodeSetFlt(node, parm, value)
    
def HaNodeSetRGB(node, parm, r, g, b, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetRGB(node, parm, r, g, b)
        return
    
    parm_entry, def_value = HaNodeGetDefault(node, parm)
    
    # parameter is an array
    if AiParamGetType(parm_entry) == AI_TYPE_ARRAY:
        array = def_value.ARRAY.contents
        if array.nelements == array.nkeys == 1 and AtRGB(r, g, b) == HaArrayGet(array, 0):
            return
        
    # check default value
    if def_value and AtRGB(r, g, b) == def_value.RGB: return
    AiNodeSetRGB(node, parm, r, g, b)
    
def HaNodeSetRGBA(node, parm, r, g, b, a, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetRGBA(node, parm, r, g, b, a)
        return
    
    parm_entry, def_value = HaNodeGetDefault(node, parm)
    
    # parameter is an array
    if AiParamGetType(parm_entry) == AI_TYPE_ARRAY:
        array = def_value.ARRAY.contents
        if array.nelements == array.nkeys == 1 and AtRGBA(r, g, b, a) == HaArrayGet(array, 0):
            return
        
    # check default value
    if def_value and AtRGBA(r, g, b, a) == def_value.RGBA: return
    AiNodeSetRGBA(node, parm, r, g, b, a)
    
def HaNodeSetVec(node, parm, x, y, z, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetVec(node, parm, x, y, z)
        return
    
    parm_entry, def_value = HaNodeGetDefault(node, parm)
    
    # parameter is an array
    if AiParamGetType(parm_entry) == AI_TYPE_ARRAY:
        array = def_value.ARRAY.contents
        if array.nelements == array.nkeys == 1 and AtVector(x, y, z) == HaArrayGet(array, 0):
            return
        
    # check default value
    if def_value and AtVector(x, y, z) == def_value.VEC: return
    AiNodeSetVec(node, parm, x, y, z)
    
def HaNodeSetPnt(node, parm, x, y, z, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetPnt(node, parm, x, y, z)
        return
    
    parm_entry, def_value = HaNodeGetDefault(node, parm)
    
    # parameter is an array
    if AiParamGetType(parm_entry) == AI_TYPE_ARRAY:
        array = def_value.ARRAY.contents
        if array.nelements == array.nkeys == 1 and AtPoint(x, y, z) == HaArrayGet(array, 0):
            return
        
    # check default value
    if def_value and AtPoint(x, y, z) == def_value.PNT: return
    AiNodeSetPnt(node, parm, x, y, z)
    
def HaNodeSetPnt2(node, parm, x, y, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetPnt2(node, parm, x, y)
        return
    
    parm_entry, def_value = HaNodeGetDefault(node, parm)
    
    # parameter is an array
    if AiParamGetType(parm_entry) == AI_TYPE_ARRAY:
        array = def_value.ARRAY.contents
        if array.nelements == array.nkeys == 1 and AtPoint2(x, y) == HaArrayGet(array, 0):
            return
        
    # check default value
    if def_value and AtPoint2(x, y) == def_value.PNT2: return
    AiNodeSetPnt2(node, parm, x, y)
    
def HaNodeSetStr(node, parm, value, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetStr(node, parm, value)
        return
    
    parm_entry, def_value = HaNodeGetDefault(node, parm)
    
    if def_value:
        parm_type = AiParamGetType(parm_entry)

        if parm_type == AI_TYPE_ARRAY:
            array = def_value.ARRAY.contents
            if array.nelements == array.nkeys == 1 and value == HaArrayGet(array, 0):
                return

        elif parm_type == AI_TYPE_ENUM:
            def_value = AiEnumGetString(AiParamGetEnum(parm_entry), def_value.INT)
        
        else:
            assert parm_type == AI_TYPE_STRING
            def_value = def_value.STR
    
    if value == def_value: return
    AiNodeSetStr(node, parm, value)
    
def HaNodeSetPtr(node, parm, value, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetPtr(node, parm, value)
        return
    
    parm_entry, def_value = HaNodeGetDefault(node, parm)
    
    # parameter is an array
    if AiParamGetType(parm_entry) == AI_TYPE_ARRAY:
        array = def_value.ARRAY.contents
        if array.nelements == array.nkeys == 1 and value == HaArrayGet(array, 0):
            return
        
    # check default value
    if def_value and value == def_value.PTR: return
    AiNodeSetPtr(node, parm, value)
    
def HaNodeSetArray(node, parm, value, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetArray(node, parm, value)
        return
    
    parm_entry, def_value = HaNodeGetDefault(node, parm)
        
    # both value and default are arrays
    if AiParamGetType(parm_entry) == AI_TYPE_ARRAY and type(value.contents) is AtArray:
        
        # both value and default are matrix arrays
        if def_value.ARRAY.contents.type == value.contents.type == AI_TYPE_MATRIX:
            
            # an empty matrix array means the identity 
            if def_value.ARRAY.contents.nelements == 0 and AiM4IsIdentity(HaArrayGet(value.contents, 0)):
                return
            
            # address the case of single element default and value arrays
            elif (def_value.ARRAY.contents.nelements == value.contents.nelements ==
                  def_value.ARRAY.contents.nkeys     == value.contents.nkeys     == 1
                  and
                  HaArrayGet(def_value.ARRAY.contents, 0).__reduce__() == HaArrayGet(value.contents, 0).__reduce__()):
                return
            
        # address the case of single element default and value arrays
        elif (def_value.ARRAY.contents.nelements == value.contents.nelements ==
              def_value.ARRAY.contents.nkeys     == value.contents.nkeys     == 1
              and
              HaArrayGet(def_value.ARRAY.contents, 0) == HaArrayGet(value.contents, 0)):
            return
        
    AiNodeSetArray(node, parm, value)
    
def HaNodeSetMatrix(node, parm, value, force_set=False):
    if force_set or HA_NODE_FORCE_SET:
        AiNodeSetMatrix(node, parm, value)
        return
    
    parm_entry, def_value = HaNodeGetDefault(node, parm)
    
    # parameter is an array
    if AiParamGetType(parm_entry) == AI_TYPE_ARRAY:
        array = def_value.ARRAY.contents
        if array.nelements == array.nkeys == 1 and value.__reduce__() == HaArrayGet(array, 0).__reduce__():
            return
        
    # check default value
    if def_value and value.__reduce__() == def_value.pMTX.contents.__reduce__(): return
    AiNodeSetMatrix(node, parm, value)
