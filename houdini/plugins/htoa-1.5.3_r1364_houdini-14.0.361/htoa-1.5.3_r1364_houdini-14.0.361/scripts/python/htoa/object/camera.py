# $Id: camera.py 1358 2015-06-15 16:39:12Z kik $

import hou
import soho

from arnold import *

import htoa.log as log
from htoa.object.object import HaObject, getShutterRange
from htoa.material import HaMaterial
from htoa.node.parms import *
from htoa.node.node import pullSohoParms

## Default Mantra orientation for polar cameras
MANTRA_ORIENTATION = hou.hmath.buildRotateAboutAxis(hou.Vector3(0, 1, 0), -90)

class HaCamera(HaObject):
    '''
    Translator for camera
    '''
    def __init__(self, session, soho_obj):
        '''Constructor'''
        
        # call superclass constructor
        self._init(session, soho_obj)
                                  
    def generate(self, index=None):
        '''Generate Arnold camera
        '''
        node_name = self.path if index is None else '%s:%s' % (self.path, repr(index))

        log.debug('Generating camera %s' % node_name)
        
        rop = self.session.rop
        projection = self.sprop('projection')
        winsize_scale = 1

        try:
            shader_path = hou.chsop(self.path + '/ar_camera_shader')
        except:
            shader_path = None
            
        custom_camera = HaMaterial(self.session, shader_path).generateCustomCamera()
        
        if custom_camera:
            projection = 'custom'
            camera = custom_camera
            node_name = AiNodeGetName(custom_camera)
        
        elif projection == 'perspective':
            aperture = self.fsamples('aperture', defvalue=[41.2136])
            focal_fov = focal_dof = self.fsamples('focal', defvalue=[50])
            fstop = self.fsamples('fstop')
            
            # aperture and focal must have the same length in order to zip them
            # and compute the fov samples. HaObject.fsamples() returns a list
            # of size len(self.xform_times) or 1, so the shortest of the two
            # lists has exactly one element.
            if len(aperture) > len(focal_fov):
                focal_fov = focal_fov * len(aperture)
            elif len(aperture) < len(focal_fov):
                aperture = aperture * len(focal_fov)
            
            af = zip(aperture, focal_fov)
            fov = [math.degrees(2 * math.atan2(a, 2 * f)) for a, f in af]

            if self.iprop('ar_dof_enable', defvalue=[False]):
                
                # we have the ar_aperture_size parameter on the camera
                if self.fprop('ar_aperture_size', defvalue=[-1]) >= 0:
                    aperture_size = self.fsamples('ar_aperture_size')
                    
                # there is no ar_aperture_size parameter, compute the aperture
                # from the filmback size and f-stop of the standard houdini
                # camera
                else:
                    # fstop and focal must have the same length in order to zip
                    # them and compute the aperture_size samples. HaObject.fsamples()
                    # returns a list of size len(self.xform_times) or 1, so the
                    # shortest of the two lists has exactly one element.
                    if len(fstop) > len(focal_dof):
                        focal_dof = focal_dof * len(fstop)
                    elif len(fstop) < len(focal_dof):
                        fstop = fstop * len(focal_dof)
    
                    ff = zip(focal_dof, fstop)
                    unit_scale = soho.houdiniUnitLength(1, self.sprop('focalunits'))
                    aperture_size = [0.5 * unit_scale * foc / fst for foc, fst in ff]
            else:
                aperture_size = [0] # no depth of field
            
            # aperture blades
            if self.iprop('ar_polygonal_aperture', defvalue=[True]):
                aperture_blades = self.iprop('ar_aperture_blades', defvalue=[5])
            else:
                aperture_blades = 0
            
            # create and fill arnold node
            if self.iprop('ar_fisheye', defvalue=[False]):
                camera = AiNode('fisheye_camera')
            else:
                camera = AiNode('persp_camera')
            
            HaNodeSetArray(camera, "fov", HaArrayConvertFloat(fov))
            HaNodeSetArray(camera, "focus_distance", HaArrayConvertFloat(self.fsamples('focus')))
            HaNodeSetArray(camera, "aperture_size", HaArrayConvertFloat(aperture_size))
            HaNodeSetInt(camera, "aperture_blades", aperture_blades)
            
            # uv_remap
            remap_shader = HaMaterial(self.session, shader_path).generateCameraUvRemap()
            if remap_shader:
                AiNodeLink(remap_shader, 'uv_remap', camera)
                        
        elif projection == 'cylinder':
            camera = AiNode('cyl_camera')
            HaNodeSetArray(camera, "horizontal_fov", HaArrayConvertFloat(self.fsamples('ar_horizontal_fov')))
            HaNodeSetArray(camera, "vertical_fov", HaArrayConvertFloat(self.fsamples('ar_vertical_fov')))

        elif projection == 'ortho':
            camera = AiNode('ortho_camera')
            orthowidth = self.fprop('orthowidth')
            winsize_scale = 0.5 * orthowidth

        elif projection == 'sphere':
            camera = AiNode('spherical_camera')
            
        else:
            log.error('Unsupported camera projection: %s' % projection)
            AiNodeDestroy(camera)
            return None
        
        # common to all cameras
        AiNodeSetStr(camera, 'name', node_name)
        pullSohoParms(camera, self)
        
        # match mantra orientation
        if projection in ('sphere', 'cylinder') and self.iprop('ar_camera_mantra_orientation', defvalue=[False]):
            pre_xform = [MANTRA_ORIENTATION] * len(self.xform_times)
        else:
            pre_xform = None
        
        HaNodeSetArray(camera, 'matrix', self.getArnoldMatrix(matrix=pre_xform))

        # shutter start / end
        # Due to limitations in the Arnold core as of Arnold 4.0.10.2, the
        # objet motion shutter is defined globally in the ROP and is mapped
        # to [0, 1]. We must then also map the camera shutter to this range.
        # This cumbersome mapping is to avoid setting the 
        # {transform, deform}_time_samples parameters on the shapes, which
        # is not advised. Until this gets sorted, let's attach the
        # equivalent "info_shutter_start" and "info_shutter_end" user
        # attributes on the camera so that they are written in the .ass
        # file should someone need this information.
        # cf. HtoA ticket #34 and MtoA ticket #571
        rop_shutter_range = getShutterRange(self.session.rop.hou_node)
        rop_shutter_length = rop_shutter_range[1] - rop_shutter_range[0]
        
        if rop_shutter_length == 0:
            cam_shutter_range = rop_shutter_range
            log.warning('ROP shutter length is zero, cannot remap camera shutter')
        else:
            cam_shutter_range = [None, None]
            cam_shutter_range[0] = (self.shutter_range[0] - rop_shutter_range[0]) / rop_shutter_length
            cam_shutter_range[1] = (self.shutter_range[1] - rop_shutter_range[0]) / rop_shutter_length
        
        log.dtrace('cam_shutter  = ' + repr(cam_shutter_range))
        log.dtrace('info_shutter = ' + repr(self.shutter_range))
        
        HaNodeSetFlt(camera, 'shutter_start', cam_shutter_range[0])
        HaNodeSetFlt(camera, 'shutter_end', cam_shutter_range[1])
        
        if rop.iprop('ar_extra_userdata'):
            AiNodeDeclare(camera, 'info_shutter_start', 'constant FLOAT')
            AiNodeDeclare(camera, 'info_shutter_end', 'constant FLOAT')
            AiNodeSetFlt(camera, 'info_shutter_start', self.shutter_range[0])
            AiNodeSetFlt(camera, 'info_shutter_end', self.shutter_range[1])
            
        # screen window
        win = self.fprop('win', defvalue=[0, 0])
        win = [win[i] * winsize_scale for i in xrange(2)]
        winsize = self.fprop('winsize', defvalue=[1, 1])
        winsize = [winsize[i] * winsize_scale for i in xrange(2)]
        
        if (win, winsize) != ([0, 0], [1, 1]):
            screen_window_min_x = 2 * win[0] - winsize[0]
            screen_window_max_x = 2 * win[0] + winsize[0]
            screen_window_min_y = 2 * win[1] - winsize[1]
            screen_window_max_y = 2 * win[1] + winsize[1]
            HaNodeSetPnt2(camera, 'screen_window_min', screen_window_min_x, screen_window_min_y)
            HaNodeSetPnt2(camera, 'screen_window_max', screen_window_max_x, screen_window_max_y)
        
        # are we the render camera?
        if self.path == self.session.sprop('camera'):
            options = AiUniverseGetOptions()
            HaNodeSetPtr(options, "camera", camera)
            res = self.iprop('res', defvalue=[640, 480])
            
            if not (res[0] > 0 and res[1] > 0):
                log.error('Bad image resolution: %i x %i' % res)
                AiNodeDestroy(camera)
                return None
            
            aspect = self.fprop('aspect', defvalue=[1])
            
            if self.session.iprop('override_camerares'):
                res_fraction = self.session.sprop('res_fraction')
                if res_fraction == 'specific':
                    res = self.session.iprop('res_override')
                    aspect = self.session.fprop('aspect_override')
                else:
                    res = [int(round(res[i] * float(res_fraction))) for i in xrange(2)]
            
            if aspect <= 0:
                log.error('Bad camera pixel aspect ratio: %f' % aspect)
                AiNodeDestroy(camera)
                return None
                
            HaNodeSetFlt(options, 'aspect_ratio', 1 / aspect)
            HaNodeSetInt(options, 'xres', res[0])
            HaNodeSetInt(options, 'yres', res[1])
            
            # crop
            cropl = self.fprop('cropl', defvalue=[0])
            cropr = self.fprop('cropr', defvalue=[1])
            cropb = self.fprop('cropb', defvalue=[0])
            cropt = self.fprop('cropt', defvalue=[1])
            if (cropl, cropr, cropb, cropt) != (0, 1, 0, 1):
                region_min_x = int(round(cropl * res[0]))
                region_max_x = int(round(cropr * res[0])) - 1
                region_min_y = int(round((1 - cropt) * res[1]))
                region_max_y = int(round((1 - cropb) * res[1])) - 1
                HaNodeSetInt(options, 'region_min_x', region_min_x)
                HaNodeSetInt(options, 'region_max_x', region_max_x)
                HaNodeSetInt(options, 'region_min_y', region_min_y)
                HaNodeSetInt(options, 'region_max_y', region_max_y)
                
            # overscan
            elif self.session.iprop('ar_overscan_enable') and not self.session.iprop('ar_overridden'):
                overscan = self.session.iprop('ar_overscan', defvalue=[0, 0, 0, 0])
                region_min_x = -overscan[2]
                region_max_x = res[0] + overscan[3] - 1
                region_min_y = -overscan[0]
                region_max_y = res[1] + overscan[1] - 1
                HaNodeSetInt(options, 'region_min_x', region_min_x)
                HaNodeSetInt(options, 'region_max_x', region_max_x)
                HaNodeSetInt(options, 'region_min_y', region_min_y)
                HaNodeSetInt(options, 'region_max_y', region_max_y)
        
        # shutter curve
        if self.sprop('ar_shutter_type') == 'curve':
            parm_instances = self.hou_node.parm('ar_shutter_curve').multiParmInstances()
            npts = len(parm_instances) / 3
            shutter_points = AiArrayAllocate(npts, 1, AI_TYPE_POINT2);
            
            for i in xrange(0, npts):
                curve_pt = AtPoint2()
                curve_pt.x = parm_instances[i * 3].evalAsFloat()
                curve_pt.y = parm_instances[i * 3 + 1].evalAsFloat()
                AiArraySetPnt2(shutter_points, i, curve_pt)
            
            HaNodeSetArray(camera, 'shutter_curve', shutter_points)
            
        # filtermap
        filtermap_shader = HaMaterial(self.session, shader_path).generateCameraFiltermap()
        if filtermap_shader:
            AiNodeSetPtr(camera, 'filtermap', filtermap_shader)

        # user options
        AiNodeSetAttributes(camera, self.parm('ar_user_options', override_suffix='_enable'))

        return camera
