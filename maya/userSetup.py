#*************************************************************
# title: 		User Setup
#
# software:     Maya
#
# content:		start point for MAYA
#
# dependencies: "PYTHONPATH=%SOFTWARE_PATH%;%PYTHONPATH%"
#
# author: 		Alexander Richter 
# email:		alexander.richter@filmakademie.de
#*************************************************************

import os
import sys 

import maya.cmds as cmds


import settings as s

sys.path.append(s.PATH['lib'])
from lib import *


#************************
# START MAYA
#************************
print ("\nWelcome " + libFunction.getCurrentUser())
print ("\nBREAKINGPOINT: System is setting ...\n")

cmds.evalDeferred("from scripts import maya_settings")
cmds.evalDeferred("from scripts import menu")
