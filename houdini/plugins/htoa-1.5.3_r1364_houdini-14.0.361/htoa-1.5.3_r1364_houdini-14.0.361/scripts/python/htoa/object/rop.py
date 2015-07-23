# $Id: rop.py 1358 2015-06-15 16:39:12Z kik $

import re

import os
import hou
import soho
from arnold import *

from htoa.object.object import HaObject
import htoa.log as log
from htoa.material import HaMaterial
from htoa.node.parms import *
from htoa.utils import mkdirs
from htoa.node.node import pullSohoParms

class HaAov(object):
    '''Arnold AOV'''
    
    def __init__(self):
        self.label = None
        self.file = None
        self.picture_format = None
        self.type = None
        self.pixel_filter = None
        self.camera = None

class HaRop(HaObject):
    '''Translator for the session's ROP.'''
    
    def __init__(self, session):
        '''Constructor'''
        
        # call superclass constructor
        self._init(session, soho.getOutputDriver(), init_motion_blur=False)
        
        ## Cameras to export
        self.cameras = set([])

    def generate(self, index=None):
        '''Generate Arnold options
        @param index: ignored
        '''
        log.debug('Generating ROP %s' % self.path)
        options = AiUniverseGetOptions()
        
        # frame number as user data on options
        AiNodeDeclare(options, 'frame', 'constant FLOAT')
        AiNodeSetFlt(options, 'frame', hou.timeToFrame(self.session.now))
        
        # main driver
        filename = self.session.sprop('ar_picture')
        picture_format = self.sprop('ar_picture_format')
        allow_aov_separate = True
        
        # Export all the cameras

        # Collect all the cameras using a bundle
        bundle = hou.nodeBundle('htoa_cameras')
        if (bundle == None):
            bundle = hou.addNodeBundle('htoa_cameras')
            bundle.setFilter(hou.nodeTypeFilter.ObjCamera)
            bundle.setPattern('*')
        for cam in bundle.nodes():
            # we must further test the type, because there are 2 cases in the testsuite (31, 39)
            # for which the bundle filters-in objects of type other than camera
            if cam.type().description() == 'Camera':
                self.cameras.add(cam.path())

        # Don't destroy the bundle, else every time the bundle gets re-created 
        # the ipr updates. This is very annoying if we have two rendering (region, view)
        # running, they feed each other with the new bundle and never stop refreshing.
        # The disadvantage is that if the user saves the scene, the bundle gets saved as well.
        # bundle.destroy()
        
        # if we are in an interactive rendering mode (mplay, renderviewer,
        # render region, etc.) then insert our custom driver
        rx = re.compile('(^ip$|^socket|^iprsocket):*([0-9]*)')
        mo = rx.search(filename)
        if mo:
            # use a default exr driver instead of driver_houdini when exporting to .ass and filename is 'ip'
            if not self.session.iprop('ar_overridden') and self.iprop('ar_ass_export_enable'):
                driver = AiNode('driver_exr')
            else:            
                driver = AiNode('driver_houdini')
                allow_aov_separate = False
                picture_format = mo.group(1)
                if picture_format != 'ip':
                    HaNodeSetUInt(driver, 'port', int(mo.group(2)))
                    
                asparm = hou.parm(self.session.camera_name + '/aspect')
                if asparm:
                    HaNodeSetFlt(driver, 'aspect', asparm.evalAsFloat())
                
                # render region does not support native tile borders
                if self.session.iprop('ar_overridden') == 2:
                    HaNodeSetBool(driver, 'borders_as_tiles', True)
                    
                HaNodeSetFlt(driver, 'frame', hou.frame())
                    
        # rendering to a file driver
        else:
            driver = AiNode('driver_' + picture_format)
            HaNodeSetStr(driver, 'filename', filename)
            
            # create intermediate directories
            if self.iprop('ar_create_intermediate_directories', defvalue=[True]):
                mkdirs(os.path.dirname(filename))
            
            if picture_format == 'exr':
                HaNodeSetStr(driver, 'compression', self.sprop('ar_exr_compression'))
                HaNodeSetBool(driver, 'half_precision', self.iprop('ar_exr_half_precision'))
                HaNodeSetBool(driver, 'tiled', self.iprop('ar_picture_tiling'))
                HaNodeSetBool(driver, 'preserve_layer_name', self.iprop('ar_exr_preserve_layer_name'))
                HaNodeSetBool(driver, 'autocrop', self.iprop('ar_exr_autocrop'))
                HaNodeSetBool(driver, 'append', self.iprop('ar_picture_append'))
                
                # exr metadata
                metadata = []
                for i in xrange(1, 1 + self.iprop('ar_exr_metadata', defvalue=[0])):
                    metadata_key = self.sprop('ar_exr_metadata_key%i' % i)
                    if metadata_key:
                        if ' ' in metadata_key:
                            metadata_key = "'%s'" % metadata_key
                        metadata_type = self.sprop('ar_exr_metadata_type%i' % i)
                        metadata_values = ' '.join([str(x) for x in self.hou_node.parmTuple('ar_exr_metadata_%s_value%i' % (metadata_type, i)).eval()])
                        metadata.append('%s %s %s' % (metadata_type, metadata_key, metadata_values))
                        
                log.dtrace('exr metadata = %s' % repr(metadata))
                
                metadata_count = len(metadata)
                if metadata_count:
                    metadata_array = AiArrayAllocate(metadata_count, 1, AI_TYPE_STRING)
                    for i in xrange(metadata_count):
                        AiArraySetStr(metadata_array, i, metadata[i])
                    HaNodeSetArray(driver, 'custom_attributes', metadata_array)

            elif picture_format == 'deepexr':
                HaNodeSetBool(driver, 'tiled', self.iprop('ar_picture_tiling'))
                HaNodeSetBool(driver, 'subpixel_merge', self.iprop('ar_deepexr_subpixel_merge'))
                HaNodeSetBool(driver, 'use_RGB_opacity', self.iprop('ar_deepexr_use_RGB_opacity'))
                HaNodeSetFlt(driver, 'alpha_tolerance', self.fprop('ar_deepexr_alpha_tolerance'))
                HaNodeSetFlt(driver, 'depth_tolerance', self.fprop('ar_deepexr_depth_tolerance'))
                HaNodeSetBool(driver, 'alpha_half_precision', self.iprop('ar_deepexr_alpha_half_precision'))
                HaNodeSetBool(driver, 'depth_half_precision', self.iprop('ar_deepexr_depth_half_precision'))
                deepexr_layer_tolerance = [self.fprop('ar_deepexr_beauty_tolerance')]
                deepexr_layer_enable_filtering = [self.iprop('ar_deepexr_enable_filtering')]
                deepexr_layer_half_precision = [self.iprop('ar_deepexr_beauty_half_precision')]
                
            elif picture_format == 'tiff':
                HaNodeSetStr(driver, 'compression', self.sprop('ar_tiff_compression'))
                HaNodeSetStr(driver, 'format', self.sprop('ar_tiff_format'))
                HaNodeSetBool(driver, 'tiled', self.iprop('ar_picture_tiling'))
                HaNodeSetFlt(driver, 'gamma', self.fprop('ar_output_driver_gamma'))
                HaNodeSetBool(driver, 'dither', self.iprop('ar_picture_dither'))
                HaNodeSetBool(driver, 'unpremult_alpha', self.iprop('ar_tiff_unpremult_alpha'))
                HaNodeSetBool(driver, 'skip_alpha', self.iprop('ar_tiff_skip_alpha'))
                HaNodeSetBool(driver, 'append', self.iprop('ar_picture_append'))
                HaNodeSetBool(driver, 'output_padded', self.iprop('ar_picture_output_padded'))
            
            elif picture_format == 'png':
                HaNodeSetStr(driver, 'format', self.sprop('ar_png_format'))
                HaNodeSetFlt(driver, 'gamma', self.fprop('ar_output_driver_gamma'))
                HaNodeSetBool(driver, 'dither', self.iprop('ar_picture_dither'))
                HaNodeSetBool(driver, 'output_padded', self.iprop('ar_picture_output_padded'))
            
            elif picture_format == 'jpeg':
                HaNodeSetInt(driver, 'quality', self.iprop('ar_jpeg_quality'))
                HaNodeSetFlt(driver, 'gamma', self.fprop('ar_output_driver_gamma'))
                HaNodeSetBool(driver, 'dither', self.iprop('ar_picture_dither'))
                HaNodeSetBool(driver, 'output_padded', self.iprop('ar_picture_output_padded'))

        driver_name = self.path + ':' + picture_format
        HaNodeSetStr(driver, 'name', driver_name)

        # main pixel filter
        filter_type = self.sprop('ar_pixel_filter_type')
        filter_name = self.path + ':' + filter_type
        pixel_filter = AiNode(filter_type)
        HaNodeSetStr(pixel_filter, 'name', filter_name)
        
        # filter width
        if filter_type in [f + '_filter' for f in 'disk gaussian cook variance cone triangle'.split()]:
            HaNodeSetFlt(pixel_filter, 'width', self.fprop('ar_pixel_filter_width'))
            
        elif filter_type == 'blackman_harris_filter':
            HaNodeSetFlt(pixel_filter, 'width', self.fprop('ar_pixel_filter_width_blackman_harris'))
        
        elif filter_type == 'sinc_filter':
            HaNodeSetFlt(pixel_filter, 'width', self.fprop('ar_pixel_filter_width_sinc'))
            
        # misc filter parameters
        if filter_type == 'farthest_filter':
            HaNodeSetStr(pixel_filter, 'domain', self.sprop('ar_pixel_filter_farthest_domain'))
            
        if filter_type == 'variance_filter':
            HaNodeSetBool(pixel_filter, 'scalar_mode', self.iprop('ar_pixel_filter_variance_scalar_mode'))
            
        if filter_type == 'heatmap_filter':
            HaNodeSetFlt(pixel_filter, 'minimum', self.fprop('ar_pixel_filter_heatmap_minimum'))
            HaNodeSetFlt(pixel_filter, 'maximum', self.fprop('ar_pixel_filter_heatmap_maximum'))

        # parse AOVs
        aovs = []
        
        for i in xrange(1, self.session.iprop('ar_aovs') + 1):
            if not self.iprop('ar_enable_aov%i' % i):
                continue
            
            aov = HaAov()
            aov.label = self.sprop('ar_aov_label%i' % i).replace(' ', '_')
            
            if not aov.label:
                continue
            
            if self.iprop('ar_aov_separate%i' % i):
                aov.file = self.sprop('ar_aov_separate_file%i' % i)
                aov.picture_format = self.sprop('ar_aov_picture_format%i' % i)
                
            aov.type = self.sprop('ar_aov_type%i' % i)
            aov.pixel_filter = self.sprop('ar_aov_pixel_filter%i' % i)
            
            aov.camera = self.sprop('ar_aov_camera%i' % i, defvalue=['']).strip()
            if not aov.camera or not self.iprop('ar_aov_camera_enable%i' % i):
                aov.camera = self.session.camera_name # fallback to default camera
                
            aovs.append(aov)

        aov_count = len(aovs)

        # multicam
        is_multicam = self.session.iprop('ar_multicam', defvalue=[False]) and len(self.cameras) != 1

        # we assume RGBA for the main output
        outputs = []
        if is_multicam:
            try:
                # look for a custom camera shader
                camera_name = HaMaterial(self.session, hou.chsop(self.session.camera_name + '/ar_camera_shader')).customCameraVop().path()
            except:
                camera_name = self.session.camera_name
                
            outputs.append('%s RGBA RGBA %s %s' % (camera_name, filter_name, driver_name))
        else:
            outputs.append('RGBA RGBA %s %s' % (filter_name, driver_name))
        
        # create AOVs
        i = 0
        for aov in aovs:
            i += 1
            
            # AOV driver, reuse the main options for the driver parameters
            if aov.file and allow_aov_separate:
                if aov.picture_format == 'beauty':
                    aov.picture_format = picture_format
                    
                aov_driver = AiNode('driver_' + aov.picture_format)
                aov_driver_name = self.path + ':' + aov.picture_format + ':aov%i' % i
                
                HaNodeSetStr(aov_driver, 'name', aov_driver_name)
                HaNodeSetStr(aov_driver, 'filename', aov.file)
                
                # create intermediate directories
                if self.iprop('ar_create_intermediate_directories', defvalue=[True]):
                    mkdirs(os.path.dirname(aov.file))

                if aov.picture_format == 'exr':
                    HaNodeSetStr(aov_driver, 'compression', self.sprop('ar_exr_compression'))
                    HaNodeSetBool(aov_driver, 'half_precision', self.iprop('ar_exr_half_precision'))
                    HaNodeSetBool(aov_driver, 'tiled', self.iprop('ar_picture_tiling'))
                    HaNodeSetBool(aov_driver, 'preserve_layer_name', self.iprop('ar_exr_preserve_layer_name'))
                    HaNodeSetBool(aov_driver, 'append', self.iprop('ar_picture_append'))
    
                elif aov.picture_format == 'deepexr':
                    HaNodeSetBool(aov_driver, 'tiled', self.iprop('ar_picture_tiling'))
                    HaNodeSetBool(aov_driver, 'subpixel_merge', self.iprop('ar_deepexr_subpixel_merge'))
                    HaNodeSetBool(aov_driver, 'use_RGB_opacity', self.iprop('ar_deepexr_use_RGB_opacity'))
                    HaNodeSetFlt(aov_driver, 'alpha_tolerance', self.fprop('ar_deepexr_alpha_tolerance'))
                    HaNodeSetFlt(aov_driver, 'depth_tolerance', self.fprop('ar_deepexr_depth_tolerance'))
                    HaNodeSetBool(aov_driver, 'alpha_half_precision', self.iprop('ar_deepexr_alpha_half_precision'))
                    HaNodeSetBool(aov_driver, 'depth_half_precision', self.iprop('ar_deepexr_depth_half_precision'))
                    HaNodeSetFlt(aov_driver, 'layer_tolerance', self.fprop('ar_aov_deep_merge_tolerance%i' % i))
                    HaNodeSetBool(aov_driver, 'layer_half_precision', self.iprop('ar_aov_deep_half_precision%i' % i))
                    HaNodeSetBool(aov_driver, 'layer_enable_filtering', self.iprop('ar_aov_deep_enable_filtering%i' % i))
    
                elif aov.picture_format == 'tiff':
                    HaNodeSetStr(aov_driver, 'compression', self.sprop('ar_tiff_compression'))
                    HaNodeSetStr(aov_driver, 'format', self.sprop('ar_tiff_format'))
                    HaNodeSetBool(aov_driver, 'tiled', self.iprop('ar_picture_tiling'))
                    HaNodeSetFlt(aov_driver, 'gamma', self.fprop('ar_output_driver_gamma'))
                    HaNodeSetBool(aov_driver, 'dither', self.iprop('ar_picture_dither'))
                    HaNodeSetBool(aov_driver, 'unpremult_alpha', self.iprop('ar_tiff_unpremult_alpha'))
                    HaNodeSetBool(aov_driver, 'skip_alpha', self.iprop('ar_tiff_skip_alpha'))
                    HaNodeSetBool(aov_driver, 'append', self.iprop('ar_picture_append'))
                    HaNodeSetBool(aov_driver, 'output_padded', self.iprop('ar_picture_output_padded'))
                
                elif aov.picture_format == 'png':
                    HaNodeSetStr(aov_driver, 'format', self.sprop('ar_png_format'))
                    HaNodeSetFlt(aov_driver, 'gamma', self.fprop('ar_output_driver_gamma'))
                    HaNodeSetBool(aov_driver, 'dither', self.iprop('ar_picture_dither'))
                    HaNodeSetBool(aov_driver, 'output_padded', self.iprop('ar_picture_output_padded'))
                
                elif aov.picture_format == 'jpeg':
                    HaNodeSetInt(aov_driver, 'quality', self.iprop('ar_jpeg_quality'))
                    HaNodeSetFlt(aov_driver, 'gamma', self.fprop('ar_output_driver_gamma'))
                    HaNodeSetBool(aov_driver, 'dither', self.iprop('ar_picture_dither'))
                    HaNodeSetBool(aov_driver, 'output_padded', self.iprop('ar_picture_output_padded'))
            
            else:
                aov_driver_name = driver_name
                
                if picture_format == 'deepexr':
                    aov.pixel_filter = 'beauty' # all deepexr AOVs must have the same filter
                    deepexr_layer_tolerance.append(self.fprop('ar_aov_deep_merge_tolerance%i' % i))
                    deepexr_layer_enable_filtering.append(self.iprop('ar_aov_deep_enable_filtering%i' % i))
                    deepexr_layer_half_precision.append(self.iprop('ar_aov_deep_half_precision%i' % i))
                
            # use same AOV pixel filter as beauty
            if aov.pixel_filter == 'beauty':
                aov_filter_name = filter_name
                 
            # specific pixel filter
            else:
                aov_filter = AiNode(aov.pixel_filter)
                aov_filter_name = self.path + ':' + aov.pixel_filter + ':aov%i' % i
                HaNodeSetStr(aov_filter, 'name', aov_filter_name)
                
                # filter width
                if aov.pixel_filter in [f + '_filter' for f in 'disk gaussian cook variance cone triangle'.split()]:
                    HaNodeSetFlt(aov_filter, 'width', self.fprop('ar_aov_pixel_filter_width%i' % i))
                    
                elif aov.pixel_filter == 'blackman_harris_filter':
                    HaNodeSetFlt(aov_filter, 'width', self.fprop('ar_aov_pixel_filter_width_blackman_harris%i' % i))
                
                elif aov.pixel_filter == 'sinc_filter':
                    HaNodeSetFlt(aov_filter, 'width', self.fprop('ar_aov_pixel_filter_width_sinc%i' % i))
                    
                # misc filter parameters
                if aov.pixel_filter == 'farthest_filter':
                    HaNodeSetStr(aov_filter, 'domain', self.sprop('ar_aov_pixel_filter_farthest_domain%i' % i))
                    
                if aov.pixel_filter == 'variance_filter':
                    HaNodeSetBool(aov_filter, 'scalar_mode', self.iprop('ar_pixel_filter_variance_scalar_mode'))
                    
                if aov.pixel_filter == 'heatmap_filter':
                    HaNodeSetFlt(aov_filter, 'minimum', self.fprop('ar_aov_pixel_filter_heatmap_minimum%i' % i))
                    HaNodeSetFlt(aov_filter, 'maximum', self.fprop('ar_aov_pixel_filter_heatmap_maximum%i' % i))
            
            if is_multicam:
                outputs.append('%s %s %s %s %s' % (aov.camera, aov.label, aov.type, aov_filter_name, aov_driver_name))
            else:
                outputs.append('%s %s %s %s' % (aov.label, aov.type, aov_filter_name, aov_driver_name))

        # write outputs to options
        outputs_array = AiArrayAllocate(aov_count + 1, 1, AI_TYPE_STRING)
        AiArraySetStr(outputs_array, 0, outputs[0])
        for i in xrange(1, aov_count + 1):
            AiArraySetStr(outputs_array, i, outputs[i])
        HaNodeSetArray(options, 'outputs', outputs_array)

        # deepexr array parameters
        if picture_format == 'deepexr':
            deepexr_nlayers = len(deepexr_layer_tolerance)
            deepexr_layer_tolerance_array = AiArrayAllocate(deepexr_nlayers, 1, AI_TYPE_FLOAT)
            deepexr_layer_enable_filtering_array = AiArrayAllocate(deepexr_nlayers, 1, AI_TYPE_BOOLEAN)
            deepexr_layer_half_precision_array = AiArrayAllocate(deepexr_nlayers, 1, AI_TYPE_BOOLEAN)
            
            for i in xrange(deepexr_nlayers):
                AiArraySetFlt(deepexr_layer_tolerance_array, i, deepexr_layer_tolerance[i])
                AiArraySetBool(deepexr_layer_enable_filtering_array, i, deepexr_layer_enable_filtering[i])
                AiArraySetBool(deepexr_layer_half_precision_array, i, deepexr_layer_half_precision[i])
                
            HaNodeSetArray(driver, 'layer_tolerance', deepexr_layer_tolerance_array)
            HaNodeSetArray(driver, 'layer_enable_filtering', deepexr_layer_enable_filtering_array)
            HaNodeSetArray(driver, 'layer_half_precision', deepexr_layer_half_precision_array)

        # properties that need special handling since they have an "enable" toogle in the rop and when disabled should not be set at all
        if self.iprop('ar_AA_sample_clamp_enable') == 1:
            HaNodeSetFlt(options, 'AA_sample_clamp', self.fprop('ar_AA_sample_clamp'))
        if self.iprop('ar_force_threads') == 1:
            # FIXME this is not written out in the .ass file, see ticket #256
            HaNodeSetInt(options, 'threads', self.iprop('ar_threads'))
        if self.iprop('ar_texture_autotile_enabled') == 1:
            HaNodeSetInt(options, 'texture_autotile', self.iprop('ar_texture_autotile'))
        if self.iprop('ar_GI_falloff_enabled') == 1:
            HaNodeSetFlt(options, 'GI_falloff_start_dist', self.fprop('ar_GI_falloff_start_dist'))
            HaNodeSetFlt(options, 'GI_falloff_stop_dist', self.fprop('ar_GI_falloff_stop_dist'))        
                
        # atmosphere & background
        if self.parm('ar_environment'):
            env_mat = HaMaterial(self.session, self.parm('ar_environment'))
            HaNodeSetPtr(options, 'atmosphere', env_mat.generateAtmosphereShader())
            bg_dict = env_mat.generateBackgroundShader()
            HaNodeSetPtr(options, 'background', bg_dict['shader'])
            HaNodeSetInt(options, 'background_visibility', bg_dict['visibility'])
        
        # all other properties
        pullSohoParms(options, self)
        
        # shader and procedural search paths
        if not self.session.iprop('ar_overridden') and self.iprop('ar_ass_export_enable') and not self.iprop('ar_prepend_htoa_paths', defvalue=[True]):
            HaNodeSetStr(options, 'shader_searchpath', self.sprop('ar_shader_searchpath'))
            HaNodeSetStr(options, 'procedural_searchpath', self.sprop('ar_procedural_searchpath'))
        else:
            HaNodeSetStr(options, 'shader_searchpath', self.session.plugin_searchpath)
            HaNodeSetStr(options, 'procedural_searchpath', self.session.procedural_searchpath)

        # user options
        AiNodeSetAttributes(options, self.parm('ar_user_options', override_suffix='_enable'))
        