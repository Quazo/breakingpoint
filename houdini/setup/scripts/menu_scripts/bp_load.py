import sys
import hou
import os
import glob


def crash_recovery():

    TEMP_PATH = hou.expandString("$TEMP")
    newest_hip = max(glob.iglob(TEMP_PATH + "/*.hip*", key=os.path.getctime))
    print(newest_hip)


# Main
arg = sys.argv[1]

if(arg == "crash_recovery"):
    crash_recovery()
