# $Id: node.py 1358 2015-06-15 16:39:12Z kik $

from arnold import *
import htoa.log as log
from htoa.node.parms import *
import htoa

import hou

## Houdini parameter names prefix
HA_PARM_PREFIX = 'ar_'

## Prefix name with HA_PARM_PREFIX
def HA_PREFIX(name):
    return HA_PARM_PREFIX + name

## Houdini friendly Arnold default values
HA_DEFVALUE = { AI_TYPE_ARRAY    : lambda x: None,
                AI_TYPE_BOOLEAN  : lambda x: int(AiParamGetDefault(x).contents.BOOL),
                AI_TYPE_BYTE     : lambda x: AiParamGetDefault(x).contents.BYTE,
                AI_TYPE_ENUM     : lambda x: AiEnumGetString(AiParamGetEnum(x), AiParamGetDefault(x).contents.INT),
                AI_TYPE_FLOAT    : lambda x: AiParamGetDefault(x).contents.FLT,
                AI_TYPE_INT      : lambda x: AiParamGetDefault(x).contents.INT,
                AI_TYPE_MATRIX   : lambda x: AiParamGetDefault(x).contents.pMTX,
                AI_TYPE_NODE     : lambda x: None,
                AI_TYPE_NONE     : None,
                AI_TYPE_POINT2   : lambda x: [AiParamGetDefault(x).contents.PNT.__getattribute__(c) for c in 'x y'.split()],
                AI_TYPE_POINT    : lambda x: [AiParamGetDefault(x).contents.PNT.__getattribute__(c) for c in 'x y z'.split()],
                AI_TYPE_POINTER  : None,
                AI_TYPE_RGB      : lambda x: [AiParamGetDefault(x).contents.RGB.__getattribute__(c) for c in 'r g b'.split()],
                AI_TYPE_RGBA     : lambda x: [AiParamGetDefault(x).contents.RGBA.__getattribute__(c) for c in 'r g b a'.split()],
                AI_TYPE_STRING   : lambda x: AiParamGetDefault(x).contents.STR,
                AI_TYPE_UINT     : lambda x: AiParamGetDefault(x).contents.UINT,
                AI_TYPE_UNDEFINED: None,
                AI_TYPE_VECTOR   : lambda x: [AiParamGetDefault(x).contents.VEC.__getattribute__(c) for c in 'x y z'.split()] }

def nodeSetUnhandled(node, name, value):
    '''Dummy function for unhandled Arnold parameter types'''
    log.error('Unhandled parameter: node=%s, name=%s, value=%s' % (AiNodeGetName(node), name, repr(value)))
    
def nodeSetRGB(node, name, value):
    '''Set RGB value'''
    AiNodeSetRGB(node, name, value[0], value[1], value[2])

def nodeSetRGBA(node, name, value):
    '''Set RGBA value'''
    AiNodeSetRGBA(node, name, value[0], value[1], value[2], value[3])
    
def nodeSetPnt2(node, name, value):
    '''Set POINT2 value'''
    AiNodeSetPnt2(node, name, value[0], value[1])
    
def nodeSetPnt(node, name, value):
    '''Set POINT value'''
    AiNodeSetPnt(node, name, value[0], value[1], value[2])
    
def nodeSetVec(node, name, value):
    '''Set VECTOR value'''
    AiNodeSetVec(node, name, value[0], value[1], value[2])
    
def nodeSetNode(node, name, value):
    '''Set NODE value'''
    AiNodeSetPtr(node, name, AiNodeLookUpByName(value))
    
def nodeSetMatrix(node, name, value):
    '''Set MATRIX value'''
    AiNodeSetMatrix(node, name, AtMatrix(value[0], value[1], value[2], value[3],
                                         value[4], value[5], value[6], value[7],
                                         value[8], value[9], value[10], value[11],
                                         value[12], value[13], value[14], value[15]))
    
def evalUnhandled(prop_name):
    '''Dummy property getter for unhandled Arnold types'''
    log.error('Unhandled parameter type for %s' % prop_name)

def getNodeEntry(node):
    '''Arnold 3 compatible AiNodeGetNodeEntry()
    @deprecated: Use AiNodeGetNodeEntry() as Arnold 3 support has ended
    '''
    if int(AiGetVersion()[0]) < 4:
        return node.contents.base_node
    else:
        return AiNodeGetNodeEntry(node)

