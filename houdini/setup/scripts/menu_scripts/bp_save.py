import sys
import hou
import re


def save_increment():

    # Save only if there are unsaved changes
    if(not hou.hipFile.hasUnsavedChanges()):
        return

    hipname = hou.expandString("$HIPNAME")
    hipfile = hou.expandString("$HIPFILE")
    hip = hou.expandString("$HIP")
    hipformat = hipfile.split(".")[-1]

    # Remove Comment
    comment = hipname.split(".")[0].split("_")[-1]
    if(len(comment) > 2):
        hipname = hipname.replace("_{0}".format(comment), "")

    # Increment Version
    version_s = re.search("(?<=_v)", hipname)
    old_version = hipname[version_s.start():version_s.start()+3]
    new_version = "%03d" % (int(old_version)+1)

    old_version = "v{0}".format(old_version)
    new_version = "v{0}".format(new_version)
    hipname = hipname.replace(old_version, new_version)

    try:

        hou.hipFile.save(file_name="{0}/{1}.{2}".format(hip, hipname, hipformat))
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
