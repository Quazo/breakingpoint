'''@version: $Id: material.py 1358 2015-06-15 16:39:12Z kik $
'''
import glob
import os
import hou
from arnold import *

import htoa
import htoa.log as log
from htoa.node.node import pullHouParms, houdiniParmGet, arnoldParmSet
from htoa.node.parms import *

## Arnold types cardinality
_type_cardinality = {
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
#                       AI_TYPE_ARRAY    : None,
#                       AI_TYPE_POINTER  : None,
#                       AI_TYPE_NONE     : None,
#                       AI_TYPE_UNDEFINED: None,
                    }

def isLightFilterCompatible(filter_type, light_type):
    '''Check light filter compatibility with light'''
    
    if filter_type == 'light_decay' and light_type in ('distant', 'skydome'):
        return False
    
    if filter_type in ('gobo', 'barndoor') and light_type != 'spot':
        return False
    
    return True

def vopKind(vop):
    '''Return a VOP kind for special nodes.
    
    Some VOP nodes require following connections like subnets and HDAs, their
    "kind" is then returned. If the VOP node is a regular Arnold shader, then
    "shader" is returned.
    '''
    
    vop_type_name = vop.type().name()
    if vop_type_name in ('subnet', 'subinput', 'null'):
        return vop_type_name
    
    if vop.type().definition():
        return 'hda'

    if vop_type_name == 'arnold::fetch':
        return 'fetch'
    
    return 'shader'

def inputShaderVop(cnx):
    '''Return the actual input shader VOP navigating through subnets, digital
    assets, fetch and null nodes upstream.
    
    @param cnx: a hou.NodeConnection
    @return: a dict containing the shader vop node or None (keyed by 'vop') and
    the output index of the connection or -1 (keyed by 'index').
    '''
    
    input_vop = cnx.inputNode()
    output_index = cnx.outputIndex()
    parm_name = None
    
    # follow subinputs and connections inside subnets or digital assets
    while vopKind(input_vop) != 'shader':
        vop_kind = vopKind(input_vop)
        index_offset = 0
        
        if vop_kind == 'subinput':
            target_vop = input_vop.parent()
            
        elif vop_kind == 'fetch':
            fetch_target_path = input_vop.parm('target').evalAsString()
            fetch_target_vop = input_vop.node(fetch_target_path)
            
            if fetch_target_vop:
                log.dtrace('Fetch %s => %s' % (input_vop.path(), fetch_target_vop.path()))
                input_vop = fetch_target_vop
                continue
            else:
                log.error('Fetch %s, invalid path: %s' % (input_vop.path(), fetch_target_path))
                return {}
        
        elif vop_kind == 'null':
            null_cnx = input_vop.inputConnectors()[output_index][0]
            if null_cnx:
                log.dtrace('Null %s => %s' % (input_vop.path(), null_cnx.inputNode().path()))
                input_vop = null_cnx.inputNode()
                output_index = null_cnx.outputIndex()
                continue
            else: # should never happen
                log.warning('Null %s => input %i is not connected' % (input_vop.path(), output_index))
                return {}
            
        # vop_kind in (subnet, hda)
        else:
            # offset the output indexes by the subinput's number of outputs (ticket #73)
            subinputs = [n for n in input_vop.children() if n.type().name() == 'subinput']
            index_offset = len(subinputs[0].outputNames()) if subinputs else 0

            suboutputs = [n for n in input_vop.children() if n.type().name() == 'suboutput']
            if not suboutputs: return {}
            target_vop = suboutputs[0]

        connectors = target_vop.inputConnectors()[output_index + index_offset]
        
        if connectors:
            input_vop = connectors[0].inputNode()
            output_index = connectors[0].outputIndex()
            
        # for hdas and subnets, if an input is not connected, we get the
        # value from a similarly named parameter, stripped of its leading
        # underscore character ("_").
        elif vop_kind == 'subinput':
            parm_name = input_vop.outputNames()[output_index][1:]
            input_vop = target_vop
            output_index = -1
            break
        else:
            return {}

    return {'vop': input_vop, 'index': output_index, 'parm': parm_name}

