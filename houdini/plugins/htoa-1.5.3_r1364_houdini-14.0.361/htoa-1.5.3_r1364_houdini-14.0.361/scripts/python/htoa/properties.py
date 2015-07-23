# $Id: properties.py 1253 2015-03-11 17:12:44Z kik $

from htoa.blacklist import attribute_blacklist
import hou

# nodes types that should accept properties
GEO_TYPE_NAMES = ['geo']
INSTANCE_TYPE_NAMES = ['instance']
PROCEDURAL_TYPE_NAMES = ['arnold_procedural']
CAMERA_TYPE_NAMES = ['cam', 'stereocamrig']
OBJ_TYPE_NAMES = GEO_TYPE_NAMES + INSTANCE_TYPE_NAMES + PROCEDURAL_TYPE_NAMES + CAMERA_TYPE_NAMES

def translateAs(node):
    # the ar_translate_as property overrides anything
    parm = node.parm('ar_translate_as')
    if parm:
        return parm.evalAsString()
       
    node_type = node.type()
    
    # digital asset case
    hda = node_type.definition() 
    if hda:
        extra_info = hda.extraInfo().split()
        for token in extra_info:
            key, value = token.split('=')
            if key == 'subtype':
                return value
            
    # if all else fails, return the type name
    return node_type.nameComponents()[2]

def addArnoldProperties(nodeseq_or_node, force=False):
    '''Add Arnold properties to the selected OBJ nodes.
    
    @param nodeseq_or_node: a sequence of houd.Node or a single hou.Node
    @param force: do not check the node type and add geometry properties
    '''
    
    # we want a sequence
    try:
        iter(nodeseq_or_node)
        nodes = nodeseq_or_node
    except:
        nodes = [nodeseq_or_node]
    
    for node in nodes:
        # we want a hou.Node
        try:
            group = node.parmTemplateGroup()
        except:
            continue
        
        # does the Arnold folder already exist?
        if len(group.findIndicesForFolder('Arnold')):
            continue
        
        # only OBJ nodes have Arnold properties for now
        if node.type().category() != hou.objNodeTypeCategory():
            continue
        
        type_name = translateAs(node)
    
        if force or type_name in OBJ_TYPE_NAMES:
            # append Arnold tab
            folder = hou.FolderParmTemplate('arnold', 'Arnold')
            group.append(folder)
            node.setParmTemplateGroup(group)
            
            # add the override properties parameter (shop_propertiespath), this
            # will silently fail if the parameter already exist.
            hou.hscript('opproperty -f -F Arnold %s arnold* ar_override_parms' % node.path())
    
        # add the others parameters
        if force or type_name in GEO_TYPE_NAMES:
            hou.hscript('opproperty -f -F Arnold %s arnold* ar_object_parms' % node.path())
            hou.hscript('opparm -b on %s ar_subdiv_dicing_camera' % node.path())
            
            # link to native Mantra properties if they exist
            if node.parm('vm_matte'):
                node.parm('ar_matte').setExpression('ch("vm_matte")')
                        
            if node.parm('geo_velocityblur'):
                node.parm('ar_mb_velocity_enable').setExpression('ch("geo_velocityblur")')
            
            if node.parm('vm_pointscale'):
                node.parm('ar_point_scale').setExpression('ch("vm_pointscale")')

        elif type_name in INSTANCE_TYPE_NAMES:
            hou.hscript('opproperty -f -F Arnold %s arnold* ar_instance_parms' % node.path())
            
        elif type_name in PROCEDURAL_TYPE_NAMES:
            hou.hscript('opproperty -f -F Arnold %s arnold* ar_procedural_parms' % node.path())
            
        elif type_name in CAMERA_TYPE_NAMES:
            hou.hscript('opproperty -f -F Arnold %s arnold* ar_camera_parms' % node.path())

def removeArnoldProperties(nodeseq_or_node, force=False):
    '''Remove Arnold properties to the selected OBJ nodes.
    
    @param nodeseq_or_node: a sequence of houd.Node or a single hou.Node 
    @param force: do not check the node type and add geometry properties
    '''

    # we want a sequence
    try:
        iter(nodeseq_or_node)
        nodes = nodeseq_or_node
    except:
        nodes = [nodeseq_or_node]

    for node in nodes:
        # we want a hou.Node
        try:
            group = node.parmTemplateGroup()
        except:
            continue
        
        type_name = translateAs(node)

        if force or type_name in OBJ_TYPE_NAMES:
            indices = group.findIndicesForFolder('Arnold')
            if len(indices):
                group.remove(indices)
                node.setParmTemplateGroup(group)

def bypass(node, parm_name, flag):
    '''Set the bypass flag on a spare parameter'''
    hou.hscript('opparm -b %s %s %s' % ('on' if flag else 'off', node.path(), parm_name))

def override(kwargs):
    '''Override callback'''
    suffix = '_override'
    suffix_length = len(suffix)
    bypass(kwargs['node'], kwargs['parm_name'][:-suffix_length], not bool(kwargs['parm'].evalAsInt()))

def detailAttributeMenu():
    geometry = hou.pwd().renderNode().geometry()
    if not geometry:
        return []
    
    menu_items = ['*', '*\t (all)']
    
    for attr in geometry.globalAttribs():
        if not attr.name() in attribute_blacklist:
            menu_items += [attr.name(), '%s\t  %s[%i]' % (attr.name(), attr.dataType().name().lower(), attr.size())]
    
    return menu_items

def primitiveAttributeMenu():
    geometry = hou.pwd().renderNode().geometry()
    if not geometry:
        return []
    
    menu_items = ['*', '*\t (all)']
    
    for attr in geometry.primAttribs():
        if not attr.name() in attribute_blacklist:
            menu_items += [attr.name(), '%s\t  %s[%i]' % (attr.name(), attr.dataType().name().lower(), attr.size())]
    
    return menu_items

def pointAttributeMenu():
    geometry = hou.pwd().renderNode().geometry()
    if not geometry:
        return []
    
    menu_items = ['*', '*\t (all)']
    
    for attr in geometry.pointAttribs():
        if not attr.name() in attribute_blacklist:
            menu_items += [attr.name(), '%s\t  %s[%i]' % (attr.name(), attr.dataType().name().lower(), attr.size())]
    
    return menu_items

def vertexAttributeMenu():
    geometry = hou.pwd().renderNode().geometry()
    if not geometry:
        return []
    
    menu_items = ['*', '*\t (all)']
    
    for attr in geometry.vertexAttribs():
        if not attr.name() in attribute_blacklist:
            menu_items += [attr.name(), '%s\t  %s[%i]' % (attr.name(), attr.dataType().name().lower(), attr.size())]
    
    return menu_items
