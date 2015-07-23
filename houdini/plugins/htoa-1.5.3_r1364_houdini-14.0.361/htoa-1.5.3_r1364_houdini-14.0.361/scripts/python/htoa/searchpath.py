# $Id: searchpath.py 1111 2014-11-27 17:06:26Z kik $

import os
import sys
import hou
import htoa

## Plugins search path
plugin = os.pathsep.join(hou.findDirectories(os.path.join('arnold', 'plugins')))
if os.environ.has_key('ARNOLD_PLUGIN_PATH'):
    plugin += os.pathsep + os.environ['ARNOLD_PLUGIN_PATH']

## Procedurals search path
procedural = os.pathsep.join(hou.findDirectories(os.path.join('arnold', 'procedurals')))
if os.environ.has_key('ARNOLD_PROCEDURAL_PATH'):
    procedural += os.pathsep + os.environ['ARNOLD_PROCEDURAL_PATH']

## Drivers search path
driver = os.pathsep.join(hou.findDirectories(os.path.join('arnold', 'drivers')))

## ROP initialization scripts
try:
    rop_init_scripts = hou.findFiles(os.path.join('scripts', 'out', 'arnold.py'))
except:
    rop_init_scripts = []

## Hick executable/script path
hick = '%s/scripts/bin/hick%s' % (htoa.folder, '.exe' if sys.platform == 'win32' else '')
