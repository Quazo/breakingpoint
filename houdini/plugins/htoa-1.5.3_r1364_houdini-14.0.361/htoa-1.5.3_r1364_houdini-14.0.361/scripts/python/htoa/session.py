# $Id: session.py 1361 2015-06-16 11:48:49Z kik $

import os
import errno
import glob
import sys
import getpass
import tempfile
import time
import uuid
import re
import json
import ctypes

import hou
import soho

from arnold import *

import htoa_pygeo

import htoa.log as log
import htoa.object.factory
import htoa.searchpath
import htoa.ipr
import htoa.license
import htoa
from htoa.material import HaMaterial
from htoa.object.rop import HaRop
from htoa.universe import HaUniverse
from htoa.object.object import HaObject, HA_MATRIX_IDENTITY
from htoa.utils import mkdirs

def tellHick(arglist=[]):
    '''Print commands for hick on stdout''' 

    for item in arglist:
        print item
        

class HaSession(object):
    '''Render session'''
    
    def __init__(self):
        ## Session's HaCamera dict keyed by name (path)
        self.cameras = {}
        
        ## Session's HaLight dict keyed by name (path)
        self.lights = {}
    
        ## Arnold shader node dict keyed by vop path
        self.shaders = {}
        
        ## Material dict keyed by shop path
        self.materials = {}
        
        ## Volume material dict keyed by shop path
        self.volume_materials = {}
        
        ## Houdini Matte objects dict keyed by path, value is the matte color
        self.matte_objects = {}
        
        ## Arnold Matte nodes dict keyed by arnold node name, value is the matte color
        self.matte_nodes = {}
        
        ## Phantom objects keyed by name (path)
        self.phantoms = {}
        
        ## Generated instances IDs
        self.instances = set([])
        
        ## Arnold shape nodes keyed by obj path
        self.shapes = {}
        
        ## object-centric shadow mask, ie. lights keyed by obj
        self.shadow_mask = {}
        
        ## Time at which the scene is being rendered
        self.now = 0.0
        
        ## Frame at which the scene is being rendered
        self.frame = 1.0
        
        ## The HaRop render operator for this session
        self.rop = None
        
        ## Main camera path
        self.camera_name = None
        
        ## Unique identifier for the session ROP, a UUID stored as a string
        self.uuid = ''

        ## SOHO mode, can be 'default', 'generate' or 'update'
        self.soho_mode = ''
        
        ## fps cache
        self.fps = 24.0
        
        ## 1/fps cache
        self.inv_fps = 1.0 / self.fps

        ## export .asstoc flag
        self.export_asstoc = True

        ## scene bounding box
        self.bbox = None
                
        ## Hook functions to be executed after translation
        self.post_translate_hooks = []
        
        ## Hook functions to be executed after .ass write
        self.post_asswrite_hooks = []
        
        ## Shader search path
        self.shader_searchpath = None
        
        ## Procedural search path
        self.procedural_searchpath = None

        ## Plugin search path
        self.plugin_searchpath = None

        ## Pygeo session object
        self.pygeo_session = None

    @staticmethod
    def getSession():
        '''Returns the current HaSession.

        The sessions are stored per Arnold ROP in the htoa.sessions dictionary, 
        keyed by a UUID automatically generated upon creation or pasting. This
        UUID is stored in the ar_rop_uuid parameter.
    
        The session will be created and added to the global htoa.sessions
        dictionary if it does not exist yet.
    
        @return: The HaSession instance for the current SOHO context.
        @raise AssertionError: rop_path is mandatory when not in SOHO context
        
        '''
        rop_uuid = soho.getOutputDriver().getDefaultedString('ar_rop_uuid', 0, None)[0]

        if not rop_uuid:
            raise AssertionError(rop_uuid)
    
        if not rop_uuid in htoa.sessions:
            htoa.sessions[rop_uuid] = HaSession()
    
        return htoa.sessions[rop_uuid]

    def __del__(self):
        '''Destructor. Will clean the universe if it is ours.'''
        universe = HaUniverse()
        if universe.isMine(self.uuid):
            universe.destroy()
            
    def suicide(self):
        '''Destroy ourselves'''
        del htoa.sessions[self.uuid]
        
    def isInteractiveRender(self):
        rx = re.compile('(^ip$|^socket|^iprsocket):*([0-9]*)')
        return rx.search(self.sprop('ar_picture')) != None
    
    def writeAss(self, filename, mask = AI_NODE_ALL, open_procs = False, binary = True):
        '''Write .ass file of current universe and run post .ass write hooks.
        @see: AiASSWrite()
        '''
        # ass header        
        app_string = 'HtoA %s, ' % htoa.__version__
        app_string += 'Houdini %s, ' % self.sprop('state:houdiniversion')
        app_string += 'user: %s, ' % getpass.getuser()
        app_string += 'scene: %s, ' % os.path.join(self.sprop('$HIP'), self.sprop('$HIPNAME'))
        app_string += 'frame: %f, ' % self.frame
        app_string += 'fps: %f' % self.fps
        AiSetAppString(app_string)
        
        ret = AiASSWrite(filename, mask, open_procs, binary)
        
        # exit SOHO translation in case of error when writing the .ass file
        if ret != 0:
            soho.error('[htoa] Error while writing ASS file (%i)' % ret)
        
        # post .ass write hooks
        for hook, arg_dict in self.post_asswrite_hooks:
            arg_dict.update({'filename': filename})
            hook(arg_dict)
            
        # scene is unuseable after AiASSWrite(), even when successful
        HaUniverse().setDirty(True)

        return ret

    def prefixSuffixNodesNames(self, mask = AI_NODE_ALL):
        '''Prefix / suffix node names'''
        node_prefix = self.rop.sprop('ar_node_prefix', defvalue=[''], override_suffix='_enable')
        node_suffix = self.rop.sprop('ar_node_suffix', defvalue=[''], override_suffix='_enable')
        
        if not (node_prefix == node_suffix == ''):
            node_it = AiUniverseGetNodeIterator(mask | ~AI_NODE_OPTIONS)
            while not AiNodeIteratorFinished(node_it):
                node = AiNodeIteratorGetNext(node_it)
                node_name = AiNodeGetName(node)
                if node_name in ('ai_default_reflection_shader', 'ai_error_shader', 'ai_bad_shader'):
                    continue
                node_name = '%s%s%s' % (node_prefix, node_name, node_suffix)
                AiNodeSetStr(node, 'name', node_name)
            AiNodeIteratorDestroy(node_it)

    def exportNodeMask(self):
        node_mask = AI_NODE_UNDEFINED

        if self.rop.iprop('ar_ass_export_options'):
            node_mask |= AI_NODE_OPTIONS
        if self.rop.iprop('ar_ass_export_cameras'):
            node_mask |= AI_NODE_CAMERA
        if self.rop.iprop('ar_ass_export_lights'):
            node_mask |= AI_NODE_LIGHT
        if self.rop.iprop('ar_ass_export_shapes'):
            node_mask |= AI_NODE_SHAPE
        if self.rop.iprop('ar_ass_export_shaders'):
            node_mask |= AI_NODE_SHADER
        if self.rop.iprop('ar_ass_export_overrides'):
            node_mask |= AI_NODE_OVERRIDE
        if self.rop.iprop('ar_ass_export_drivers'):
            node_mask |= AI_NODE_DRIVER
        if self.rop.iprop('ar_ass_export_filters'):
            node_mask |= AI_NODE_FILTER

        return node_mask

    def exportAss(self, mask = AI_NODE_ALL):
        ass_filename = self.rop.sprop('ar_ass_file')
        expand_procs = self.rop.iprop('ar_ass_expand_procedurals')
        binary_ass = self.rop.iprop('ar_binary_ass')

        # create intermediate directories
        if self.rop.iprop('ar_create_intermediate_directories', defvalue=[True]):
            mkdirs(os.path.dirname(ass_filename))
        
        self.writeAss(ass_filename, mask, expand_procs, binary_ass)
        
        # export asstoc
        if self.export_asstoc and self.bbox:
            asstoc_filename = re.sub('\.ass(\.gz)*$', '.asstoc', ass_filename)

            # if re.sub fails, just add '.asstoc'
            if asstoc_filename == ass_filename:
                asstoc_filename += '.asstoc'

            asstoc = open(asstoc_filename, 'w+')
            asstoc.write('bounds ' + ' '.join([str(s) for s in list(self.bbox.minvec()) + list(self.bbox.maxvec())]))
            asstoc.close()

    def run(self):
        '''Start a render session. The session could be brand new or be
        previously created and we are updating for IPR
        '''
        # make sure arnold is started
        universe = HaUniverse()
        universe.reset()

        self.rop = HaRop(self)
        
        # time and fps
        self.now = soho.getDefaultedFloat('state:time', 0)[0]
        self.frame = hou.timeToFrame(self.now)
        self.fps = self.fprop('state:fps')
        self.inv_fps = 1.0 / self.fps

        # reset hooks
        self.post_translate_hooks = []
        self.post_asswrite_hooks = []
        
        # update asstoc flag and reset scene bounding box
        self.export_asstoc = self.rop.iprop('ar_export_asstoc', defvalue=[True])
        self.bbox = None
        
        # set up logging
        base_flags = AI_LOG_WARNINGS | AI_LOG_ERRORS | AI_LOG_NAN | AI_LOG_TIMESTAMP | AI_LOG_MEMORY | AI_LOG_BACKTRACE | AI_LOG_COLOR
        log_levels = {'warnings': base_flags,
                      'info': base_flags | AI_LOG_INFO | AI_LOG_PROGRESS,
                      'detailed': AI_LOG_ALL & ~AI_LOG_DEBUG & ~AI_LOG_PLUGINS,
                      'debug': AI_LOG_ALL & ~AI_LOG_PLUGINS}

        verbosity = log_levels[self.rop.sprop('ar_log_verbosity')]
        
        if self.rop.iprop('ar_log_plugins'):
            verbosity |= AI_LOG_PLUGINS
        
        if self.rop.iprop('ar_log_console_enable'):
            AiMsgSetConsoleFlags(verbosity)
        else:
            AiMsgSetConsoleFlags(AI_LOG_NONE)
            
        if self.rop.iprop('ar_log_file_enable'):
            # TODO check file permissions
            AiMsgSetLogFileFlags(verbosity)
            AiMsgSetLogFileName(self.rop.sprop('ar_log_file'))

        AiMsgSetMaxWarnings(self.rop.iprop('ar_log_max_warnings'))
        log.enable_trace = self.rop.iprop('ar_log_trace_enable')
        os.environ['HTOA_LOG_TRACE'] = '1' if log.enable_trace else '0'

        # early test for .ass filename
        if self.rop.iprop('ar_ass_export_enable') and not self.rop.sprop('ar_ass_file'):
            soho.error('[htoa] Cannot export, empty ASS filename')

        # plugin search path
        plugin_paths = [htoa.searchpath.plugin]
        
        # add driver path in interactive render contexts
        if self.iprop('ar_overridden') or self.sprop('ar_picture') == 'ip':
            plugin_paths.append(htoa.searchpath.driver)
        
        # shader search path
        self.shader_searchpath = self.rop.sprop('ar_shader_searchpath')
        if self.shader_searchpath:
            plugin_paths.append(self.shader_searchpath)
            
        self.plugin_searchpath = os.pathsep.join(plugin_paths)
        
        # procedural search path
        self.procedural_searchpath = self.rop.sprop('ar_procedural_searchpath')
        self.procedural_searchpath = htoa.searchpath.procedural + os.pathsep + self.procedural_searchpath if self.procedural_searchpath else htoa.searchpath.procedural

        # load arnold plugins
        AiLoadPlugins(self.plugin_searchpath)
        
        # setup IPR
        self.uuid = self.rop.sprop('ar_rop_uuid')
        self.soho_mode = self.sprop('state:previewmode', 'default')
        
        # initialize SOHO
        camera_list = soho.getDefaultedString('camera', ['/obj/ipr_camera'])
        self.camera_name = camera_list[0]
        
        # FIXME: Skip generation if we are rendering a render region for the
        # first time as it's always bogus then. The first generation is always
        # followed by an update, force generation then. See #66, comment:10.
        #
        # The following condition is we in the first render region render. Note
        # that Mantra could have done the first region render already.
        # 
        # The conditions are:
        # - We must be in generate mode
        # - The camera is a hidden camera created on the fly by Houdini that is
        #   matching the viewport and named "/obj/ipr_camera#"
        # - We are rendering a region render (ar_overridden == 2)
        #
        if htoa.render_region_might_skip_generate and self.soho_mode == 'generate' and self.camera_name.startswith('/obj/ipr_camera') and self.iprop('ar_overridden') == 2:
            # the bug only happens for the very first render region, so avoid
            # any further checks 
            htoa.render_region_might_skip_generate = False
            
            # the main symptom is that the camera's transform is the identity
            cam_xform = soho.getObject(self.camera_name).getDefaultedFloat('space:world', self.now, [])
            if cam_xform == HA_MATRIX_IDENTITY:
                # force generation on the next update
                htoa.render_region_force_generate = True
                log.debug('First region render, skip generation')
                return 0

        # the first bogus render region generation is always immediately
        # followed by an update, force generation then
        if htoa.render_region_force_generate:
            htoa.render_region_force_generate = False
            log.debug('First region render update, force generation')
            self.soho_mode = 'generate'

        log.debug('Session UUID: %s' % self.uuid)
        log.debug('SOHO mode: %s' % self.soho_mode)

        universe.take(self.uuid)
        universe.setDirty(False)

        # pygeo session
        self.pygeo_session = htoa_pygeo.Session(self.rop.path, self.now)
        
        # there's no camera in the scene, create a dummy one to keep SOHO happy
        if not hou.node(self.camera_name):
            export_camera = hou.node('/obj').createNode('cam', node_name='htoa_export_cam')
            export_camera_name = export_camera.name()
            log.debug('Export Camera: %s' % export_camera_name)
            camera_list = [export_camera_name]
        else:
            export_camera = None
        
        log.debug('Camera: %s' % self.camera_name)
        
        if not soho.initialize(self.now, camera_list):
            soho.error('[htoa] Cannot find cameras "%s"' % repr(camera_list))
        
        # add objects to the scene
        self.selectObjects()

        # reset cache dicts
        self.objects = {}
        self.shaders = {}
        self.materials = {}
        self.volume_materials = {}
        self.shapes = {}
        self.shadow_mask = {}

        # always generate rop
        self.rop.generate()

        if self.soho_mode == 'update':
            self.generateCameras()
            self.updateLights()
        else:
            # Generate world
            self.generate()
        
        # post translate hooks
        for hook, arg_dict in self.post_translate_hooks:
            hook(arg_dict)
        
        # exporting an .ass file
        if not self.iprop('ar_overridden') and self.rop.iprop('ar_ass_export_enable'):
            node_mask = self.exportNodeMask()
            
            # prefix / suffix node names
            self.prefixSuffixNodesNames(node_mask)
            
            # export .ass and .asstoc files
            self.exportAss(node_mask)
                        
            # if the ROP was created prior to r792, the hick pipe command might
            # get launched even if we are just writing an ass file, so tell
            # it to exit gracefully (#328).
            if self.rop.iprop('soho_outputmode') != 2:
                tellHick(['exit'])
            
        # really rendering, not exporting an .ass file
        else:
            # Write a temporary .ass file in the system temp folder and spawn
            # kick on it to render. This way Houdini is still responsive and
            # the process can be killed from MPlay.
            
            # ensure the per-user htoa temp dir exists
            ass_tempdir = os.path.join(tempfile.gettempdir(), 'htoa_%s' % getpass.getuser())
            try:
                os.makedirs(ass_tempdir)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
            
            # FIXME: quick hack, delete all temp ass file older than 5 minutes
            # in this directory, they should have been loaded already
            for ass in glob.glob(os.path.join(ass_tempdir, '*')):
                try:
                    if (time.time() - os.path.getmtime(ass)) / 60 > 5:
                        os.remove(ass)
                except:
                    pass
                
            # skip license check if we could not find any valid licencing
            if htoa.license.skip:
                AiNodeSetBool(AiUniverseGetOptions(), 'skip_license_check', True)
            
            if self.soho_mode in ('default', 'generate'):
                # build temporary .ass file path
                ass_filename = '%s_%s.ass' % (str(os.getpid()), str(uuid.uuid4()))
                ass_path = os.path.join(ass_tempdir, ass_filename) 
                self.writeAss(ass_path, AI_NODE_ALL, False)
            
            # send logging options
            tellHick(['log_verbosity: %i' % verbosity])
            tellHick(['log_console_enable: %i' % self.rop.iprop('ar_log_console_enable')])
            tellHick(['log_file: %s' % (self.rop.sprop('ar_log_file') if self.rop.iprop('ar_log_file_enable') else '')])
            tellHick(['log_max_warnings: %i' % self.rop.iprop('ar_log_max_warnings')])

            # AA
            aa_samples = self.rop.iprop('ar_AA_samples')
            aa_start = self.rop.iprop('ar_AA_initial') if self.iprop('ar_progressive') and self.isInteractiveRender() else aa_samples
            tellHick(['AA: %i %i' % (aa_start, aa_samples)])
            
            # tell hick if the render context supports updates
            if self.iprop('ar_interactive'):
                tellHick(['interactive'])
            
            if self.soho_mode == 'update':
                # update resolution and render region with tel hick because
                # those settings are specific to each context
                options = AiUniverseGetOptions()
                xres = AiNodeGetInt(options, "xres")
                yres = AiNodeGetInt(options, "yres")
                region_min_x = AiNodeGetInt(options, 'region_min_x')
                region_max_x = AiNodeGetInt(options, 'region_max_x')
                region_min_y = AiNodeGetInt(options, 'region_min_y')
                region_max_y = AiNodeGetInt(options, 'region_max_y')
                tellHick(['update_resolution: %i %i %i %i %i %i' % (xres,
                                                                    yres,
                                                                    region_min_x,
                                                                    region_max_x,
                                                                    region_min_y,
                                                                    region_max_y)])

                # skip those parameters
                options_skip = ['camera', 'xres',  'yres', 'region_min_x', 'region_max_x', 'region_min_y', 'region_max_y']
                htoa.ipr.publish(htoa.ipr.delta(options, skip=options_skip))
                
                xform_skip = ['position', 'look_at', 'up']
                for cam in self.cameras.itervalues():
                    htoa.ipr.publish(htoa.ipr.delta(cam, skip=xform_skip))
                    
                for light in self.lights.itervalues():
                    htoa.ipr.publish(htoa.ipr.delta(light, skip=xform_skip))
                
                # update object transform
                for soho_obj in soho.objectList('objlist:dirtyinstance'):
                    ha_obj = HaObject(self, soho_obj)
                    delta = {}
                    delta['action'] = htoa.ipr.UPDATE_OBJ
                    delta['name'] = ha_obj.path
                    delta['parameters'] = {}
                    delta['parameters']['matrix'] = {'type': AI_TYPE_ARRAY, 'value': ha_obj.getMatrixValueDict()}
                    htoa.ipr.publish(delta)

            # if self.soho_mode in ('default', 'generate'):
            else:
                # send the delta publisher port on which to connect
                tellHick(['delta_publisher_port: %i' % htoa.ipr.deltaPublisherPort()])

                # write the ass filename on stdout so that the hick pipe command
                # will pick it up, load it and render it.
                tellHick(['assfile: ' + ass_path])
                
        # FIXME: get rid of this
        universe.destroy()
        universe.release()
        self.suicide()

        # destroy dummy export camera
        if export_camera:
            export_camera.destroy()
    
    def selectObjects(self):
        '''
        Add objects to the scene. We check for parameters on the viewing
        camera.  If the parameters don't exist there, they will be picked up
        by the output driver. The selected objects are locked at the end of
        this method.
        '''
        for cam in soho.objectList('objlist:camera'):
            break
        else:
            soho.error("[htoa] Unable to find viewing camera for render")

        ## Scene objects selection parameters
        candidate_objects = self.sprop('vobject', ['*'])
        candidate_lights = self.sprop('alights', ['*'])
        candidate_fogs = self.sprop('vfog', ['*'])
        force_objects = self.sprop('forceobject', [''])
        force_lights = self.sprop('forcelights', [''])
        force_fogs = self.sprop('forcefog', [''])
        exclude_objects = self.sprop('excludeobject', [''])
        exclude_lights = self.sprop('excludelights', [''])
        exclude_fogs = self.sprop('excludefog', [''])
        solo_lights = self.sprop('sololight', [''])
        matte_objects = self.sprop('matte_objects', [''])
        phantom_objects = self.sprop('phantom_objects', [''])
        force_lights_parm = 'forcelights'
        if solo_lights:
            candidate_lights = exclude_lights = ''
            force_lights = solo_lights
            force_lights_parm = 'sololight'
        
        # Obtain the list of cameras through which we need to render. The main
        # camera may specify a few sub-cameras, for example, in the stereo
        # camera case.
        camera_paths = self.sprop('vm_cameralist', ['']).split()
        self.camera_list  = []
        for cam_path in camera_paths:
            self.camera_list.append(soho.getObject(cam_path))
        if len(self.camera_list) == 0:
            cam.storeData('NoFileSuffix', True)
            self.camera_list.append(cam)
        
        # First, we add objects based on their display flags or dimmer values
        soho.addObjects(self.now, candidate_objects, candidate_lights,
                        candidate_fogs, True, geo_parm='vobject',
                        light_parm='alights', fog_parm='vfog')
        soho.addObjects(self.now, force_objects, force_lights, force_fogs,
                        False, geo_parm='forceobject',
                        light_parm=force_lights_parm, fog_parm='forcefog')
        
        # Force matte & phantom objects to be visible too
        if matte_objects:
            soho.addObjects(self.now, matte_objects, '', '', False,
                            geo_parm='matte_objects', light_parm='', fog_parm='')
        if phantom_objects:
            soho.addObjects(self.now, phantom_objects, '', '', False,
                            geo_parm='phantom_objects', light_parm='', fog_parm='')
        soho.removeObjects(self.now, exclude_objects, exclude_lights, exclude_fogs,
                           geo_parm='excludeobject', light_parm='excludelights',
                           fog_parm='excludefog')

        # Lock off the objects we've selected
        soho.lockObjects(self.now)
        
        # Matte objects
        self.matte_nodes = {}
        self.matte_objects = {}
        for obj in soho.getOutputDriver().objectList('objlist:instance', self.now, matte_objects):
            self.matte_objects[obj.getName()] = (0.0, 0.0, 0.0, 0.0)
            
        # Phantom objects
        self.phantoms = {}
        for obj in soho.getOutputDriver().objectList('objlist:instance', self.now, phantom_objects):
            self.phantoms[obj.getName()] = True

    def generate(self):
        '''Generate the Arnold scene'''
        
        # cameras
        self.generateCameras()
            
        # objects
        shader_dict = {}
        for soho_obj in soho.objectList('objlist:instance'):
            shdict = htoa.object.factory.generate(self, soho_obj)
            if shdict:
                shader_dict.update(shdict)
            
            # update scene bounding box for .asstoc
            if self.export_asstoc:
                obj_hnode = hou.node(soho_obj.getName())
                
                # It is common that the render SOP is just a Null because we 
                # are just displaying a proxy in the viewport, whose
                # geometry is not not be rendered, like a bounding box for
                # example. This is why we first check if the geometry is not
                # empty, ie. it has at least one primitive.
                try:
                    geo_render = obj_hnode.renderNode().geometry()
                    geo_render.iterPrims()[0] # throws exception if geometry is empty
                    obj_bbox = geo_render.boundingBox()
                    
                # fallback to the display SOP
                except:
                    # the object could contain no geometry at all, see test_0015
                    try:
                        obj_bbox = obj_hnode.displayNode().geometry().boundingBox()
                    except:
                        obj_bbox = None
                
                if obj_bbox:
                    obj_bbox *= obj_hnode.worldTransform()

                    if self.bbox:
                        self.bbox.enlargeToContain(obj_bbox)
                    else:
                        self.bbox = obj_bbox
            
        # lights
        self.generateLights()

        # materials
        self.generateShaders(shader_dict)

    def generateCameras(self):
        for cam_path in self.rop.cameras:
            if hou.node(cam_path):
                self.cameras[cam_path] = htoa.object.factory.generate(self, soho.getObject(cam_path), 'camera')

    def generateLights(self):
        for soho_light in soho.objectList('objlist:light'):
            self.lights[soho_light.getName()] = htoa.object.factory.generate(self, soho_light, 'light')
        
        # shadow groups
        for obj, lights in self.shadow_mask.iteritems():
            
            if len(self.lights) == len(lights):
                continue
            
            light_array = AiArrayAllocate(len(lights), 1, AI_TYPE_NODE)
            
            for i, light_name in enumerate(lights):
                light_node = AiNodeLookUpByName(light_name)
                AiArraySetPtr(light_array, i, light_node)

            for shape_node in self.shapes[obj]:
                AiNodeSetBool(shape_node, "use_shadow_group", True)
                AiNodeSetArray(shape_node, "shadow_group", AiArrayCopy(light_array))
                
            AiArrayDestroy(light_array)

    def generateShaders(self, shader_dict):
        '''Generate and link all Arnold shaders'''
        
        for anode_ptr, shop_paths in shader_dict.iteritems():
            anode = cast(anode_ptr, ctypes.POINTER(AtNode))
            anode_entry = AiNodeGetNodeEntry(anode)
            anode_type = AiNodeEntryGetName(anode_entry)
            is_volumic = anode_type == 'volume' or (anode_type in ('sphere', 'box', 'points') and AiNodeGetFlt(anode, 'step_size') > 0) 
            shaders = []
            
            for shop_path in shop_paths:
                if is_volumic:
                    if shop_path in self.volume_materials:
                        shaders.append(self.volume_materials[shop_path])
                    else:
                        volume_shader_dict = HaMaterial(self, shop_path).generateMaterial(is_volumic)
                        self.volume_materials.update({shop_path: volume_shader_dict})
                        shaders.append(volume_shader_dict)
                else:
                    if shop_path in self.materials:
                        shaders.append(self.materials[shop_path])
                    else:
                        material_shader_dict = HaMaterial(self, shop_path).generateMaterial(is_volumic)
                        self.materials.update({shop_path: material_shader_dict})
                        shaders.append(material_shader_dict)

            # early out if we don't have any shaders
            if shaders == [{}] or shaders == []:
                continue
            
            # volumes have a single shader, use the first shop in the list
            if is_volumic:
                vol_shader = shaders[0]['volume'] if shaders[0].has_key('volume') else None
                AiNodeSetPtr(anode, 'shader', vol_shader)
                
            else:
                surf_shader_array = AiArrayAllocate(len(shaders), 1, AI_TYPE_POINTER)
                disp_shader_array = AiArrayAllocate(len(shaders), 1, AI_TYPE_POINTER)
                
                has_disp = False
                
                for i in xrange(len(shaders)):
                    surf_shader = shaders[i]['surface'] if shaders[i].has_key('surface') else None
                    disp_shader = shaders[i]['disp'] if shaders[i].has_key('disp') else None
                    AiArraySetPtr(surf_shader_array, i, surf_shader)
                    AiArraySetPtr(disp_shader_array, i, disp_shader)
                    
                    # do not displace at all unless at least one displacement
                    # shader exists
                    if not has_disp and disp_shader:
                        has_disp = True 
                        
                AiNodeSetArray(anode, 'shader', surf_shader_array)

                if has_disp:
                    AiNodeSetArray(anode, 'disp_map', disp_shader_array)

    def update(self):
        '''Update the Arnold scene.'''
        for t in self.translators:
            t.update()
            
    def updateLights(self):
        for soho_light in soho.objectList('objlist:dirtylight'):
            self.lights[soho_light.getName()] = htoa.object.factory.generate(self, soho_light, 'light')
            
    @staticmethod
    def fprop(token, defvalue=[]):
        '''Convenience function to evaluate a global float SOHO token or property.
        
        Returns a float or a list of floats depending on the property being
        evaluated. Unlike soho.getDefaultedFloat(), a single float
        value (and not a single element list) unless the return value is a list
        containing at least two elements.
        
        @param token: SOHO token or object property name. 
        @param defvalue: A default value to be returned if the queried property
        does not exist on the object. The default default [] will return None
        if the property does not exist.
        @return: Evaluated parameter as a float or list of floats
        @see: iprop(), sprop(), HaObject.fprop(), soho.getDefaultedFloat(),
        <a href="http://www.sidefx.com/docs/hdk11.1/namespace_h_d_k___s_o_h_o___a_p_i.html#d20dbd9df7fab2cd565affc43c719518">
        sohoglue.evaluate()</a>.
        
        '''
        res = soho.getDefaultedFloat(token, defvalue)
        res_size = len(res)
        if res_size == 0:
            return None
        elif res_size == 1:
            return res[0]
        else:
            return res
    
    @staticmethod 
    def iprop(token, defvalue=[]):
        '''Convenience function to evaluate a global integer SOHO token or property.
        
        This is the integer counterpart of fprop().
        @see: fprop(), sprop(), soho.getDefaultedInt()
        
        '''
        res = soho.getDefaultedInt(token, defvalue)
        res_size = len(res)
        if res_size == 0:
            return None
        elif res_size == 1:
            return res[0]
        else:
            return res
    
    @staticmethod
    def sprop(token, defvalue=[]):
        '''Convenience function to evaluate a global string SOHO token or property.
        
        This is the string counterpart of fprop().
        @see: fprop(), siprop(), soho.getDefaultedString()
        
        '''
        res = soho.getDefaultedString(token, defvalue)
        res_size = len(res)
        if res_size == 0:
            return None
        elif res_size == 1:
            return res[0]
        else:
            return res
