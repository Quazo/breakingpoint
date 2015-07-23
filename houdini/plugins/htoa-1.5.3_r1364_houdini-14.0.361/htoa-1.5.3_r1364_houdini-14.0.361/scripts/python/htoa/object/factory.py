# $Id: factory.py 1361 2015-06-16 11:48:49Z kik $

from htoa.node.include import HaInclude
from htoa.node.override import HaOverride
from htoa.node.volume import HaVolumeContainer
from htoa.object.camera import HaCamera
from htoa.object.geometry import HaGeometry
from htoa.object.light import HaLight
from htoa.object.object import HaObject, sohoObjectType
from htoa.object.rop import HaRop
import htoa.log as log

_generators = {'light'                  : HaLight,
               'camera'                 : HaCamera,
               'geometry'               : HaGeometry,
               'rop'                    : HaRop,
               'arnold_volume_container': lambda session, soho_obj: HaVolumeContainer(HaObject(session, soho_obj)),
               'arnold_vdb'             : lambda session, soho_obj: HaVolumeContainer(HaObject(session, soho_obj)),
               'arnold_override'        : lambda session, soho_obj: HaOverride(HaObject(session, soho_obj)),
               'arnold_include'         : lambda session, soho_obj: HaInclude(HaObject(session, soho_obj))}

def generate(session, soho_object, obj_type=None, index=None):
    '''Generate Arnold nodes from a soho.SohoOject.
    @param session: the current HaSession
    @param soho_object: the SohoObject to generate
    @param obj_type: a target object type to translate to, if set to None the
    type will be automatically deduced.
    @param index: optional instance index
    @return: a dict of material paths keyed by generated Arnold nodes.
    '''
    
    if not obj_type:
        obj_type = sohoObjectType(soho_object)
        
        if not obj_type:
            log.warning('invalid OBJ type, skipping %s' % soho_object.getDefaultedString('object:name', 0, [None])[0])
            return {}
        
    if obj_type in _generators:
        return _generators[obj_type](session, soho_object).generate(index)
    else:
        # for full point instances, generate the first occurence only
        obj_id = soho_object.getDefaultedInt('object:id', 0, [None])[0]
        instance_id = soho_object.getDefaultedInt('object:instanceid', 0, [None])[0]
        if obj_id != instance_id: # full point instances
            if obj_id in session.instances:
                return
            else:
                session.instances.update([obj_id])
        
        # generate geometry by default
        return HaGeometry(session, soho_object).generate(index)
    