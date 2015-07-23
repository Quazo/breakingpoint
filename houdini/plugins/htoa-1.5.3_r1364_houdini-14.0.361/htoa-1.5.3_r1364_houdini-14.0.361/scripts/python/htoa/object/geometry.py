# $Id: geometry.py 1359 2015-06-15 17:06:26Z kik $

import hou
import soho

from arnold import *

from htoa.object.object import HaObject, pathToId
from htoa.node.node import pullSohoParms
from htoa.node.parms import *
from htoa.properties import translateAs

import htoa.log as log
import htoa_pygeo

import ctypes

def setLightGroup(arg_dict):
    '''Post-translate hook to assign light groups'''
    
    out_nodes = arg_dict['out_nodes']
    light_mask = arg_dict['light_mask']
    light_array = AiArrayAllocate(len(light_mask), 1, AI_TYPE_NODE)
    
    for i, light_name in enumerate(light_mask):
        light_node = AiNodeLookUpByName(light_name)
        AiArraySetPtr(light_array, i, light_node)
    
    for shape_node in out_nodes:
        AiNodeSetBool(shape_node, "use_light_group", True)
        AiNodeSetArray(shape_node, "light_group", AiArrayCopy(light_array))
        
    AiArrayDestroy(light_array)
    
class HaGeometry(HaObject):
    '''Houdini geometry translator'''

    def __init__(self, session, soho_obj):
        '''Constructor'''
        
        # call superclass constructor
        self._init(session, soho_obj)
        
    def _generate(self, index=None):
        '''Generate Arnold geometry'''
        
        shdict = {}

        log.debug('Generating %s' % self.path)
        pygeo_obj = htoa_pygeo.Object(self.session.pygeo_session,
                                      self.hou_node.path(),
                                      self.instance_index,
                                      tuple(self.xform_times),
                                      tuple(self.dform_times),
                                      self.mbtype)
        shdict.update(pygeo_obj.generate())
        
        # output Arnold node list
        out_nodes = [cast(k, ctypes.POINTER(AtNode)) for k in shdict.iterkeys()]
        self.session.shapes[self.path] = out_nodes
        
        # early out if nothing was generated
        if out_nodes == [None] * len(out_nodes):
            return {}
            
        # init shadow mask
        self.session.shadow_mask[self.path] = []
        
        # ids
        for anode in out_nodes:
            AiNodeSetInt(anode, 'id', pathToId(self.path))
            
        # properties
        if translateAs(self.hou_node) != 'instance' and self.session.iprop('ar_inherit_properties'):
            for anode in out_nodes:
                pullSohoParms(anode, self)
            
        # forced matte     
        if self.isForcedMatte():
            for anode in out_nodes:
                AiNodeSetBool(anode, 'matte', True)
            
        # sss set
        sss_setname = self.sprop('ar_sss_setname', defvalue=['']).strip()
        if sss_setname:
            for anode in out_nodes:
                AiNodeDeclare(anode, 'sss_setname', 'constant STRING')
                AiNodeSetStr(anode, 'sss_setname', sss_setname)
                        
        # trace sets
        ts_list = self.sprop('ar_trace_sets', defvalue=['']).split()
        if ts_list:
            ts_count = len(ts_list)
            ts_array = AiArrayAllocate(ts_count, 1, AI_TYPE_STRING)
            for i in xrange(ts_count):
                AiArraySetStr(ts_array, i, ts_list[i])
            for anode in out_nodes:
                AiNodeSetArray(anode, "trace_sets", AiArrayCopy(ts_array))
            AiArrayDestroy(ts_array)

        # user options
        user_options = self.parm('ar_user_options', override_suffix='_enable')
        if user_options:
            for anode in out_nodes:
                AiNodeSetAttributes(anode, user_options)

        # light groups
        light_count = sum(1 for _ in soho.objectList('objlist:light')) # soho.objectList is a generator
        light_mask = [l.getName() for l in self.soho_obj.objectList('objlist:lightmask', self.session.now)]
        
        if light_mask and len(light_mask) != light_count:
            arg_dict = {'light_mask': light_mask, 'out_nodes': out_nodes}
            self.session.post_translate_hooks.append((setLightGroup, arg_dict))
            
        return shdict

    def generate(self, index=None):
        shdict = self._generate(index)
        
        # no geometry generated
        if not shdict:
            return
        
        # make shader paths canonical
        obj_shader_path = self.materialPath() # default shader
        
        if self.sop_path:
            hou.cd(self.sop_path)
            for aname in shdict:
                shader_paths = shdict[aname]
                canonical_shader_paths = []
                for path in shader_paths:
                    shader_node = hou.node(path)
                    if shader_node:
                        canonical_shader_paths.append(shader_node.path())
                    else:
                        canonical_shader_paths.append(obj_shader_path) # fallback to default shader
                
                shdict[aname] = canonical_shader_paths

        return shdict

        