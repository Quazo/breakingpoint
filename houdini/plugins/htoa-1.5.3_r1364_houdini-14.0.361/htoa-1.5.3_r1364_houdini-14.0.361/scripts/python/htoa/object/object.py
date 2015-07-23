# $Id: object.py 1361 2015-06-16 11:48:49Z kik $

import hashlib

import soho
import sohog
import sohoglue
import hou

from arnold import *
import htoa.log as log

## The identity matrix
HA_MATRIX_IDENTITY = [1.0, 0.0, 0.0, 0.0,
                      0.0, 1.0, 0.0, 0.0,
                      0.0, 0.0, 1.0, 0.0,
                      0.0, 0.0, 0.0, 1.0]

def getShutterRange(hou_node):
    '''Return the object shutter range in frames.
    
    @return: a shutter range list in frames or None if any of ar_mb_shutter,
    ar_mb_shutter_range or ar_mb_shutter_length is missing on the object.
    
    '''
    try:
        shutter_position = hou_node.parm('ar_mb_shutter').evalAsString()
    except:
        return None
    
    shutter_range = [None, None]

    if shutter_position == 'custom':
        try:
            shutter_range = hou_node.parmTuple('ar_mb_shutter_range').eval()
        except:
            return None
        
        shutter_length = shutter_range[1] - shutter_range[0]
    else:
        try:
            shutter_length = hou_node.parm('ar_mb_shutter_length').evalAsFloat()
        except:
            return None
    
        if shutter_position == 'start':
            shutter_range[0] = 0.0
            shutter_range[1] = shutter_length
            
        elif shutter_position == 'center':
            shutter_range[0] = -0.5 * shutter_length
            shutter_range[1] =  0.5 * shutter_length
            
        elif shutter_position == 'end':
            shutter_range[0] = -shutter_length
            shutter_range[1] = 0.0
        else:
            return None
    
    return shutter_range

def sohoObjectType(soho_object):
    '''Get a SohoObject type from the OBJ node name.
    If the object has an optional "ar_translate_as" property, it will be
    returned instead.
    '''
    # try ar_translate_as property
    obj_type = soho_object.getDefaultedString('ar_translate_as', 0, [None])[0]
    if obj_type:
        return obj_type
        
    # use the OBJ type
    hou_node = hou.nodeBySessionId(soho_object.getDefaultedInt('object:id', 0, [None])[0])
    if hou_node:
        return hou_node.type().nameComponents()[2]
    else:
        log.warning('cannot get node type for %s' % soho_object.getDefaultedString('object:name', 0, [None])[0])
        return None

def objectType(obj):
    '''Get an OBJ type.
    If the object has an optional "ar_translate_as" property, it will be
    returned instead.
    '''
    parm = obj.parm('ar_translate_as')
    
    if parm is not None:
        return parm.evalAsString()
    else:
        return obj.type().nameComponents()[2]