## Map Arnold AiNodeSet functions to type
arnoldParmSet = {AI_TYPE_ARRAY:     nodeSetUnhandled, # TODO
                 AI_TYPE_BOOLEAN:   AiNodeSetBool,
                 AI_TYPE_BYTE:      AiNodeSetByte,
                 AI_TYPE_ENUM:      AiNodeSetStr,
                 AI_TYPE_FLOAT:     AiNodeSetFlt,
                 AI_TYPE_INT:       AiNodeSetInt,
                 AI_TYPE_MATRIX:    nodeSetMatrix,
                 AI_TYPE_NODE:      nodeSetNode,
                 AI_TYPE_NONE:      nodeSetUnhandled,
                 AI_TYPE_POINT2:    nodeSetPnt2,
                 AI_TYPE_POINT:     nodeSetPnt,
                 AI_TYPE_POINTER:   nodeSetUnhandled,
                 AI_TYPE_RGB:       nodeSetRGB,
                 AI_TYPE_RGBA:      nodeSetRGBA,
                 AI_TYPE_STRING:    AiNodeSetStr,
                 AI_TYPE_UINT:      AiNodeSetUInt,
                 AI_TYPE_UNDEFINED: nodeSetUnhandled,
                 AI_TYPE_VECTOR:    nodeSetVec}

## Parameter evaluation dict for HaNode.pullHouParms()
houdiniParmGet = {AI_TYPE_ARRAY    : lambda n, x, f: log.error('Unhandled parameter of type ARRAY: %s/%s' % (n.path(), x)), # TODO
                  AI_TYPE_BOOLEAN  : lambda n, x, f: n.parm(x).evalAsIntAtFrame(f),
                  AI_TYPE_BYTE     : lambda n, x, f: n.parm(x).evalAsIntAtFrame(f),
                  AI_TYPE_ENUM     : lambda n, x, f: n.parm(x).evalAsStringAtFrame(f),
                  AI_TYPE_FLOAT    : lambda n, x, f: n.parm(x).evalAsFloatAtFrame(f),
                  AI_TYPE_INT      : lambda n, x, f: n.parm(x).evalAsIntAtFrame(f),
                  AI_TYPE_MATRIX   : lambda n, x, f: n.parmTuple(x).evalAsFloatsAtFrame(f),
                  AI_TYPE_NODE     : lambda n, x, f: n.parm(x).evalAsStringAtFrame(f),
                  AI_TYPE_NONE     : lambda n, x, f: log.error('Unhandled parameter of type NONE: %s/%s' % (n.path(), x)),
                  AI_TYPE_POINT2   : lambda n, x, f: n.parmTuple(x).evalAsFloatsAtFrame(f),
                  AI_TYPE_POINT    : lambda n, x, f: n.parmTuple(x).evalAsFloatsAtFrame(f),
                  AI_TYPE_POINTER  : lambda n, x, f: log.error('Unhandled parameter of type POINTER: %s/%s' % (n.path(), x)),
                  AI_TYPE_RGB      : lambda n, x, f: n.parmTuple(x).evalAsFloatsAtFrame(f),
                  AI_TYPE_RGBA     : lambda n, x, f: n.parmTuple(x).evalAsFloatsAtFrame(f),
                  AI_TYPE_STRING   : lambda n, x, f: n.parm(x).evalAsStringAtFrame(f),
                  AI_TYPE_UINT     : lambda n, x, f: n.parm(x).evalAsIntAtFrame(f),
                  AI_TYPE_UNDEFINED: lambda n, x, f: log.error('Unhandled parameter of type UNDEFINED: %s/%s' % (n.path(), x)),
                  AI_TYPE_VECTOR   : lambda n, x, f: n.parmTuple(x).evalAsFloatsAtFrame(f)}

_visibility_bits = {'camera':     AI_RAY_CAMERA,
                    'shadow':     AI_RAY_SHADOW,
                    'reflection': AI_RAY_REFLECTED,
                    'refraction': AI_RAY_REFRACTED,
                    'diffuse':    AI_RAY_DIFFUSE,
                    'glossy':     AI_RAY_GLOSSY}

def visibility(ha_object, prefix='ar_visibility_', defmask=AI_RAY_ALL):
    vis_mask = defmask
    
    for p in _visibility_bits:
        parm_name = prefix + p
        if ha_object.hou_node.parm(parm_name):
            if ha_object.iprop(parm_name):
                vis_mask |= _visibility_bits[p]
            else:
                vis_mask &= ~_visibility_bits[p]
            
    return vis_mask
    