class HaMaterial(object):
    '''Any SHOP network, not just materials
    
    @todo: refactor HaMaterial to HaVopnet or something
    '''

    def __init__(self, session, path):
        ## The context HaSession
        self.session = session
        
        ## shader type
        self.type = None

        ## shader path
        self.path = path

        # early out for empty path
        if not self.path:
            log.dtrace('Empty shader path')
            return

        # check node existence
        self.hnode = hou.node(self.path)
        if not self.hnode:
            log.error('Cannot find shader path ' + self.path)
            return
        
        ## Parent shop
        self.shop = self.getShop()
        if not self.shop:
            log.error('Cannot find parent SHOP for shader path ' + self.path)
            return
        
        # path is a SHOP
        if self.hnode == self.shop:
            # arnold vopnet
            if self.shop.type().name() == 'arnold_vopnet':
                self.type = 'vopnet'
            else:
                # try to find a child arnold_vopnet
                for shop_node in self.hnode.children():
                    if shop_node.type().name() == 'arnold_vopnet':
                        self.type = 'vopnet'
                        self.path = shop_node.path()
                        self.hnode = hou.node(self.path)
                        self.shop = self.hnode
                        break
                    
                if not self.type:
                    log.error('Unhandled SHOP type %s (%s)' % (self.path, self.shop.type().name()))
        
        # path is an Arnold VOP
        elif self.hnode.type().category().name() == 'Vop' and self.shop.type().name() == 'arnold_vopnet':
            self.type = self.hnode.type().name()
            
            if not self.type in ['arnold_material', 'arnold_environment', 'arnold_light']:
                self.type = 'vop'
                
        else:
            log.error('Invalid shader path ' + self.path)

    def getShop(self):
        '''Return parent SHOP or None'''
        
        hnode = self.hnode
        
        while hnode and hnode.type().category().name() != 'Shop':
            hnode = hnode.parent()
        
        return hnode

    def getDefaultOutput(self, shader_type):
        '''Find the default output of a vopnet'''
        
        if self.type != 'vopnet':
            log.error('Only applies to Arnold vopnets (type=%s)' % self.type)
            return None
        
        # get the first collector node we find
        for vop in self.shop.children():
            if vop.type().name() == shader_type:
                return vop

        log.error('Cannot find default %s output in vopnet %s' % (shader_type, self.path))
        return None

    def generateMaterial(self, volumic=False):
        '''Generate material shader networks
        
        @return: a dictionary of the Arnold shader keyed by context ('surface',
        'disp', 'volume')
        '''
        
        # early out for empty shader path
        if not self.type:
            return {}
        
        log.dtrace('Generating material ' + self.path)

        if volumic:
            return self.generateVolumeShader()
        else:
            return self.generateSurfaceShader()
    
    def generateSurfaceShader(self):
        '''Generate VOP network surface shader, including bump and displacement'''
        
        if not self.type in ['vopnet', 'arnold_material']:
            log.error('Must specify a vopnet or an arnold_material output (type=%s)' % self.type)
            return {}
        
        if self.type == 'vopnet':
            output_vop = self.getDefaultOutput('arnold_material')
            if not output_vop:
                return {}
                
        else: # self.type == 'arnold_material':
            output_vop = self.hnode
        
        # surface is input #1
        res = {}
        try:
            surface_vop = inputShaderVop(output_vop.inputConnectors(True)[0][0])['vop']
            res['surface'] = self.generateVop(surface_vop)
            
            # bump is input #2
            try:
                bump_vop = inputShaderVop(output_vop.inputConnectors(True)[1][0])['vop']
                AiNodeLink(self.generateVop(bump_vop), '@before', res['surface'])
            except: pass
        except: pass
        
        # displacement is input #3
        try:
            disp_vop = inputShaderVop(output_vop.inputConnectors(True)[2][0])['vop']
            res['disp'] = self.generateVop(disp_vop)
        except: pass

        return res
    
    def generateVolumeShader(self):
        '''Generate VOP network volume shader'''
        
        if not self.type in ['vopnet', 'arnold_material']:
            log.error('Must specify a vopnet or an arnold_material output (type=%s)' % self.type)
            return {}
        
        if self.type == 'vopnet':
            output_vop = self.getDefaultOutput('arnold_material')
            if not output_vop:
                return {}
                
        else: # self.type == 'arnold_material':
            output_vop = self.hnode

        # volume is input #4 
        try:
            volume_vop = inputShaderVop(output_vop.inputConnectors(True)[3][0])['vop']
            return {'volume': self.generateVop(volume_vop)}
        except:
            return {}
        
    def generateAtmosphereShader(self):
        '''Generate VOP network atmosphere shader'''
        
        if not self.type in ['vopnet', 'arnold_environment']:
            log.error('Must specify a vopnet or an arnold_environment output (type=%s)' % self.type)
            return None
        
        if self.type == 'vopnet':
            output_vop = self.getDefaultOutput('arnold_environment')
            if not output_vop:
                return None
                
        else: # self.type == 'arnold_environment':
            output_vop = self.hnode

        # atmosphere is input #1 
        try:
            atm_vop = inputShaderVop(output_vop.inputConnectors(True)[0][0])['vop']
            return self.generateVop(atm_vop)
        except:
            return None
        
    def generateBackgroundShader(self):
        '''Generate VOP network background shader'''
        
        res = {'shader': None, 'visibility': AI_RAY_ALL}
        
        if not self.type in ['vopnet', 'arnold_environment']:
            log.error('Must specify a vopnet or an arnold_environment output (type=%s)' % self.type)
            return res
        
        if self.type == 'vopnet':
            output_vop = self.getDefaultOutput('arnold_environment')
            if not output_vop:
                return res
                
        else:
            output_vop = self.hnode

        # background is input #2 
        try:
            background_vop = inputShaderVop(output_vop.inputConnectors(True)[1][0])['vop']
            res['shader'] = self.generateVop(background_vop)
            res['visibility'] = output_vop.parm('background_visibility').evalAsIntAtFrame(self.session.frame)
        except: pass
            
        return res
    
    def generateLightColorShader(self):
        '''Generate VOP network light color shader'''
        
        if not self.type in ['vopnet', 'arnold_light']:
            log.error('Must specify a vopnet or an arnold_light output (type=%s)' % self.type)
            return None
        
        if self.type == 'vopnet':
            output_vop = self.getDefaultOutput('arnold_light')
            if not output_vop:
                return None
                
        else: # self.type == 'arnold_light':
            output_vop = self.hnode

        # light color is input #1 
        try:
            light_color_vop = inputShaderVop(output_vop.inputConnectors(True)[0][0])['vop']
            return self.generateVop(light_color_vop)
        except:
            return None

    def generateLightFilters(self, light_type):
        '''Generate VOP network light filters'''
        
        res = []

        if not self.type in ['vopnet', 'arnold_light']:
            log.error('Must specify a vopnet or an arnold_light output (type=%s)' % self.type)
            return res
        
        if self.type == 'vopnet':
            output_vop = self.getDefaultOutput('arnold_light')
            if not output_vop:
                return res
                
        else:
            output_vop = self.hnode

        # only one of these filters is allowed
        has_gobo = False
        has_barndoor = False
        
        for cnx in output_vop.inputConnections():
            # skip the color input
            if cnx.inputIndex() == 0:
                continue
            
            vop_filter = inputShaderVop(cnx)['vop']
            if not vop_filter:
                continue
            
            filter_type = vop_filter.type().nameComponents()[2]
            
            if not isLightFilterCompatible(filter_type, light_type):
                log.warning('Light filter %s (%s) is incompatible with light of type %s' % (vop_filter.path(), filter_type, light_type))
                continue
            
            if filter_type == 'gobo':
                if has_gobo:
                    log.warning('Only one gobo filter is allowed, skipping %s' % vop_filter.path())
                    continue
                else:
                    has_gobo = True
                
            if filter_type == 'barndoor':
                if has_barndoor:
                    log.warning('Only one barndoor filter is allowed, skipping %s' % vop_filter.path())
                    continue
                else:
                    has_barndoor = True
            
            res.append(self.generateVop(vop_filter))
            
        return res
        
    def customCameraVop(self):
        '''return the target custom camera VOP'''
        if not self.path:
            log.dtrace('Empty shader path, cannot find custom camera')
            return None
        
        if not self.type in ['vopnet', 'arnold_camera']:
            log.error('Must specify a vopnet or an arnold_camera output (type=%s)' % self.type)
            return None
        
        if self.type == 'vopnet':
            output_vop = self.getDefaultOutput('arnold_camera')
            if not output_vop:
                return None
                
        else: # self.type == 'arnold_camera':
            output_vop = self.hnode

        # camera is input #1 
        try:
            return inputShaderVop(output_vop.inputConnectors(True)[0][0])['vop']
        except:
            return None
        
    def generateCustomCamera(self):
        '''Generate VOP network custom camera'''
        try:
            return self.generateVop(self.customCameraVop())
        except:
            return None

    def generateCameraUvRemap(self):
        '''Generate VOP network UV remap shader'''
                
        if not self.path:
            log.dtrace('Empty shader path, cannot generate camera uv remap')
            return None

        if not self.type in ['vopnet', 'arnold_camera']:
            log.error('Must specify a vopnet or an arnold_camera output (type=%s)' % self.type)
            return None
        
        if self.type == 'vopnet':
            output_vop = self.getDefaultOutput('arnold_camera')
            if not output_vop:
                return None
                
        else: # self.type == 'arnold_camera':
            output_vop = self.hnode

        # uv_remap is input #2
        try:
            remap_vop = inputShaderVop(output_vop.inputConnectors(True)[1][0])['vop']
            return self.generateVop(remap_vop)
        except:
            return None

    def generateCameraFiltermap(self):
        '''Generate VOP network filtermap shader'''
                
        if not self.path:
            log.dtrace('Empty shader path, cannot generate camera filtermap')
            return None

        if not self.type in ['vopnet', 'arnold_camera']:
            log.error('Must specify a vopnet or an arnold_camera output (type=%s)' % self.type)
            return None
        
        if self.type == 'vopnet':
            output_vop = self.getDefaultOutput('arnold_camera')
            if not output_vop:
                return None
                
        else: # self.type == 'arnold_camera':
            output_vop = self.hnode

        # uv_remap is input #3
        try:
            filtermap_vop = inputShaderVop(output_vop.inputConnectors(True)[2][0])['vop']
            return self.generateVop(filtermap_vop)
        except:
            return None

    def generateVop(self, vop):
        '''Recursively generate linked Arnold shaders, starting at vop
        
        The recursion occurs on the input nodes. If a vop has already been
        translated during this session (according to self.session.shaders),
        the Arnold node will not be regenerated and the already existing
        shader node will be returned.
        
        @param vop: the starting hou.VopNode
        @return: the Arnold shader node corresponding to vop
        '''
        
        vop_path = vop.path()
        
        # early out if shader was already generated
        if vop_path in self.session.shaders:
            # TODO insert a cache node
            return self.session.shaders[vop_path]
        
        log.debug('Generating shader ' + vop_path)
        arnold_type = vop.type().nameComponents()[2] # remove namespace, version
        
        # try to find a native, prefixed shader first
        htoa_shader_name = htoa.shader_prefix + arnold_type
        if AiNodeEntryLookUp(htoa_shader_name):
            shader = AiNode(htoa_shader_name)
        else:
            shader = AiNode(arnold_type)

        pullHouParms(shader, vop, prefix='', frame=self.session.frame) # no parameter prefix in VOP context

        # special case: ramp_rgb
        if arnold_type == 'ramp_rgb':
            parm_instances = vop.parm('ramp').multiParmInstances()
            npts = len(parm_instances) / 5
            array_position      = AiArrayAllocate(npts, 1, AI_TYPE_FLOAT);
            array_color         = AiArrayAllocate(npts, 1, AI_TYPE_RGB);
            array_interpolation = AiArrayAllocate(npts, 1, AI_TYPE_INT);
            
            for i in xrange(0, npts):
                AiArraySetFlt(array_position, i, parm_instances[i * 5].evalAsFloatAtFrame(self.session.frame))
                cr = parm_instances[i * 5 + 1].evalAsFloatAtFrame(self.session.frame)
                cg = parm_instances[i * 5 + 2].evalAsFloatAtFrame(self.session.frame)
                cb = parm_instances[i * 5 + 3].evalAsFloatAtFrame(self.session.frame)
                AiArraySetRGB(array_color, i, AtRGB(cr, cg, cb))
                AiArraySetInt(array_interpolation, i, parm_instances[i * 5 + 4].evalAsIntAtFrame(self.session.frame))
            
            HaNodeSetArray(shader, 'position'     , array_position)
            HaNodeSetArray(shader, 'color'        , array_color)
            HaNodeSetArray(shader, 'interpolation', array_interpolation)
            
        # special case: ramp_float
        if arnold_type == 'ramp_float':
            parm_instances = vop.parm('ramp').multiParmInstances()
            npts = len(parm_instances) / 3
            array_position      = AiArrayAllocate(npts, 1, AI_TYPE_FLOAT);
            array_value         = AiArrayAllocate(npts, 1, AI_TYPE_FLOAT);
            array_interpolation = AiArrayAllocate(npts, 1, AI_TYPE_INT);
            
            for i in xrange(0, npts):
                AiArraySetFlt(array_position     , i, parm_instances[i * 3].evalAsFloatAtFrame(self.session.frame))
                AiArraySetFlt(array_value        , i, parm_instances[i * 3 + 1].evalAsFloatAtFrame(self.session.frame))
                AiArraySetInt(array_interpolation, i, parm_instances[i * 3 + 2].evalAsIntAtFrame(self.session.frame))
            
            HaNodeSetArray(shader, 'position'     , array_position)
            HaNodeSetArray(shader, 'value'        , array_value)
            HaNodeSetArray(shader, 'interpolation', array_interpolation)
        
        # set the arnold node name to this VOP's path
        AiNodeSetStr(shader, 'name', vop_path)
        
        # replace texture with existing .tx file
        if arnold_type == 'image' and self.session.iprop('ar_texture_use_existing_tx'):
            filename = vop.parm('filename').evalAsStringAtFrame(self.session.frame)
            txfile = os.path.splitext(filename)[0] + '.tx'
            txglob = txfile.replace('<udim>', '[1-9][0-9][0-9][0-9]')
            if glob.glob(txglob):
                HaNodeSetStr(shader, 'filename', txfile)
                log.dtrace('Using existing .tx texture for ' + vop_path + ': ' + txfile)
        
        # append the shader to the current session's shaders
        self.session.shaders[vop_path] = shader
        
        # recurse over connected inputs
        for cnx in list(vop.inputConnections()):
            vop_dict = inputShaderVop(cnx)
            if not vop_dict: continue
            
            input_vop = vop_dict['vop']
            output_index = vop_dict['index']
            input_parm_name = vop_dict['parm']
            parm_name = vop.inputNames()[cnx.inputIndex()]
            
            # the input is not connected let's try to find a matching parameter
            # on the hda or subnet and retrieve its value to set the shader
            # parameter
            if input_parm_name:
                arnold_type = AiParamGetType(AiNodeEntryLookUpParameter(AiNodeGetNodeEntry(shader), parm_name))
                
                try:
                    value = houdiniParmGet[arnold_type](input_vop, input_parm_name, self.session.frame)
                    
                    # if value is a tuple, ensure it matches the size expected by the setter
                    if type(value) is tuple:
                        value_size = len(value)
                        type_cardinality = _type_cardinality[arnold_type]
                        
                        # get rid of the tuple for single values
                        if type_cardinality == 1:
                            value = value[0]
                            
                        # if the tuple is too short, fill with zeros
                        elif value_size < type_cardinality:
                            value = [value[i] if i < value_size else 0 for i in xrange(type_cardinality)]
                except:
                    log.wtrace('[hou] Parameter "%s" does not exist on %s' % (input_parm_name, input_vop.name()))
                    continue
                
                if value is None:
                    log.error('[hou] Parameter "%s" does not exist on %s' % (input_parm_name, input_vop.name()))
                else:
                    arnoldParmSet[arnold_type](shader, parm_name, value)
                    log.dtrace('[hou] Parameter %s = %s' % (parm_name, repr(value)))
            
            # normal case, recurse to generate the upstream shader network and
            # link the parameter to its output
            else:
                input_anode = self.generateVop(input_vop) # recurse
                
                # special cases: ramp_float, ramp_rgb
                if arnold_type in ('ramp_float', 'ramp_rgb'):
                    if parm_name[:len('position')] == 'position':
                        parm_name = 'position[%i]' % (int(parm_name[len('position'):]) - 1)
                    elif parm_name[:len('color')] == 'color':
                        parm_name = 'color[%i]' % (int(parm_name[len('color'):]) - 1)
                    elif parm_name[:len('value')] == 'value':
                        parm_name = 'value[%i]' % (int(parm_name[len('value'):]) - 1)
                    elif parm_name[:len('interp')] == 'interp':
                        parm_name = 'interpolation[%i]' % (int(parm_name[len('interp'):]) - 1)

                if output_index == 0: # default output
                    AiNodeLink(input_anode, parm_name, shader)
                else: # output component
                    AiNodeLinkOutput(input_anode, input_vop.outputNames()[output_index], shader, parm_name)

        return shader
