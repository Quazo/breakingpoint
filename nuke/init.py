#*************************************************************
# function: 	Starup script for Nuke
#			
# depencence: 	set "NUKE_PATH=%PLUGINS_PATH%;%NUKE_PATH%"
#
# author: 		Alexander Richter 
# email:		alexander.richter@filmakademie.de
#*************************************************************

import nuke

import settings as s
sys.path.append(s.PATH["lib"])
from lib import libFunction


#************************
# INIT
#************************
print ("\nWelcome " + libFunction.getCurrentUser())
print ("\nBREAKINGPOINT: System is setting ...\n")


# #*******************
# # VARIABLES
# #*******************
FPS 			= '25'
RESOLUTION 		= '2048 1152 BP_2K'


# #*******************
# # SETTINGS
# #*******************
nuke.knobDefault('Root.fps', FPS)
nuke.addFormat(RESOLUTION)
nuke.knobDefault("Root.format", "BP_2K")



