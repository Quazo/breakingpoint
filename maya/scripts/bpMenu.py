#*************************************************************
# title: 		bpMenu
#
# software:       Maya
#
# content:		Adds a Menu with its functions to MAYA
#
# dependencies:   userSetup
#
# author: 		Alexander Richter 
# email:		alexander.richter@filmakademie.de
#*************************************************************

import os, sys

import maya.cmds as cmds


print ("\nWelcome " + os.getenv('username'))
print("setup bpMenu")


#*************************
# MENU
#*************************
bpMenu = cmds.menu('bpMenu', hm = 1, p = 'MayaWindow', l = 'bpMenu', to = 1, )


#*************************
# SAVE
#*************************
cmds.menuItem(p = bpMenu, l = 'Save',c = 'from scripts import bpSave\nbpSave.main()')#, en = 0)
cmds.menuItem(d = True)


#*************************
# SHD
#*************************
toolMenu = cmds.menuItem(p = bpMenu, l = 'SHD', sm = True)#, en = 0)

cmds.menuItem(p = toolMenu,
            l = 'Reference SHD_SCENE',
            c = 'from scripts.SHD import referenceSCENE_SHD\nreferenceSCENE_SHD.start()')

cmds.menuItem(p = toolMenu,
            l = 'Combine SHD and MODEL',
            c = 'from scripts.SHD import combineSHD_MODEL\ncombineSHD_MODEL.start()')

cmds.menuItem(p = toolMenu,
            l = 'Unite Shader and Group',
            c = 'from scripts.SHD import uniteShaderGroup\nuniteShaderGroup.start()')


#*************************
# ANIM
#*************************
toolMenu = cmds.menuItem(p = bpMenu, l = 'ANIM', sm = True)#, en = 0)

cmds.menuItem(p = toolMenu,
            l = 'ALEMBIC EXPORT',
            c = 'from scripts.ANIM import alembicExport\nalembicExport.start()')


#*************************
# LIGHT
#*************************
toolMenu = cmds.menuItem(p = bpMenu, l = 'LIGHT', sm = True, en = 0)

cmds.menuItem(p = toolMenu,
            l = 'ALEMBIC IMPORT',
            c = 'from scripts.LIGHT import alembicImport\nalembicImport.start()')


#*************************
# RENDER
#*************************
toolMenu = cmds.menuItem(p = bpMenu, l = 'RENDER', sm = True, en = 0)

cmds.menuItem(p = toolMenu,
            l = 'Set Render Settings',
            c = 'from scripts.RENDER import renderSettings\nrenderSettings.start()')

cmds.menuItem(p = bpMenu,
             d = True)


# cmds.menuItem(p = bpMenu,
#             l = 'Report',
#             c = '', en = 0)


#*************************
# HELP
#*************************
cmds.menuItem(p = bpMenu,
            l = 'Wiki',
            c = 'import webbrowser\nwebbrowser.open("https://www.filmakademie.de/wiki/display/AISPD/BREAKINGPOINT+-+Pipeline")')
