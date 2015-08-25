#*************************************************************
# title: 		Menu
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

import os
import sys

import maya.cmds as cmds

import settings as s
sys.path.append(s.PATH['lib'])
import libFunction


#************************
# START MAYA
#************************
print ("\nWelcome " + libFunction.getCurrentUser())
print("\nsetup bpMenu\n")


#*************************
# MENU
#*************************
menu = cmds.menu('bpMenu', hm = 1, p = 'MayaWindow', l = 'bpMenu', to = 1, )


#*************************
# SAVE
#*************************
cmds.menuItem(p = menu, l = 'Save',c = 'from scripts import save\nsave.start()')#, en = 0)
cmds.menuItem(d = True)


#*************************
# SHD
#*************************
toolMenu = cmds.menuItem(p = menu, l = 'SHD', sm = True)

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
toolMenu = cmds.menuItem(p = menu, l = 'ANIM', sm = True)

cmds.menuItem(p = toolMenu,
            l = 'ALEMBIC EXPORT',
            c = 'from scripts.ANIM import alembicExport\nalembicExport.start()')


#*************************
# LIGHT
#*************************
toolMenu = cmds.menuItem(p = menu, l = 'LIGHT', sm = True, en = 0)

cmds.menuItem(p = toolMenu,
            l = 'ALEMBIC IMPORT',
            c = 'from scripts.LIGHT import alembicImport\nalembicImport.start()')


#*************************
# RENDER
#*************************
toolMenu = cmds.menuItem(p = menu, l = 'RENDER', sm = True, en = 0)

cmds.menuItem(p = toolMenu,
            l = 'Set Render Settings',
            c = 'from scripts.RENDER import renderSettings\nrenderSettings.start()')

cmds.menuItem(p = menu,
             d = True)


#*************************
# HELP
#*************************
cmds.menuItem(p = menu,
            l = 'Report',
            c = 'from lib import libReport\nlibReport.start()')

cmds.menuItem(p = menu,
            l = 'Help',
            c = 'import webbrowser\nwebbrowser.open("https://www.filmakademie.de/wiki/display/AISPD/BREAKINGPOINT+-+Software")')
