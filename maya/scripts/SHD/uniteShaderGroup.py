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


def start(): 

	shaderList = cmds.ls(type = 'alSurface')

	for shader in shaderList:

	    shaderGroup = getSGFromMaterial(shader)
	    
	    if (shaderGroup != shader + "SG"):       
	        try:
	        	mel.eval('rename ' + shaderGroup[0] +  ' ' + shader + 'SG;')
	        except:
	        	print ("FAIL: Shader has no shading group: " + shader)

	print ("** DONE: Unite names of shader and shader group **")