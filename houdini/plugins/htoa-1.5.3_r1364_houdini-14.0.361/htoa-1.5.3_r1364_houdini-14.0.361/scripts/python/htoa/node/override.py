# $Id: override.py 1199 2015-02-12 20:03:15Z kik $

import htoa.log as log
from htoa.node.shape import HaShape

def overrideHook(arg_dict):
    '''The post .ass write hook for the override node.
    This will append the override node definition manually to the .ass file
    after generation because there is no API to write the override node.
    '''
    try:
        f = open(arg_dict['filename'], 'a') # append
        f.write('override\n{\n')
        for ov in arg_dict['overrides']:
            f.write(' %s\n' % ov)
        f.write('}\n\n')
    finally:
        f.close()

class HaOverride(HaShape):
    '''Arnold override '''
                
    def generate(self, index=None):
        '''Generate Arnold nodes.
        @param index: ignored
        '''
        log.debug('Generating override: %s' % self.obj.path)

        hobj = self.obj.hou_node
        
        for i in xrange(1, hobj.parm('ar_overrides').evalAsInt() + 1):
            node_name = hobj.parm('ar_node_name%i' % i).evalAsString()
            
            if node_name:
                arg_dict = {}
                overrides = []
                
                for j in xrange(1, hobj.parm('ar_parameters%i' % i).evalAsInt() + 1):
                    param_name = hobj.parm('ar_param_name%i_%i' % (i, j)).evalAsString()
                    if param_name:
                        param_type = hobj.parm('ar_param_type%i_%i' % (i, j)).evalAsString()
                        param_value_name = 'ar_param_value_%s_%i_%i' % (param_type, i, j)
                        param_value = ' '.join([str(x) for x in hobj.parmTuple(param_value_name).eval()]) 
                        overrides.append('%s %s %s' % (node_name, param_name, param_value))
                
                if overrides:
                    arg_dict['overrides'] = overrides
                    self.obj.session.post_asswrite_hooks.append((overrideHook, arg_dict))
                    
        return {}
