#*************************************************************
# title:        referenceSCENESHD
#
# content:      
#
# dependencies: 
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************


import maya.cmds as cmds
import maya.mel as mel

import settings as s

def start():

	if not(s.PATH_EXTRA["scene_shd"].replace("\\","/") in mel.eval('file -q -l;')):
		
		try:
		    cmds.file(s.PATH_EXTRA["scene_shd"], r=True )
		    mel.eval('lookThroughModelPanel SCENE_SHD_cam_SHD_sceneShape modelPanel4;')
		
		except:
		    print ("** FAIL | Reference SCENE_SHD: Scene or Camera is already used! **")
		
		print("** DONE | Reference SCENE_SHD: Reference SCENE_SHD! **")
	
	else:
		print("** FAIL | Reference SCENE_SHD: SCENE_SHD already exist! **")