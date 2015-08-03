#*************************************************************
# title:        uniteShaderGroup
#
# content:      automaticly saves work and publish files
#
# dependencies: "PYTHONPATH=%SOFTWARE_PATH%/maya;%PYTHONPATH%"
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
	        print shaderGroup
	        print shader
	        print ""
	        mel.eval('rename ' + shaderGroup[0] +  ' ' + shader + 'SG;') ;

	print ("** DONE: Unite Shader and Group **")