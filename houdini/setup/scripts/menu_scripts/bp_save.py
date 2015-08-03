import sys
import hou
import re


def save_increment():

    if(not hou.hipFile.hasUnsavedChanges()):
        return

    hipname = hou.expandString("$HIPNAME")
    hip = hou.expandString("$HIP")

    if("CRASH" in hipname):
        hipname.replace("_CRASH", "")
    if("PUBLISH" in hipname):
        hipname.replace("_PUBLISH")

    version_s = re.search("(?<=_v)", hipname)
    old_version = hipname[version_s.start():version_s.start()+3]
    new_version = "%03d" % (int(old_version)+1)

    hipname = hipname.replace("v{0}".format(old_version), "v{0}".format(new_version))

    try:

        hou.hipFile.save(file_name="{0}/{1}".format(hip, hipname))
        # hou.hipFile.saveAndIncrementFileName()
        HIPFILE = hou.expandString("$HIPFILE")
        msg = "[BP] Successfully saved under : {0}".format(HIPFILE)
        msgSeverityType = hou.severityType.ImportantMessage
        hou.ui.setStatusMessage(msg, msgSeverityType)

    except:

        hou.ui.setStatusMessage("Save aborted!", hou.severityType.Error)

# Main
arg = sys.argv[1]

if(arg == "increment"):
    save_increment()
