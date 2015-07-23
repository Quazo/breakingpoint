# $Id: light.py 1358 2015-06-15 16:39:12Z kik $

import hou
import soho

from arnold import *

from htoa.object.object import HaObject
import htoa.log as log
from htoa.node.node import HaNode, pullSohoParms
from htoa.material import HaMaterial
from htoa.node.parms import *

light_class = {'point':       'point_light',
               'distant':     'distant_light',
               'spot':        'spot_light',
               'quad':        'quad_light',
               'disk':        'disk_light',
               'cylinder':    'cylinder_light',
               'skydome':     'skydome_light',
               'mesh':        'mesh_light',
               'photometric': 'photometric_light'}

# map radius parameters
radius_name = {'point':    'ar_point_radius',
               'spot':     'ar_spot_radius',
               'disk':     'ar_disk_radius', 
               'cylinder': 'ar_cylinder_radius'}

# post-translate hook to set the mesh parameter
def linkMeshHook(arg_dict):
    mesh_path = arg_dict['mesh_path']
    mesh_node = hou.node(mesh_path)
    obj_path = mesh_node.path() if mesh_node else ''
    mesh_name = obj_path + ':polygons' # FIXME: hardcoded suffix
    mesh_node = AiNodeLookUpByName(mesh_name)
    mesh_light = arg_dict['mesh_light']
    if mesh_node and AiNodeIs(mesh_node, 'polymesh'):
        HaNodeSetPtr(mesh_light, 'mesh', mesh_node)
    else:
        log.error('Invalid mesh name "%s" for mesh light %s' % (mesh_name, AiNodeGetName(mesh_light)))

class HaLight(HaObject):
    '''
    Translator for lights
    '''
    
    def __init__(self, session, soho_obj):
        '''Constructor'''
        
        # call superclass constructor
        self._init(session, soho_obj)
                
    def generate(self, index=None):
        '''Generate Arnold Light
        
        @return: Created Arnold light node or None
        '''

        # TODO: handle auto-headight
        if self.path == 'soho_autoheadlight_light':
            log.debug('Skipping auto-headlight')
            return None

        light_type = self.sprop('ar_light_type')
        if not light_type:
            log.debug('Skipping non-Arnold light %s' % self.path)
            return None
            
        if not self.iprop('light_enable'):
            log.debug('Skipping disabled light %s' % self.path)
            return None
        
        node_name = self.path if index is None else '%s:%s' % (self.path, repr(index))

        log.debug('Generating %s light %s' % (light_type, node_name))
        
        light = AiNode(light_class[light_type])
        AiNodeSetStr(light, 'name', node_name)
        pullSohoParms(light, self)
        
        if light_type in radius_name:
            HaNodeSetFlt(light, 'radius', self.fprop(radius_name[light_type]))
            
        # quad light
        if light_type == 'quad':
            # vertices
            vtx_array = AiArrayAllocate(4, 1, AI_TYPE_POINT)
            hsize = self.fprop('ar_quad_size')
            hsizex = 0.5 * hsize[0]
            hsizey = 0.5 * hsize[1]
            AiArraySetPnt(vtx_array, 0, AtPoint(hsizex, -hsizey, 0.0))
            AiArraySetPnt(vtx_array, 1, AtPoint(-hsizex, -hsizey, 0.0))
            AiArraySetPnt(vtx_array, 2, AtPoint(-hsizex, hsizey, 0.0))
            AiArraySetPnt(vtx_array, 3, AtPoint(hsizex, hsizey, 0.0))
            HaNodeSetArray(light, 'vertices', vtx_array)
            
            color_type = self.sprop('ar_light_color_type')
            
            if color_type == 'texture':
                image = HaNode('image')
                image.name = node_name + ':texture'
                HaNodeSetStr(image.node, 'filename', self.sprop('ar_light_color_texture'))
                AiNodeLink(image.node, 'color', light)
                
            elif color_type == 'shader':
                shader_path = hou.chsop(self.path + '/ar_light_color_shader')
                AiNodeLink(HaMaterial(self.session, shader_path).generateLightColorShader(), 'color', light)
        
        # cylinder light
        elif light_type == 'cylinder':
            hheight = self.fprop('ar_height') * 0.5
            HaNodeSetArray(light, 'top', AiArray(1, 1, AI_TYPE_POINT, AtPoint(0.0, hheight, 0.0)))
            HaNodeSetArray(light, 'bottom', AiArray(1, 1, AI_TYPE_POINT, AtPoint(0.0, -hheight, 0.0)))
        
        # skydome light
        elif light_type == 'skydome':
            color_type = self.sprop('ar_light_color_type')
            
            if color_type == 'texture':
                image = HaNode('image')
                image.name = node_name + ':texture'
                HaNodeSetStr(image.node, 'filename', self.sprop('ar_light_color_texture'))
                AiNodeLink(image.node, 'color', light)
                
            elif color_type == 'shader':
                shader_path = hou.chsop(self.path + '/ar_light_color_shader')
                AiNodeLink(HaMaterial(self.session, shader_path).generateLightColorShader(), 'color', light)

        # mesh light
        elif light_type == 'mesh':
            color_type = self.sprop('ar_light_color_type')
            
            if color_type == 'texture':
                image = HaNode('image')
                image.name = node_name + ':texture'
                HaNodeSetStr(image.node, 'filename', self.sprop('ar_light_color_texture'))
                AiNodeLink(image.node, 'color', light)
                
            elif color_type == 'shader':
                shader_path = hou.chsop(self.path + '/ar_light_color_shader')
                AiNodeLink(HaMaterial(self.session, shader_path).generateLightColorShader(), 'color', light)

            # append a post-translate hook to set the mesh parameter
            mesh_path = self.sprop('ar_mesh')
            mesh_hnode = self.hou_node.node(mesh_path)
            
            if mesh_hnode:
                arg_dict = {}
                arg_dict['mesh_light'] = light
                arg_dict['mesh_path'] = mesh_hnode.path()
                self.session.post_translate_hooks.append((linkMeshHook, arg_dict))
            else:
                log.error('Invalid mesh path "%s" for mesh light %s' % (mesh_path, self.path))
            
        elif light_type not in light_class:
            log.error('Skipping unsupported light type: %s' % light_type)
            return None
        
        # set transform
        HaNodeSetArray(light, "matrix", self.getArnoldMatrix())
        
        # light filters
        filters_path = hou.chsop(self.path + '/ar_light_filters')
        if filters_path:
            filters_list = HaMaterial(self.session, filters_path).generateLightFilters(light_type)
            filters_array = AiArrayAllocate(len(filters_list), 1, AI_TYPE_POINTER)
            for i in xrange(len(filters_list)):
                AiArraySetPtr(filters_array, i, filters_list[i])
                
            HaNodeSetArray(light, 'filters', filters_array)
        
        # shadow groups
        shadow_mask = [o.getName() for o in self.soho_obj.objectList('objlist:shadowmask', self.session.now)]
        for obj in shadow_mask:
            if obj in self.session.shadow_mask:
                self.session.shadow_mask[obj].append(self.path)
                    
        # alSurface light groups
        if self.iprop('ar_light_group_enable', defvalue=[False]):
            AiNodeDeclare(light, 'lightGroup', 'constant INT')
            AiNodeSetInt(light, 'lightGroup', self.iprop('ar_light_group', defvalue=[0]))

        # user options
        AiNodeSetAttributes(light, self.parm('ar_user_options', override_suffix='_enable'))
        
        return light
    