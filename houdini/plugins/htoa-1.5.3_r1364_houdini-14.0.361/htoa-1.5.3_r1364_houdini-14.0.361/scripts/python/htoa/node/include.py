# $Id: include.py 1012 2014-10-10 15:14:05Z kik $

import htoa.log as log
from htoa.node.shape import HaShape

def includeHook(arg_dict):
    '''The post .ass write hook for the includes.
    This will append the include directives manually to the .ass file after
    generation because there is no API to do that.
    '''
    try:
        f = open(arg_dict['filename'], 'a') # append
        for inc in arg_dict['includes']:
            f.write('include "%s"\n\n' % inc)
    except:
        pass
    finally:
        f.close()

class HaInclude(HaShape):
    '''Arnold include '''
                
    def generate(self, index=None):
        '''Generate Arnold nodes.
        @param index: ignored
        '''
        log.debug('Generating include: %s' % self.obj.path)

        hobj = self.obj.hou_node
        includes = []
        
        for i in xrange(1, hobj.parm('ar_includes').evalAsInt() + 1):
            include = hobj.parm('ar_filename%i' % i).evalAsString()
            if include:
                log.debug(' including "%s"' % include)
                includes.append(include)
        
        if includes:
            self.obj.session.post_asswrite_hooks.append((includeHook, {'includes': includes}))
        
        return {}
