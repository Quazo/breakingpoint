# $Id: volume.py 1358 2015-06-15 16:39:12Z kik $

import ctypes

import hou

from arnold import *

from htoa.node.shape import HaShape
import htoa.log as log
from htoa.object.object import pathToId
from htoa.node.parms import *
from htoa.node.node import pullSohoParms
import htoa

class HaVolumeContainer(HaShape):
    '''Arnold volume container
    '''
                
    def generate(self, index=None):
        '''Generate Arnold geometry.
        '''
        node_name = self.obj.path if index is None else '%s:%s' % (self.obj.path, repr(index))

        log.debug('Generating volume container: %s' % node_name)

        container = self.obj.sprop('ar_volume_container')

        # which arnold node should we build        
        if container in ('box', 'sphere', 'cylinder'):
            arnold_type = container
        elif container == 'sop':
            bounds_primitive = self.obj.sprop('ar_bounds_primitive')
            if bounds_primitive == 'bounding_box':
                arnold_type = 'box'
            else: # bounding_sphere
                arnold_type = 'sphere'
        elif container == 'openvdb':
            arnold_type = 'box'
        
        # create arnold shape
        self.node = AiNode(arnold_type)
        self.name = node_name
        HaNodeSetArray(self.node, "matrix", AiArrayCopy(self.obj.getArnoldMatrix()))
        HaNodeSetInt(self.node, 'id', pathToId(self.obj.path))

        # get display sop bbox
        sop_node = self.obj.hou_node.displayNode()
        bbox = sop_node.geometry().boundingBox()
        bbmin = bbox.minvec()
        bbmax = bbox.maxvec()
        
        # box
        if arnold_type == 'box':
            HaNodeSetPnt(self.node, 'min', bbmin[0], bbmin[1], bbmin[2])
            HaNodeSetPnt(self.node, 'max', bbmax[0], bbmax[1], bbmax[2])
            
        else: # arnold_type == 'sphere':
            HaNodeSetFlt(self.node, 'radius', 0.5 * (bbmax[0] - bbmin[0]))
            
        pullSohoParms(self.node, self.obj)
        
        # user options
        AiNodeSetAttributes(self.node, self.obj.parm('ar_user_options', override_suffix='_enable'))

        hou.cd(self.obj.path)
        return {ctypes.addressof(self.node.contents): [self.obj.materialPath()]}
