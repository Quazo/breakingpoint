# Imports

import os
import sys
import re
import shutil
import getpass
import hou
import platform

USER = getpass.getuser()

FPS = 25

# Setting platform dependend basepath
BP_BASE_PATH = ''
if(platform.system()=='Windows'):
	BP_BASE_PATH = '//bigfoot/breakingpoint'
else:
	BP_BASE_PATH = '/bigfoot/breakingpoint'

BP_PIPELINE_PATH = BP_BASE_PATH + '/_pipeline'
BP_OTL_PATH = BP_PIPELINE_PATH + '/otl/publish'

BP_HDRI_PATH = BP_BASE_PATH + '/2_production/0_footage/hdri'

BP_RENDER_PATH = BP_BASE_PATH + '/2_production/3_render'

BP_SCRIPTS_PATH = BP_PIPELINE_PATH + '/houdini/'

BP_SHOTS_PATH = '{0}/2_production/2_shots'.format(BP_BASE_PATH)

# Set / Get shot name
BP_SHOT_NAME = '$BP_SHOT_NAME'

try:

	hou.hscriptExpression(BP_SHOT_NAME)

	BP_SHOT_NAME_VALUE = hou.expandString('$BP_SHOT_NAME')

except:

	print('Initializing {0} to an empty value'.format(BP_SHOT_NAME))

	hou.hscript('set -g BP_SHOT_NAME = {0}'.format(''))


# Set variables
# --------------------------------------------------------------------------------------------
try:
	
	
	hou.hscript('set -g BP_SHOT_NAME = {0}'.format(BP_SHOT_NAME))
	hou.hscript('set -g BP_SHOTS_PATH = {0}'.format(BP_SHOTS_PATH))
	hou.hscript('set -g BP_HDRI_PATH = {0}'.format(BP_HDRI_PATH))
	hou.hscript('set -g BP_OTL_PATH = {0}'.format(BP_OTL_PATH))
	hou.hscript('set -g BP_RENDER_PATH = {0}'.format(BP_RENDER_PATH))
	hou.hscript('set -g JOB = {0}'.format(BP_SCRIPTS_PATH))

	print 'Environment variables set.'

	
except:

	print 'Could not set environment variables.'


# FPS
hou.setFps(FPS)
print('fps set to {0}'.format(FPS))


print "456.cmd successfully executed."
print "Welcome " + USER