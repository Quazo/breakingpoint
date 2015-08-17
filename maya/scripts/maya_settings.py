#*************************************************************
# title:        Maya Settings
#
# content:      Start settings for Maya
#
# dependencies: userSetup
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************


import maya.cmds as cmds

print("BREAKINGPOINT: settings")


# Change the current time unit to pal
cmds.currentUnit( time='pal' )
cmds.optionVar(sv = ("workingUnitTime", "pal"))
cmds.optionVar(sv = ("workingUnitTimeDefault", "pal"))

cmds.optionVar(sv = ("preferredRenderer", "arnold"))
cmds.optionVar(sv = ("preferredRendererHold", "arnold"))

# cmds.setAttr ("defaultArnoldRenderOptions.textureMaxMemoryMB", 10024)
# cmds.setAttr ("defaultArnoldRenderOptions.display_gamma", 1)
# cmds.setAttr ("defaultArnoldRenderOptions.light_gamma", 1)
# cmds.setAttr ("defaultArnoldRenderOptions.shader_gamma", 1)
# cmds.setAttr ("defaultArnoldRenderOptions.texture_gamma", 1)