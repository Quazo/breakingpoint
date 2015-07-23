import maya.cmds as cmds


print("BREAKINGPOINT: settings")

# Change the current time unit to ntsc
cmds.currentUnit( time='pal' )





# cmds.setAttr ("defaultArnoldRenderOptions.textureMaxMemoryMB", 10024)
# cmds.setAttr ("defaultArnoldRenderOptions.display_gamma", 1)
# cmds.setAttr ("defaultArnoldRenderOptions.light_gamma", 1)
# cmds.setAttr ("defaultArnoldRenderOptions.shader_gamma", 1)
# cmds.setAttr ("defaultArnoldRenderOptions.texture_gamma", 1)