#*************************************************************
# title: 		User Setup
#
# content:		start point for MAYA
#
# dependencies: "PYTHONPATH=%SOFTWARE_PATH%/maya;%PYTHONPATH%"
#
# author: 		Alexander Richter 
# email:		alexander.richter@filmakademie.de
#*************************************************************


import sys
import os

import maya.cmds as cmds


print ("\nWelcome " + os.getenv('username'))
print ("\nBREAKINGPOINT: System is setting ...\n")

cmds.evalDeferred("from scripts import maya_settings")
cmds.evalDeferred("from scripts import bpMenu")

  
