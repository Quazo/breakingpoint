# $Id: arnold.py 1358 2015-06-15 16:39:12Z kik $

import os

# debug mode, reload everything
try:
    if int(os.environ['HTOA_DEBUG']) > 0:
        import sys
        sys.dont_write_bytecode = True
        
        import htoa
        import htoa.session
        import htoa.universe  # don't reload, cf. singleton implementation
        import htoa.material
        import htoa.log
        import htoa.object
        import htoa.object.camera
        import htoa.object.factory
        import htoa.object.geometry
        import htoa.object.light
        import htoa.object.object
        import htoa.object.rop
        import htoa.node
        import htoa.node.node
        import htoa.node.shape
        import htoa.node.parms
        import htoa.node.override
        import htoa.node.include
        import htoa.utils
        import htoa.ipr
        import htoa.dialog
        import htoa.blacklist
        import htoa.license
    #    reload(htoa)  # reloading this disables IPR (htoa.sessions dict is reset)
        reload(htoa.session)
        reload(htoa.material)
        reload(htoa.log)
        reload(htoa.object)
        reload(htoa.object.camera)
        reload(htoa.object.factory)
        reload(htoa.object.geometry)
        reload(htoa.object.light)
        reload(htoa.object.object)
        reload(htoa.object.rop)
        reload(htoa.node)
        reload(htoa.node.node)
        reload(htoa.node.shape)
        reload(htoa.node.parms)
        reload(htoa.node.override)
        reload(htoa.node.include)
        reload(htoa.utils)
        reload(htoa.ipr)
        reload(htoa.dialog)
        reload(htoa.blacklist)
        reload(htoa.license)

except:
    pass

# profile data file
try:
    profile_data = os.environ['HTOA_PROFILE']
except:
    profile_data = None

if profile_data:
    import htoa.session
    import cProfile
    cProfile.run('htoa.session.HaSession.getSession().run()', profile_data)    
else:
    from htoa.session import HaSession
    HaSession.getSession().run()
