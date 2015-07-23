# $Id: pythonrc.py 1335 2015-06-03 13:55:17Z kik $

import os
import htoa.searchpath

# cache license information
import htoa.license

# set the HTOA environment variable pointing to the HtoA installation directory
if os.environ.has_key('HTOA'):
    print '[htoa] HTOA environment variable already set to %s' % os.environ['HTOA']
else:
    os.environ['HTOA'] = htoa.folder

# Arnold plugins and procedurals paths
os.environ['HTOA_PLUGIN_PATH'] = htoa.searchpath.plugin
os.environ['HTOA_PROCEDURAL_PATH'] = htoa.searchpath.procedural
