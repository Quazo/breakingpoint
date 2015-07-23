'''
@file
@since: 07/08/2011
@author: kik
'''
from htoa.node.node import HaNode    

class HaShape(HaNode):
    '''Arnold primitive abstract class'''
    
    def __init__(self, ha_object, mbtype=None):
        '''Constructor'''

        ## Parent HaObject
        self.obj = ha_object
        
        if mbtype:
            ## motion blur type (none|transform|deform|velocity)
            self.mbtype = mbtype
        else:
            self.mbtype = self.obj.mbtype
