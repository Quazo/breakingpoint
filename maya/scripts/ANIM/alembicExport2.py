#*************************************************************
# title:        Alembic Export
#
# software:     Maya
#
# content:      exports selectiv or the whole scene
#
# dependencies: lib, settings
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************

import os, sys
import shutil
import webbrowser

from PySide.QtGui import *
from PySide.QtCore import *

sys.path.append("..")
from ui import alembicExport

# import maya.cmds as cmds
# import maya.mel as mel

sys.path.append("../../../..")
import settings as s
sys.path.append(s.PATH['lib'])
import libFunction


#**********************
# RUN DOS RUN
#**********************
app     = QApplication(sys.argv)
WIDGET  = QWidget()
ui      = alembicExport.Ui_alembicExport()


#**********************
# VARIABLE
#**********************
CHECKBOX    = []
SAVE_DIR    = ""
SAVE_PATH   = ""
ERROR       = " Wrong name: "

#**********************
# CLICKED_TRIGGER
#**********************
def clicked_export():
    global WIDGET
    

    objectGroups = selectObjects()
    print objectGroups

    ui.edtMsg.setText("Alembic Export | In Progress ... 1 of " + str(len(objectGroups)))

    if not (objectGroups):
        ui.edtMsg.setText("Fail: Nothing was selected!")
    elif(ui.cbxMerge.isChecked()):
        ui.edtMsg.setText(exportAlembic(objectGroups))
    elif (len(objectGroups) < 2):
        ui.edtMsg.setText(exportAlembic(objectGroups[0], False))
    else:
        for obj in objectGroups:
            ui.edtMsg.setText(exportAlembic(obj, False))


def clicked_cancel():
    global WIDGET
    WIDGET.close()


def clicked_help():
    webbrowser.open(s.LINK["software"])


def clicked_report():
    libReport.start("Save")


def clicked_openFolder():
    global SAVE_PATH
    webbrowser.open(SAVE_PATH)


#**********************
# CHANGED_TRIGGER
#**********************



#**********************
# CHECKED_TRIGGER
#**********************
def checked_allObjects():
    ui.cbxAssets.setChecked(ui.cbxAll.isChecked())
    ui.cbxCam.setChecked(ui.cbxAll.isChecked())
    ui.cbxLight.setChecked(ui.cbxAll.isChecked())


def checked_assets():
    ui.cbxAssetsChar.setChecked(ui.cbxAssets.isChecked())
    ui.cbxAssetsSet.setChecked(ui.cbxAssets.isChecked())
    ui.cbxAssetsProp.setChecked(ui.cbxAssets.isChecked())
    ui.cbxAssetsFx.setChecked(ui.cbxAssets.isChecked())


#**********************
# FUNCTIONS
#**********************
def selectObjects():
    global CHECKBOX, ERROR
    print ("GO")
    checkList = []

    for box in CHECKBOX:
        if (box.isChecked()):
            if(box.text() == "fx"):
                    for box2 in cmds.listRelatives("fx"):
                        if (box2[1:4].isdigit() and box2.startswith("D")):
                            checkList.append(box2)
                            ERROR += box2 + "  "
            else:
                checkList.append(box.text())

    return checkList


def setAttributeToMesh(attribute = "Name"):

    objList = cmds.ls( type = "mesh")

    for obj in objList:

        if not (mel.eval('attributeExists "name" ' + obj)):
            try: 
                mel.eval('addAttr -ln "name"  -dt "string" ' + obj + ';')
            except:
                print "Name attribute cant be added: " + obj
        
        try:    
            mel.eval('setAttr -type "string" ' + (obj + ".name") + ' ' + obj + ';')
        except:
            print "Name attribute cant be set: " + obj


