#*************************************************************
# title: 		bpMenu
#
# content:		Adds a Menu with its functions to MAYA
#
# dependencies: userSeutup
#
# author: 		Alexander Richter 
# email:		alexander.richter@filmakademie.de
#*************************************************************

import os
import maya.cmds as cmds


print ("\nWelcome " + os.getenv('username'))
print("setup bpMenu")


bpMenu = cmds.menu('bpMenu', hm = 1, p = 'MayaWindow', l = 'bpMenu', to = 1, )

cmds.menuItem(p = bpMenu, l = 'Load',c = 'from scripts import bpLoad', en = 0)
cmds.menuItem(p = bpMenu, l = 'Save',c = 'from scripts import bpSave\nbpSave.main()')#, en = 0)

cmds.menuItem(d = True)

cmds.menuItem(p = bpMenu, l = 'Asset Manager',c = 'import bpAssetManager', en = 0)
#cmds.menuItem(p = bpMenu, l = 'Export Manager',c = 'import bpLoad', en = 0)

cmds.menuItem(d = True)


# toolMenu = cmds.menuItem(p = bpMenu, l = 'Utilities', to = True, sm = True, en = 0)

# cmds.menuItem(p = toolMenu,
#             l = 'Dock Output Window',
#             c = 'import arutils.ui.generalUI;arutils.ui.generalUI.dockableOutputWindow()')
# cmds.menuItem(p = toolMenu,
#             l = 'Search UI Elements',
#             c = 'import arutils.ui.generalUI;arutils.ui.generalUI.SearchUI().create()')
# cmds.menuItem(p = toolMenu,
#             l = 'FPS Drop Down',
#             c = 'import arutils.ui.generalUI;arutils.ui.generalUI.fpsDropDown()')
# cmds.menuItem(p = bpMenu,
#             d = True)


# cmds.menuItem(p = bpMenu,
#             l = 'Report',
#             c = '', en = 0)

cmds.menuItem(p = bpMenu,
            l = 'Help',
            c = 'import webbrowser\nwebbrowser.open("https://www.filmakademie.de/wiki/display/AISPD/BREAKINGPOINT+-+Pipeline")')