def rayVisibility(ha_object):
    defmask = AI_RAY_ALL & ~AI_RAY_CAMERA if ha_object.isPhantom() else AI_RAY_ALL
    vismask = visibility(ha_object, defmask=defmask)
    
    if ha_object.isForcedPhantom():
        vismask &= ~AI_RAY_CAMERA
    
    return vismask
    
def autobumpVisibility(ha_object):
    return visibility(ha_object, prefix='ar_autobump_visibility_',
                      defmask=AI_RAY_ALL & ~(AI_RAY_DIFFUSE | AI_RAY_GLOSSY))
    
def sidedness(ha_object):
    return visibility(ha_object, prefix='ar_sidedness_')

def isBlacklisted(node_entry, parm):
    '''Check if a parameter is blacklisted from its metadata
    '''
    res = POINTER(c_bool)(c_bool(False))
    if AiMetaDataGetBool(node_entry, parm, 'blacklist', res):
        return res.contents.value
    else:
        return False
    
def isOptional(node_entry, parm):
    '''Check if a parameter is optional from its metadata
    '''
    res = POINTER(c_bool)(c_bool(False))
    if AiMetaDataGetBool(node_entry, parm, 'optional', res):
        return res.contents.value
    else:
        return False
    
def isOverridable(node_entry, parm):
    '''Check if a parameter is overridable from its metadata
    '''
    res = POINTER(c_bool)(c_bool(False))
    if AiMetaDataGetBool(node_entry, parm, 'overridable', res):
        return res.contents.value
    else:
        return False
    
def houdiniParmName(node_entry, parm, prefix=HA_PARM_PREFIX):
    '''Return the corresponding Houdini parameter name for an Arnold parameter.
    
    This function will query metadata on the Arnold parameters and look for a 
    "remap" string metadata entry for the parmeter. If such metadata is found,
    it will be returned. If not the parameter name is returned, with an
    optional prefix.
    
    @param node_entry: an Arnold node entry
    @param parm: an Arnold parameter
    @param prefix: a string to prefix the resulting parameter name. This prefix
    is not applied if a remap entry was found in the metatdata.
    ''' 
    remap = POINTER(AtString)(c_char_p())
    if AiMetaDataGetStr(node_entry, parm, 'remap', remap):
        return remap.contents.value
    else:
        return HA_PARM_PREFIX + parm
    