def exportAlembic(objectGroup = ["ASSETS", "CAM"], multiply = True):
    global SAVE_DIR, SAVE_PATH, ERROR

    msgText = ""

    # setAttributeToMesh()
    SAVE_PATH       = os.path.dirname(cmds.file(q=True,sn=True))
    SAVE_PATH       = SAVE_PATH.replace("WORK", "PUBLISH")

    FRAME_START     = cmds.playbackOptions( query = True, animationStartTime = True )
    FRAME_END       = cmds.playbackOptions( query = True, animationEndTime = True )
    tmpExport       = 'AbcExport -j "-frameRange ' + str(FRAME_START) + ' ' + str(FRAME_END)
    
    mel.eval('select -cl  ;')

    if(multiply):
        tmpExport += ' -attr name -dataFormat hdf '
        for obj in objectGroup:
            tmpExport += "-root " + obj + " "
    else:
        tmpSave     = objectGroup
        tmpExport   += ' -stripNamespaces -dataFormat hdf ' 

        if (objectGroup[1:4].isdigit() and objectGroup.startswith("D")):
            
            alembic = objectGroup.split("_")[1] + ":" + cmds.listRelatives("D0100_genericSplashGroundA")[0].split(":")[0] + "_AlembicNode.offset"
            offset = int(cmds.getAttr (alembic))
            #int(17.656) #need OFFSET
            if(offset > 0):
                offset = "+" + '{0}'.format(str(offset).zfill(3))

            s1 = str("%0.3f" % cmds.getAttr(objectGroup + ".tx")).replace(".", ",")
            s2 = str("%0.3f" % cmds.getAttr(objectGroup + ".ty")).replace(".", ",")
            s3 = str("%0.3f" % cmds.getAttr(objectGroup + ".tz")).replace(".", ",")
            tmpSave += ".f" + offset + ".s" + s1 + ".s" + s2 + ".s" + s3
            # D0100_genericSplashGroundB.f+017.s1,388.s1,388.s1,388
        SAVE_PATH += '/FX_GEO/'
        if not(os.path.exists(SAVE_PATH)):
            os.makedirs(SAVE_PATH)
        SAVE_DIR = (SAVE_PATH + tmpSave + ".abc").replace("\\","/")
        tmpExport += "-root " + objectGroup + " "

    tmpExport += '-file ' + SAVE_DIR + '";'
    mel.eval(tmpExport)
    print tmpExport
    #'AbcExport -j "-frameRange ' + str(FRAME_START) + ' ' + str(FRAME_END) + ' -attr name -stripNamespaces -dataFormat hdf -root |ASSETS -root |CAM -file ' + SAVE_DIR + '";'
    if(ERROR == " Wrong name: "):
        ERROR = ""
    msgText = "DONE | ALEMBIC EXPORT" + ERROR
    
    return msgText


#**********************
# INIT
#**********************
def init():
    global SAVE_DIR, SAVE_PATH
    SAVE_PATH       = os.path.dirname(cmds.file(q=True,sn=True))
    SAVE_PATH       = SAVE_PATH.replace("WORK", "PUBLISH")
    SAVE_FILE       = os.path.basename(cmds.file(q=True,sn=True))

    if (len(SAVE_FILE.split('_')) > 2):
        tmpFile = SAVE_FILE.split('_')
        SAVE_FILE = tmpFile[0] + "_" + tmpFile[1]

    SAVE_DIR        = (SAVE_PATH + '\\' + SAVE_FILE.split('.')[0] + ".abc").replace("\\","/")


#**********************
# START PROZESS
#**********************
def start():
    global WIDGET
    WIDGET  = QWidget()
    ui.setupUi(WIDGET)

    WIDGET.connect(ui.btnExport, SIGNAL("clicked()"), clicked_export)
    WIDGET.connect(ui.btnCancel, SIGNAL("clicked()"), clicked_cancel)
    WIDGET.connect(ui.btnHelp, SIGNAL("clicked()"), clicked_help)
    WIDGET.connect(ui.btnReport, SIGNAL("clicked()"), clicked_report)
    WIDGET.connect(ui.btnOpenFolder, SIGNAL("clicked()"), clicked_openFolder)

    ui.cbxAll.toggled.connect(checked_allObjects) 
    ui.cbxAssets.toggled.connect(checked_assets) 

    CHECKBOX.append(ui.cbxCam)
    CHECKBOX.append(ui.cbxLight)
    CHECKBOX.append(ui.cbxAssetsChar)
    CHECKBOX.append(ui.cbxAssetsProp)
    CHECKBOX.append(ui.cbxAssetsSet)
    CHECKBOX.append(ui.cbxAssetsFx)

    libFunction.setUserImg(imgObj = ui.lblUser)

    init()

    WIDGET.show() 
    sys.exit(app.exec_())  

start()