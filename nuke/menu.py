#*************************************************************
# function: 	Starup script for Nuke Menu
#			
# depencence: 	set "NUKE_PATH=%PLUGINS_PATH%;%NUKE_PATH%"
#
# author: 		Alexander Richter 
# email:		alexander.richter@filmakademie.de
#*************************************************************

import os
import sys
import nuke
import webbrowser


print ("Breaking Point: MENU")


PIPELINE_PATH 	= os.getcwd()

ICON_PATH 		= PIPELINE_PATH + '/img/icons'
MAIN_ICON_PATH 	= ICON_PATH 	+ '/bpN.png'

WRITE_ICON_PATH	= ICON_PATH 	+ '/menu/changeBtn24.ico'
HELP_ICON_PATH	= ICON_PATH 	+ '/menu/helpBtn24.ico'

RT_ICON_PATH	= ICON_PATH 	+ '/menu/rt_timm.ico'
RT2_ICON_PATH	= ICON_PATH 	+ '/menu/rt_timm.ico'

GIZMO_PATH		= PIPELINE_PATH + '/nuke/gizmos'


menuNode = nuke.menu('Nodes').addMenu("BREAKINGPOINT", icon = MAIN_ICON_PATH)


# #*******************
# # TOOLBAR
# #*******************
menuNode.addCommand('bpWrite', lambda: nuke.createNode(GIZMO_PATH + '/bpWrite'), 'alt+w', WRITE_ICON_PATH)

menuNode.addSeparator()

menuNode.addCommand('RenderThreads by Timm', lambda: run_renderthreads(), 'alt+t', RT_ICON_PATH)
menuNode.addCommand('RenderThreads by Vincent', lambda: run_renderthreadsV(), 'alt+v', RT2_ICON_PATH)

menuNode.addSeparator()

menuNode.addCommand('Help', lambda: webbrowser.open("https://www.filmakademie.de/wiki/display/AISPD/BREAKINGPOINT+-+Pipeline"), 'alt+h', HELP_ICON_PATH)


# m = menuNode.findItem('bpWrite')
# m.setEnabled( False )
# m = menuNode.findItem('RenderThreads by Vincent')
# m.setEnabled( False )



# #*******************
# # RENDERTHREADS
# #*******************
def run_renderthreads():

    from plugins.renderthreads import renderthreads
    reload(renderthreads)
    renderthreads.run()


def run_renderthreadsV():

    from plugins.vuRenderThreads.plugin_nuke import plugin_nuke
    plugin_nuke.showPopup()