def pullSohoParms(anode, ha_object, force_set=False, overridable_parms=None):
    '''Pull SOHO parameters to this node.
    
    This function accomplishes the bulk of the parameter passing from SOHO
    to Arnold. It will iterate over this Arnold node's parameters and try
    to find matching parameters prefixed with htoa.node.node.HA_PARM_PREFIX
    on the target HaObject. <a href="http://www.sidefx.com/docs/houdini11.1/props/#Inheritance">
    SOHO property inheritance</a> is enforced in this method.
    
    It is sometimes necessary to ignore some of the Arnold node parameters
    because they require a specific processing, are irrelevant or are not
    yet implemented. Such parameters should be added to a parameter
    blacklist (HaNode._blacklist) that can be overridden by subclasses.
    
    All parameters succesfully passed or ignored can be traced by setting
    htoa.log.HaLog.enable_trace to True. A non-blacklisted parameter that
    does not exist on the target will always yield an error in the log.
    
    @param ha_object: The HaObject to suck parameters from.
    @param force_set: Always set parameters regardless of their default values.
    @param overridable_parms: Use this set of overridable parameters instead this node's.
    @todo: Some Arnold parameter types are not handled, motion blur
    samples could be automatic.
    @see: pullHouParms()
    
    '''
    node_entry = AiNodeGetNodeEntry(anode)
    parm_iter = AiNodeEntryGetParamIterator(node_entry)
    xprop = {AI_TYPE_ARRAY    : evalUnhandled,
             AI_TYPE_BOOLEAN  : ha_object.iprop,
             AI_TYPE_BYTE     : ha_object.iprop,
             AI_TYPE_ENUM     : ha_object.sprop,
             AI_TYPE_FLOAT    : ha_object.fprop,
             AI_TYPE_INT      : ha_object.iprop,
             AI_TYPE_MATRIX   : ha_object.fprop,
             AI_TYPE_NODE     : ha_object.sprop,
             AI_TYPE_NONE     : evalUnhandled,
             AI_TYPE_POINT2   : ha_object.fprop,
             AI_TYPE_POINT    : ha_object.fprop,
             AI_TYPE_POINTER  : evalUnhandled,
             AI_TYPE_RGB      : ha_object.fprop,
             AI_TYPE_RGBA     : ha_object.fprop,
             AI_TYPE_STRING   : ha_object.sprop,
             AI_TYPE_UINT     : ha_object.iprop,
             AI_TYPE_UNDEFINED: evalUnhandled,
             AI_TYPE_VECTOR   : ha_object.fprop}

    while not AiParamIteratorFinished(parm_iter):
        parm_entry = AiParamIteratorGetNext(parm_iter)
        
        # skip blacklisted parameters
        arnold_name = AiParamGetName(parm_entry)
        if isBlacklisted(node_entry, arnold_name):
            log.wtrace('[soho] Blacklisted parameter: %s' % arnold_name)
            continue

        # remap or prefix parameter name to get the houdini parameter name
        houdini_name = houdiniParmName(node_entry, arnold_name)
            
        # check overrides
        is_overridable = arnold_name in overridable_parms if overridable_parms else isOverridable(node_entry, arnold_name)
        is_overridden = ha_object.isOverridden(houdini_name)
        if is_overridable and not is_overridden:
            log.dtrace('[soho] Overridable parameter %s is not overridden, skipping' % arnold_name)
            continue

        # get parameter type, for arrays get the default value type
        arnold_type = AiParamGetType(parm_entry)
        if arnold_type == AI_TYPE_ARRAY:
            array_default = AiParamGetDefault(parm_entry).contents.ARRAY.contents
            array_size = array_default.nkeys * array_default.nelements
            if array_size == 1:
                arnold_type = array_default.type
            else:
                log.wtrace('[soho] Skipping array parameter %s (size = %i)' % (arnold_name, array_size))
                continue
        
        # get the SOHO value
        value = xprop[arnold_type](houdini_name)
        
        if value != None:
            # skip setting the parameter if its value is default 
            if not (HA_NODE_FORCE_SET or force_set or is_overridden) and value == HA_DEFVALUE[arnold_type](parm_entry):
                log.dtrace('[soho] Parameter %s is at its default value (%s), skipping' % (arnold_name, repr(value)))
                continue
            
            # set the arnold value
            arnoldParmSet[arnold_type](anode, arnold_name, value)
            log.dtrace('[soho] Parameter %s = %s (%s)' % (arnold_name, repr(value), houdini_name))
            
        elif isOptional(node_entry, arnold_name):
            log.wtrace('[soho] Optional parameter not found: %s (%s)' % (arnold_name, houdini_name))
        else:
            log.error('[soho] Parameter not found: %s (%s)' % (arnold_name, houdini_name))
            
    # sidedness and visibility
    if isBlacklisted(node_entry, 'sidedness'):
        is_overridable = isOverridable(node_entry, 'sidedness')
        is_overridden = ha_object.isOverridden(HA_PREFIX('sidedness'))
        if not is_overridable or (is_overridable and is_overridden):
            HaNodeSetByte(anode, 'sidedness', sidedness(ha_object), force_set=force_set or is_overridden)
        
    if isBlacklisted(node_entry, 'visibility'):
        is_overridable = isOverridable(node_entry, 'visibility')
        is_overridden = ha_object.isOverridden(HA_PREFIX('visibility'))
        if not is_overridable or (is_overridable and is_overridden):
            HaNodeSetByte(anode, 'visibility', rayVisibility(ha_object), force_set=force_set or is_overridden)
        elif is_overridable and not is_overridden and ha_object.isForcedPhantom():
            HaNodeSetByte(anode, 'visibility', AI_RAY_ALL & ~AI_RAY_CAMERA, force_set=force_set)

    if isBlacklisted(node_entry, 'autobump_visibility'):
        is_overridable = isOverridable(node_entry, 'autobump_visibility')
        is_overridden = ha_object.isOverridden(HA_PREFIX('autobump_visibility'))
        if not is_overridable or (is_overridable and is_overridden):
            HaNodeSetByte(anode, 'autobump_visibility', autobumpVisibility(ha_object), force_set=force_set or is_overridden)
            
