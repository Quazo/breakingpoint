# Imports

import os
import sys
import hou


def report():
    sys.path.append('P:\_pipeline')
    from lib import libReport
    libReport.start(currentScript='other', software='houdini')


# Main
arg = sys.argv[1]

if(arg == "report"):
    report()
