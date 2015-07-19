# Imports

import os
import sys
import re
import shutil
import getpass
import hou
import platform

# BP Scene Defaults
FPS = 25

FSTART = 950
FEND = 1100
RFSTART = 1021
RFEND = 1100

USER = getpass.getuser()
HIPNAME = hou.expandString('$HIPNAME')

# Setting platform dependend basepath
BP_BASE_PATH = ''
if(platform.system() == 'Windows'):
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
    hou.hscript('set -g BP_SHOT_NAME = {0}'.format(''))
    print('Initialized {0} to an empty value'.format(BP_SHOT_NAME))


# Set Environment
# -----------------------------------------------------------------------------

try:
    hou.hscript('set -g BP_SHOT_NAME = {0}'.format(BP_SHOT_NAME))
    hou.hscript('set -g BP_SHOTS_PATH = {0}'.format(BP_SHOTS_PATH))
    hou.hscript('set -g BP_HDRI_PATH = {0}'.format(BP_HDRI_PATH))
    hou.hscript('set -g BP_OTL_PATH = {0}'.format(BP_OTL_PATH))
    hou.hscript('set -g BP_RENDER_PATH = {0}'.format(BP_RENDER_PATH))
    hou.hscript('set -g JOB = {0}'.format(BP_SCRIPTS_PATH))

    print('Environment variables set.')

except:
    print("Could not set environment variables.")


# Set Scene Values
# -----------------------------------------------------------------------------

# FPS
hou.setFps(FPS)
print("FPS set to {0}".format(FPS))

# Set Framerange
if(HIPNAME == 'untitled'):
    hou.hscript('tset `{0}/$FPS` `{1}/$FPS`'.format(FSTART, FEND))
    hou.playbar.setPlaybackRange(RFSTART, RFEND)
    hou.playbar.setRealTime(True)
    hou.setFrame(RFSTART)
    print("Default Framerange set.")

# Success messages
print("456.cmd successfully executed.")
print("Welcome " + USER)
