import sys
import hou
import os
import glob
import re
import shutil


def crash_recovery():

    TEMP_PATH = hou.expandString("$TEMP")
    newest_hip = max(glob.iglob(TEMP_PATH + "/*.hip*"), key=os.path.getctime)
    newest_hip = newest_hip.replace("/", "\\")

    old_path = ""
    with open(newest_hip, mode="rb") as f:
        for line in f.readlines():
            if(line.startswith("set -g HIPFILE = ")):
                old_path = line.replace("set -g HIPFILE = ", "")
                old_path = old_path.replace("\'", "")
                old_path = old_path.replace("\n", "")
                break

    version_s = re.search("(?<=_v)", old_path)
    old_version = old_path[version_s.start():version_s.start()+3]
    new_version = "%03d" % (int(old_version)+1)

    new_path = old_path.replace("v{0}".format(old_version), "v{0}".format(new_version))
    new_path = new_path.replace(".hip", "_CRASH.hip")

    shutil.copy2(old_path, new_path)
    hou.hipFile.load(new_path)

    hou.ui.setStatusMessage("[BP] Recovered crashed file {0} to {1} successfully".format(old_path, new_path))


# Main
arg = sys.argv[1]

if(arg == "crash_recovery"):
    crash_recovery()
