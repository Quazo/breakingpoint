import sys
import os

import maya.cmds as cmds


print("BREAKINGPOINT: userSetup\n")

cmds.evalDeferred("from scripts import settings")
cmds.evalDeferred("from scripts import bpMenu")

  
