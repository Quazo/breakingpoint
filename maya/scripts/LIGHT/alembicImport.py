#*************************************************************
# title:        ALEMBIC IMPORT
#
# content:      
#
# dependencies: 
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************

import os, sys

import maya.cmds as cmds
import maya.mel as mel



def start():

	#referenceNode
	mel.eval('file -r -type "mayaAscii"  -ignoreVersion -gl -mergeNamespacesOnClash false -namespace "SCENE_SHD" -options "v=0;" "//bigfoot/breakingpoint/2_production/0_footage/shader/SCENE_SHD/PUBLISH/SCENE_SHD.ma";')


