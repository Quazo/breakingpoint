#*************************************************************
# title:        alembicExport
#
# content:      automaticly saves work and publish files
#
# dependencies: "PYTHONPATH=%SOFTWARE_PATH%/maya;%PYTHONPATH%"
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************

import os

import maya.cmds as cmds
import maya.mel as mel


def setAttributeToMesh(attribute = "Name"):

	objList = cmds.ls( type="mesh")

	for obj in objList:

	    if not (mel.eval('attributeExists "name" ' + obj)):
	        try: 
	            mel.eval('addAttr -ln "name"  -dt "string" ' + obj + ';')
	        except:
	            print "Name attribute cant be added: " + obj
	    
	    try:    
	        mel.eval('setAttr -type "string" ' + (obj + ".name") + ' ' + obj + ';')
	    except:
	        print "Name attribute cant be set: " + obj


def exportAlembic():
	SAVE_PATH       = os.path.dirname(cmds.file(q=True,sn=True))
	SAVE_PATH		= SAVE_PATH.replace("WORK", "PUBLISH")
	SAVE_FILE     	= os.path.basename(cmds.file(q=True,sn=True))

	if (len(SAVE_FILE.split('_')) > 2):
		tmpFile = SAVE_FILE.split('_')
		SAVE_FILE = tmpFile[0] + "_" + tmpFile[1]

	SAVE_DIR		= (SAVE_PATH + '\\' + SAVE_FILE.split('.')[0] + ".abc").replace("\\","/")

	FRAME_START		= cmds.playbackOptions( query=True, animationStartTime=True )
	FRAME_END		= cmds.playbackOptions( query=True, animationEndTime=True )


	try:
		mel.eval('select -r ASSETS ;')
		mel.eval('select -add CAM ;')
		mel.eval('AbcExport -j "-frameRange ' + str(FRAME_START) + ' ' + str(FRAME_END) + ' -attr name -dataFormat hdf -root |ASSETS -root |CAM -file ' + SAVE_DIR + '";')
		print("** DONE: bpEXPORT IS READY: " + SAVE_DIR.replace("/","\\") + " **")  
	except:
		print("** FAIL: No ASSETS & CAM group in the scene **")

	
def start():

	setAttributeToMesh()
	exportAlembic()