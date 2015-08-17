#*************************************************************
# title:        uniteShaderGroup
#
# content:      sets the name of all shader groups as the shader (+SG)
#
# dependencies: 
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************


from pymel.core import *

import maya.cmds as cmds
import maya.mel as mel


def getSGFromMaterial(mat):
    mat = PyNode(mat)
    return mat.shadingGroups()


def start(shaderType = "alSurface"): 

	shaderList = cmds.ls(type = shaderType)

	for shader in shaderList:

	    shaderGroup = getSGFromMaterial(shader)
	    
	    if (shaderGroup != shader + "SG"):       
	        try:
	        	mel.eval('rename ' + shaderGroup[0] +  ' ' + shader + 'SG;')
	        except:
	        	print ("** FAIL | Unite Shader and Shader Group: Shader has no shading group or is a reference - " + shader + " **")

	print ("** DONE | Unite Shader and Shader Group **")