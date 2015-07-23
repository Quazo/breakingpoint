'''
@file
@since: 2011-11-10
@author: Frederic Servant <frederic.servant@gmail.com>
@namespace: htoa.universe

Arnold universe class.

'''
from arnold.ai_universe import AiUniverseIsActive
from arnold.ai_render import AiBegin, AiEnd

class HaUniverse(object):
    '''Arnold universe.
    
    As of Arnold 3.3 (and 3.4), only a single universe (Arnold context) can
    exist at a time. HaUniverse is thus implemented as the singleton design
    pattern.
    
    The single HaUniverse instance has an owner, which is represented as a
    UUID. HaUniverse is meant to be shared among several Arnold ROPs, and each
    of these ROPs has uuid hidden parameter containing an UUID automatically
    generated upon creation. Nothing prevents any other object to claim
    ownership of the HaUniverse by passing a UUID.
    
    The universe also has a dirty flag, to indicate whether the universe's
    contents should be regenerated from scratch in IPR situations. If it is
    clean, it is considered safe to just update the Arnold nodes it contains
    or add new ones before (re-)rendering.
    
    '''
    ## Singleton instance
    _instance = None
    
    ## Universe owner UUID
    _owner_uuid = None
    
    ## Dirty flag
    _dirty = True
    
    def __new__(cls, *args, **kwargs):
        '''Create a new instance.'''
        if not cls._instance:
            cls._instance = super(HaUniverse, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        '''Initialize a new instance.'''
        pass

    def activate(self):
        '''Create an Arnold universe if none is already active.'''
        if not AiUniverseIsActive():
            self._dirty = True
            AiBegin()

    def take(self, taker_uuid):
        '''Take ownership of the current universe.'''
        self._owner_uuid = taker_uuid

    def owner(self):
        '''Return the universe owner's UUID.'''
        return self._owner_uuid

    def isMine(self, my_uuid):
        '''Test if the universe is owned by UUID.'''
        return self._owner_uuid == my_uuid

    def destroy(self):
        '''Destroy current universe if one was active.'''
        if AiUniverseIsActive():
            AiEnd()
            self._dirty = True
            
    def reset(self):
        '''Restarts a clean universe.'''
        self.destroy()
        AiBegin()
        
    def isActive(self):
        '''Test if a univserse is active.'''
        return AiUniverseIsActive()
    
    def release(self):
        '''Make the universe owned by nobody.'''
        self._owner_uuid = None
    
    def isDirty(self):
        '''Test if the universe is dirty.'''
        return self._dirty
    
    def setDirty(self, flag):
        '''Set the universe dirty flag.'''
        self._dirty = flag
        