class HaObject(object):
    '''Abstract Houdini object translator.
    This is the base class for everything living in /obj
    
    '''
    def __init__(self, session, soho_obj, init_motion_blur=True):
        self._init(session, soho_obj, init_motion_blur)
    
    def _init(self, session, soho_obj, init_motion_blur=True):
        '''Initialization be called in subclass constructors'''
        
        ## Parent HaSession
        self.session = session

        ## Input SohoObject
        self.soho_obj = soho_obj
        
        ## SOP path
        self.sop_path = self.sprop('object:soppath')

        ## Object ID
        self.object_id = self.iprop('object:id')
        
        ## Instance ID
        self.instance_id = self.iprop('object:instanceid')
        
        ## Instance index
        self.instance_index = -1
        
        ## Houdini hou.Node
        self.hou_node = hou.nodeBySessionId(self.object_id)
        if not self.hou_node:
            self.hou_node = hou.node(self.sprop('object:name'))
        
        ## Object path
        self.path = self.hou_node.path() if self.hou_node else None
        
        ## Shutter range in frames, relative to 0
        self.shutter_range = [0.0, 0.0]
        
        # Motion blur settings
        if init_motion_blur:
            self._initMotionBlur()

    def _initMotionBlur(self):
        '''
        Initialize motion blur settings.
        @return: self.mbtype, self.xform_times, self.dform_times,
                 self.shutter_start_frame, self.shutter_end_frame
        '''
        rop = self.session.rop
        now = self.session.now

        # mbtype
        if not rop.iprop('ar_mb_xform_enable') and not rop.iprop('ar_mb_dform_enable'):
            mbtype = "none"
        elif rop.iprop('ar_mb_dform_enable'):
            if self.iprop('ar_mb_velocity_enable', defvalue=[self.iprop('geo_velocityblur', defvalue=[False])]):
                if self.iprop('ar_mb_acceleration_enable', defvalue=[False]):
                    mbtype = 'acceleration'
                else:
                    mbtype = 'velocity'
            else:
                mbtype = 'deform'
        else:
            mbtype = 'transform'

        ## Motion blur type.
        # Values: {'none'|'transform'|'deform'|'velocity'|'acceleration'}
        self.mbtype = mbtype
        log.dtrace('init motion blur for "%s" => mbtype = %s' % (self.path, mbtype))

        # early out for none
        if mbtype == "none":
            self.xform_times = self.dform_times = [now]
            log.dtrace('xform_times = ' + repr(self.xform_times))
            log.dtrace('dform_times = ' + repr(self.dform_times))
            return

        # xform steps
        if self.iprop('ar_mb_xform_keys_override', defvalue=[False]):
            xform_keys = self.iprop('ar_mb_xform_keys')
        elif rop.iprop('ar_mb_xform_enable'):
            xform_keys = rop.iprop('ar_mb_xform_keys')
        else:
            xform_keys = 1

        # dform steps
        if mbtype in ['deform', 'acceleration']:
            if self.iprop('ar_mb_dform_keys_override', defvalue=[False]):
                dform_keys = self.iprop('ar_mb_dform_keys')
            elif rop.iprop('ar_mb_dform_enable'):
                dform_keys = rop.iprop('ar_mb_dform_keys')
            else:
                dform_keys = 1
                
        elif mbtype == 'velocity':
            dform_keys = 2 # velocity is always 2-step linear
        else: # 'transform' 
            dform_keys = 1

        # try to find the ar_mb_shutter property property on the object, then
        # on the ROP, taking into account that there might be no Arnold
        # properties set on the object and they might not be enabled
        try:
            shutter_position = self.hou_node.parm('ar_mb_shutter').evalAsString()
            shutter_node = self.hou_node
        except:
            shutter_position = 'rop'
            shutter_node =  rop.hou_node
            
        if shutter_position == 'camera':
            shutter_node = hou.node(self.session.sprop('camera'))
            try:
                shutter_position = shutter_node.parm('ar_mb_shutter').evalAsString()
            except:
                shutter_position = 'rop'
            
        if shutter_position == 'rop':
            shutter_node = rop.hou_node
            shutter_position = shutter_node.parm('ar_mb_shutter').evalAsString()

        self.shutter_range = getShutterRange(shutter_node)
        shutter_duration = (self.shutter_range[1] - self.shutter_range[0]) * self.session.inv_fps
        start_time = now + self.shutter_range[0] * self.session.inv_fps
                    
        # if the number of keys is less than 2, we assume we have a single key
        # that we sample at the current frame time and not at shutter open
        if xform_keys > 1:
            self.xform_step_duration = shutter_duration / float(xform_keys - 1)
            xform_start_time = start_time
        else:
            self.xform_step_duration = 0
            xform_start_time = now
            xform_keys = 1
            
        if dform_keys > 1:
            self.dform_step_duration = shutter_duration / float(dform_keys - 1)
            dform_start_time = start_time
        else:
            self.dform_step_duration = 0
            dform_start_time = now
            dform_keys = 1
            
        ## Tranformation blur time samples
        self.xform_times = [xform_start_time + (i * self.xform_step_duration) for i in xrange(xform_keys)]

        ## Deformation blur time samples
        self.dform_times = [dform_start_time + (i * self.dform_step_duration) for i in xrange(dform_keys)]

        log.dtrace('xform_times = ' + repr(self.xform_times))
        log.dtrace('dform_times = ' + repr(self.dform_times))
        
        # DEBUG
        log.dtrace('xform_frames = ' + repr([t * self.session.fps + 1.0 for t in self.xform_times]))
        log.dtrace('dform_frames = ' + repr([t * self.session.fps + 1.0 for t in self.dform_times]))
        
    def getArnoldMatrix(self, matrix=None):
        '''Get Arnold transform matrix
        @param matrix: an optional list of hou.Matrix4 for instances transform
        time samples
        @return: an Arnold AtMatrix array
        '''
        xf_samples_count = len(self.xform_times)
        xf_samples = []
        is_const_xf = True
        prev_xf = None
        
        for i in xrange(len(self.xform_times)):
            mtx_xf = self.hou_node.worldTransformAtTime(self.xform_times[i])

            # optional transform
            if matrix:
                mtx_xf = matrix[i] * mtx_xf
            
            # check that the transform is not constant
            if prev_xf and prev_xf != mtx_xf:
                is_const_xf = False
                
            prev_xf = mtx_xf

            xf_samples.append(mtx_xf.asTuple())
            
        # all transform samples are equal, do not motion blur
        if is_const_xf:
            xf_samples_count = 1

        xform_array = AiArrayAllocate(1, xf_samples_count, AI_TYPE_MATRIX)
        for i in range(xf_samples_count):
            AiArraySetMtx(xform_array, i,
                          AtMatrix(xf_samples[i][0], xf_samples[i][1],
                                   xf_samples[i][2], xf_samples[i][3], 
                                   xf_samples[i][4], xf_samples[i][5],
                                   xf_samples[i][6], xf_samples[i][7], 
                                   xf_samples[i][8], xf_samples[i][9],
                                   xf_samples[i][10], xf_samples[i][11], 
                                   xf_samples[i][12], xf_samples[i][13],
                                   xf_samples[i][14], xf_samples[i][15]))
        return xform_array
    
    def getMatrixValueDict(self):
        '''Get Arnold transform matrix as a value dictionary suitable for deltas'''
        xf_samples_count = len(self.xform_times)
        xf_samples = []
        is_const_xf = True
        prev_xf = None
        
        for time in self.xform_times:
            xf = self.soho_obj.getDefaultedFloat('space:world', time, HA_MATRIX_IDENTITY)
            
            if prev_xf and prev_xf != xf:
                is_const_xf = False
                
            prev_xf = xf
            xf_samples.append(hou.Matrix4(xf).asTuple())

        # all transform samples are equal, do not motion blur
        if is_const_xf:
            xf_samples_count = 1

        value = {}
        value['nkeys'] = xf_samples_count
        value['nelts'] = 1
        value['type'] = AI_TYPE_MATRIX
        value['data'] = [xf_samples[k][i] for k in xrange(xf_samples_count) for i in xrange(16)]
        return value
    
    def materialPath(self):
        '''Return the canonical material path'''
        return hou.chsop(self.path + '/shop_materialpath')
    
    def isPhantom(self):
        self.iprop('vm_phantom', [False])
        
    def isForcedPhantom(self):
        return self.path in self.session.phantoms
    
    def isMatte(self):
        return self.iprop('ar_matte', [self.iprop('vm_matte', [False])])
        
    def isForcedMatte(self):
        return self.path in self.session.matte_objects
    
    def parm(self, parm_name, now=None, defvalue=None, override_suffix='_override'):
        '''Convenience function to evaluate a parameter through the hou module.
        
        @note: You should use fprop(), iprop(), sprop() as they are faster
        and support <a href="http://www.sidefx.com/docs/houdini11.1/props/#Inheritance">
        SOHO property inheritance</a> unless you specifically want to avoid that.
        @param now: Property evaluation time; the session's default time
        (HaSession.now) will be used if left to None.
        @param defvalue: A default value to be returned if the queried property
        does not exist on the object.
        @param override_suffix: The suffix to append to the token name to check 
        if the parameter has a corresponding override boolean parameter. If such
        a parameter is found and is False, None is returned.
        @see: fprop(), iprop(), sprop()
        
        '''
        t = now if now else self.session.now
        
        override_parm = self.hou_node.parm(parm_name + override_suffix)
        if override_parm and not override_parm.evalAtTime(t):
            return defvalue
        
        try:
            return self.hou_node.parm(parm_name).evalAtTime(t)
        except:
            return defvalue

    def fprop(self, token, now=None, defvalue=[], override_suffix='_override'):
        '''Convenience function to evaluate a single float property through SOHO.
        
        Returns a float or a list of floats depending on the property being
        evaluated. Unlike soho.SohoGeometry.getDefaultedFloat(), a single float
        value (and not a single element list) unless the return value is a list
        containing at least two elements. The returned value benefits from 
        <a href="http://www.sidefx.com/docs/houdini11.1/props/#Inheritance">
        SOHO property inheritance</a>.
        
        @param token: SOHO token or object property name. 
        @param now: Property evaluation time; the session's default time
        (HaSession.now) will be used if left to None.
        @param defvalue: A default value to be returned if the queried property
        does not exist on the object. The default default [] will return None
        if the property does not exist.
        @param override_suffix: The suffix to append to the token name to check 
        if the parameter has a corresponding override boolean parameter. If such
        a parameter is found and is False, None is returned.
        @return: Evaluated parameter as a float or list of floats or None
        @see: iprop(), sprop(), fsamples(), soho.SohoGeometry.getDefaultedFloat(),
        <a href="http://www.sidefx.com/docs/hdk11.1/namespace_h_d_k___s_o_h_o___a_p_i.html#d20dbd9df7fab2cd565affc43c719518">
        sohoglue.evaluate()</a>.
        
        '''
        t = now if now else self.session.now
        is_overridden = self.soho_obj.getDefaultedInt(token + override_suffix, t, [None])[0]
        
        if is_overridden != None and is_overridden == False:
            res = defvalue
        else:    
            res = self.soho_obj.getDefaultedFloat(token, t, defvalue)
        
        res_size = len(res)
        if   res_size == 0: return None
        elif res_size == 1: return res[0]
        else:               return res
                  
    def iprop(self, token, now=None, defvalue=[], override_suffix='_override'):
        '''Convenience function to evaluate a single integer property through SOHO.

        This method is the integer counterpart of fprop().
        @see: fprop(), sprop(), isamples(), soho.SohoGeometry.getDefaultedInt()
        '''
        t = now if now else self.session.now
        is_overridden = self.soho_obj.getDefaultedInt(token + override_suffix, t, [None])[0]
        
        if is_overridden != None and is_overridden == False:
            res = defvalue
        else:    
            res = self.soho_obj.getDefaultedInt(token, t, defvalue)
        
        res_size = len(res)
        if   res_size == 0: return None
        elif res_size == 1: return res[0]
        else:               return res
        
    def sprop(self, token, now=None, defvalue=[], override_suffix='_override'):
        '''Convenience function to evaluate a single float property through SOHO.
        
        This method is the string counterpart of fprop().
        @see: fprop(), iprop(), soho.SohoGeometry.getDefaultedString()

        '''
        t = now if now else self.session.now
        is_overridden = self.soho_obj.getDefaultedInt(token + override_suffix, t, [None])[0]
        
        if is_overridden != None and is_overridden == False:
            res = defvalue
        else:
            res = self.soho_obj.getDefaultedString(token, t, defvalue)
        
        res_size = len(res)
        if   res_size == 0: return None
        elif res_size == 1: return res[0]
        else:               return res

    def isOverridable(self, parm_name, suffix='_override'):
        '''Check if a parameter is overridable'''
        override_parm = parm_name + suffix
        return self.iprop(override_parm) != None
    
    def isOverridden(self, parm_name, suffix='_override'):
        '''Check if a parameter is overridden'''
        override_parm = parm_name + suffix
        return self.iprop(override_parm, defvalue=[False])

    def fsamples(self, token, sample_times=[], defvalue=[]):
        '''Convenience function to evaluate float samples of a property through SOHO.
        
        Returns a list float values for a property evaluated at a series of
        time samples. Like fprop(), the returned values benefit from 
        <a href="http://www.sidefx.com/docs/houdini11.1/props/#Inheritance">
        SOHO property inheritance</a>.
        
        If the parameter does not depend on time, as per
        <a href="http://www.sidefx.com/docs/houdini11.1/hom/hou/Parm#isTimeDependent">
        hou.Parm.isTimeDependent()</a>, then the returned list contains only a
        single value, speeding up motion blur calculations when passed to
        Arnold as well as lowering memory requirements.
        
        @param token: SOHO token or object property name. 
        @param sample_times: A list of evaluation times; the object's default
        sampling times (self.xform_times) will be used if left to None.
        @param defvalue: A default value to be returned if the queried property
        does not exist on the object. The default default [] will return None
        if the property does not exist.
        @see: isamples(), ssamples(), fprop(), soho.SohoGeometry.getDefaultedFloat(),
        <a href="http://www.sidefx.com/docs/hdk11.1/namespace_h_d_k___s_o_h_o___a_p_i.html#d20dbd9df7fab2cd565affc43c719518">
        sohoglue.evaluate()</a>.
        
        '''
        if not sample_times:
            sample_times = self.xform_times
        
        parm = self.hou_node.parm(token)
        if not parm:
            return defvalue

        # sample once if parameter is constant
        elif parm.isTimeDependent():
            return [self.fprop(token, None, defvalue)]
        
        res_list = []
        for t in sample_times:
            res = self.soho_obj.getDefaultedFloat(token, t, defvalue)
            res_size = len(res)
            if res_size == 0:
                return None
            elif res_size == 1:
                res_list.append(res[0])
            else:
                res_list.append(res)
        
        return res_list
    
    def isamples(self, token, sample_times=[], defvalue=[]):
        '''Convenience function to evaluate float samples of a property through SOHO.
        
        This method is the integer counterpart of fsamples().
        @note: Is this method really useful?
        @see: fsamples(), ssamples(), iprop(), soho.SohoGeometry.getDefaultedInt()

        '''
        if not sample_times:
            sample_times = self.xform_times
            
        # sample once if parameter is constant
        if not self.hou_node.parm(token).isTimeDependent():
            return [self.iprop(token, None, defvalue)]

        res_list = []
        for t in sample_times:
            res = self.soho_obj.getDefaultedInt(token, t, defvalue)
            res_size = len(res)
            if res_size == 0:
                return None
            elif res_size == 1:
                res_list.append(res[0])
            else:
                res_list.append(res)
        
        return res_list
    
    def ssamples(self, token, sample_times=[], defvalue=[]):
        '''Convenience function to evaluate string samples of a property through SOHO.
        
        This method is the integer counterpart of fsamples().
        @note: Is this method really useful?
        @see: fsamples(), isamples(), sprop(), soho.SohoGeometry.getDefaultedInt()

        '''
        if not sample_times:
            sample_times = self.xform_times
            
        # sample once if parameter is constant
        if not self.hou_node.parm(token).isTimeDependent():
            return [self.sprop(token, None, defvalue)]

        res_list = []
        for t in sample_times:
            res = self.soho_obj.getDefaultedString(token, t, defvalue)
            res_size = len(res)
            if res_size == 0:
                return None
            elif res_size == 1:
                res_list.append(res[0])
            else:
                res_list.append(res)
        
        return res_list

def pathToId(path):
    '''Returns a reasonably unique unsigned int ID from a path string in the
    range [1, 2^24 - 1] (#578)
     '''
    path_id = int(hashlib.md5(path).hexdigest()[:6], 16)
    return path_id if path_id else 1