def pullHouParms(anode, hou_node, prefix=HA_PARM_PREFIX, force_set=False, frame=None):
    '''Pull hou.Node parameters to this node.
    
    This function is the hou counterpart of pullSohoParms(). It operates
    similarly but on a hou.Node parameter. Parameters are prefixed with
    htoa.node.node.HA_PARM_PREFIX also. 
    
    You should always use pullSohoParms() instead of this method if you
    can as it is faster and supports <a href="http://www.sidefx.com/docs/houdini11.1/props/#Inheritance">
    SOHO property inheritance</a>. Some nodes such as shaders are not
    available through SOHO and thus have to use this method.
    
    Contrarily to pullSohoParms(), there is no blacklist for parameters,
    only the "name" parameter is hardcoded to be ignored.
    
    @param hou_node: The target hou.Node to suck parameters from.
    @param prefix: A string prefix for the parameters, defaults to HA_PARM_PREFIX
    @param force_set: Always set parameters regardless of their default values.
    @param frame: Evaluate at this frame, or at the current time if None
    @todo: Some Arnold parameter types are not handled, motion blurs
    samples could be automatic.
    @see: pullSohoParms()
    '''
    node_entry = AiNodeGetNodeEntry(anode)
    parm_iter = AiNodeEntryGetParamIterator(node_entry)
    
    if frame == None:
        frame = hou.frame()

    while not AiParamIteratorFinished(parm_iter):
        parm_entry = AiParamIteratorGetNext(parm_iter)
        
        arnold_type = AiParamGetType(parm_entry)
        if arnold_type == AI_TYPE_ARRAY:
            arnold_type = AiParamGetDefault(parm_entry).contents.ARRAY.contents.type

        arnold_name = AiParamGetName(parm_entry)
        
        if arnold_name == 'name':
            continue
        
        houdini_name = prefix + AiParamGetName(parm_entry)

        # get the HOM value
        try:
            value = houdiniParmGet[arnold_type](hou_node, houdini_name, frame)
        except:
            log.wtrace('[hou] Parameter "%s" does not exist on %s' % (houdini_name, hou_node.name()))
            continue

        if value != None:
            # skip setting the parameter if its value is default 
            defvalue = HA_DEFVALUE[arnold_type](parm_entry)
            if not (HA_NODE_FORCE_SET or force_set) and value == defvalue:
                log.dtrace('[hou] Parameter %s is at its default value (%s), skipping' % (arnold_name, repr(value)))
                continue

            # set the arnold value
            arnoldParmSet[arnold_type](anode, arnold_name, value)
            log.dtrace('[hou] Parameter %s = %s' % (arnold_name, repr(value)))
        else:
            log.error('[hou] Parameter "%s" does not exist on %s' % (houdini_name, hou_node.name()))


class HaNode(object):
    '''Arnold node wrapper class.

HaNode is a wrapper around AiNode. It can create the AiNode it wraps or attach
to an existing one. 

This class can be used as is, subclassed directly or indirectly through HaShape. 

@section passing_parameters Pulling parameters

The Arnold node Parameters can be "pulled" from a target HaObject. This is
achieved with the following methods:

- htoa.node.node.HaNode.pullSohoParms()
- htoa.node.node.HaNode.pullHouParms()

These methods will do the bulk of the parameter passing but sometimes it is 
necessary to ignore some of the Arnold node parameters because they require a
specific processing, are irrelevant or are not yet implemented. Such parameters
should be added to a parameter blacklist (htoa.node.node.HaNode._blacklist)
that can be overridden by subclasses.

All parameters successfully passed or blacklisted are logged at the trace level
(see @ref logging). Any other parameter not passed is logged as an error. This
gives you a way to ensure you don't miss any parameters unintentionally.
    
    '''
    def __init__(self, type_or_node=None):
        '''Constructor.
        
        @param type_or_node: Can be either a type name (eg. "polymesh") or an
        AiNode instance. 
        '''
        
        ## The actual Arnold node
        self.node = None
        
        if isinstance(type_or_node, str):
            # try to find a native, prefixed shader first
            htoa_node_name = htoa.shader_prefix + type_or_node
            if AiNodeEntryLookUp(htoa_node_name):
                self.node = AiNode(htoa_node_name)
            else:
                self.node = AiNode(type_or_node)
                
        elif type(type_or_node) == type(AiUniverseGetOptions()):
            self.node = type_or_node
            
    @property
    def name(self):
        '''Name getter'''
        return AiNodeGetName(self.node)
 
    @name.setter
    def name(self, newname):
        '''Name setter'''
        AiNodeSetStr(self.node, 'name', newname)
