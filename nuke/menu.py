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

sys.path.append(os.path.abspath(".."))

import settings as s

print ("\nWelcome " + os.getenv('username'))
print ("\nBreaking Point: MENU")


PATH_ICON 		= os.path.join(s.PATH["img"], 'icons').replace('\\', '/')
PATH_MAIN_ICON	= os.path.join(PATH_ICON , 'bpN.png').replace('\\', '/')

PATH_WRITE_ICON	= os.path.join(PATH_ICON , 'menu', 'changeBtn24.ico').replace('\\', '/')
PATH_HELP_ICON	= os.path.join(PATH_ICON , 'menu', 'helpBtn24.ico').replace('\\', '/')

PATH_RT_ICON	= os.path.join(PATH_ICON , 'menu', 'rt_timm.ico').replace('\\', '/')
PATH_RT2_ICON	= os.path.join(PATH_ICON , 'menu', 'rt_timm.ico').replace('\\', '/')

PATH_GIZMO		= os.path.join(s.PATH["nuke"], 'gizmos').replace('\\', '/')  #JUST FOR SOFTWARE NOT _SANDBOX

PATH_BPWRITE	= os.path.join(PATH_GIZMO, 'bpWrite').replace('\\', '/')


menuNode = nuke.menu('Nodes').addMenu("BREAKINGPOINT", icon = PATH_MAIN_ICON)


# #*******************
# # TOOLBAR
# #*******************
menuNode.addCommand('bpWrite', lambda: nuke.createNode(PATH_BPWRITE), 'alt+w', PATH_WRITE_ICON)

menuNode.addSeparator()

menuNode.addCommand('RenderThreads by Timm', lambda: run_renderthreads(), 'alt+t', PATH_RT_ICON)
menuNode.addCommand('RenderThreads by Vincent', lambda: run_renderthreadsV(), 'alt+v', PATH_RT2_ICON)

menuNode.addSeparator()

menuNode.addCommand('Help', lambda: webbrowser.open("https://www.filmakademie.de/wiki/display/AISPD/BREAKINGPOINT+-+Pipeline"), 'alt+h', PATH_HELP_ICON)

m = menuNode.findItem('bpWrite')
m.setEnabled( False )
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



