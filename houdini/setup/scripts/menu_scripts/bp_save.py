import sys
import hou


def save_increment():

    if(not hou.hipFile.hasUnsavedChanges()):
        return

    try:

        hou.hipFile.saveAndIncrementFileName()
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
