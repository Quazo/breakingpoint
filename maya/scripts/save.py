#*************************************************************
# title:        Save
#
# software:     Maya
#
# content:      automaticly saves work and publish files
#               automaticly executes other scripts on PUBLISH
#
# dependencies: "PYTHONPATH=%SOFTWARE_PATH%;%PYTHONPATH%"
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************

import os 
import sys
import shutil
import webbrowser

from PySide.QtGui import *
from PySide.QtCore import *

import maya.mel as mel
import maya.cmds as cmds


from scripts.ui import save
import settings as s

sys.path.append(s.PATH['lib'])
from lib import *


#**********************
# RUN DOS RUN
#**********************
saveW   = QWidget()
ui      = save.Ui_save()


#**********************
# VARIABLE
#**********************
VERSION         = "v0.50"

FILE_NAME       = ['140', s.TASK["shading"], 'v001', 'ar']
SAVE_DIR        = ''

SCENE_SHD_PATH  = s.PATH_EXTRA["scene_shd"]
META_DATA       = "Resolution:  2048 x 1152\n\nFPS:           25\n\nFrames:       1001 - "


#**********************
# CLICKED_TRIGGER
#**********************
def clicked_btnSave():
    saveFile()


def clicked_btnCancel():
    saveW.close() 


def clicked_btnHelp():
    webbrowser.open(s.LINK["software"])


def clicked_btnOpenFolder():
    global SAVE_DIR
    webbrowser.open(SAVE_DIR)


def clicked_btnReport():
    libReport.start("Save")


def clicked_btnMsgFolder():
    global SAVE_DIR
    output = libMessageBox.folderMsgBox(saveW, "Maya Files (*.mb *.ma)", "Choose Maya File to Open", SAVE_DIR)
    print "OUTPUT: " + str(output)
    
    initPath(output)


def clicked_btnVersionUp():
    global FILE_NAME

    if('v' in FILE_NAME[2]): 
        FILE_NAME[2] = FILE_NAME[2].replace('v', '')
        FILE_NAME[2] = 'v' + str('{0:03d}'.format(int(FILE_NAME[2]) + 1))

    ui.edtSavePath.setText(('_').join(FILE_NAME) + '.' + s.SOFTWARE_FORMAT["maya"])
    changed_edtComment()


def clicked_btnVersionDown():
    global FILE_NAME

    if('v' in FILE_NAME[2] and FILE_NAME[2] != "v000"): 
        FILE_NAME[2] = FILE_NAME[2].replace('v', '')
        FILE_NAME[2] = 'v' + str('{0:03d}'.format(int(FILE_NAME[2]) - 1))

    ui.edtSavePath.setText(('_').join(FILE_NAME) + '.' + s.SOFTWARE_FORMAT["maya"])
    changed_edtComment()


#**********************
# CHANGED_TRIGGER
#**********************
def changed_user(): 
    global FILE_NAME, SAVE_DIR  

    # CHANGE USER IMG
    libFunction.changeUserImg(ui.cbxUser.currentText(), ui.lblUser)

    # CHANGE USER TOKEN
    FILE_NAME[3] = ui.cbxUser.currentText()[:2]
    ui.edtSavePath.setText(('_').join(FILE_NAME) + '.' + s.SOFTWARE_FORMAT["maya"])
    ui.edtPath.setText(os.path.join(SAVE_DIR, ui.edtSavePath.text()))
    changed_edtComment()


def changed_publish():
    if(ui.cbxPublish.isChecked()):
        ui.edtComment.setEnabled(False)
        ui.edtComment.setPlainText('')
        ui.lblStatus.setText(s.STATUS["publish"])

    else:
        ui.edtComment.setEnabled(True)
        ui.lblStatus.setText(s.STATUS["work"])
       

def changed_edtComment():
    if not (ui.edtComment.toPlainText() == "Comment"):    
        if (ui.edtComment.toPlainText().isalnum() == False and ui.edtComment.toPlainText() != ""):
            ui.edtComment.textCursor().deletePreviousChar()
            # ui.edtPath.setText("FAIL: Comment uses alphanumeric character. Please use lower camelCase!")
            print ("FAIL: Comment uses alphanumeric character. Please use lower camelCase!")

        elif (len(ui.edtComment.toPlainText()) < 20):
            if not (ui.edtComment.toPlainText() == ''):
                ui.edtSavePath.setText(('_').join(FILE_NAME) + '_' + ui.edtComment.toPlainText() + '.' + s.SOFTWARE_FORMAT["maya"])   
            else:
                ui.edtSavePath.setText(('_').join(FILE_NAME) + '.' + s.SOFTWARE_FORMAT["maya"])   

        else:
            ui.edtComment.textCursor().deletePreviousChar()
            ui.edtPath.setText("FAIL: Comment is to long")
       

def changed_edtSavePath():
    global SAVE_DIR 
    currentFile = ui.edtPath.text()

    if(len(currentFile.split('.')) > 1):
        (FILE_NAME, s.SOFTWARE_FORMAT["maya"]) = currentFile.split('.')

        if (len(FILE_NAME.split('_')) > 4):
            FILE_NAME = FILE_NAME.split('_')
        else:
            ui.edtPath.setText('NAME CONVENTION: Not conform name setting - 010_' + s.TASK["shading"] + '_v001_ar.' + s.SOFTWARE_FORMAT["maya"])

    ui.edtPath.setText(os.path.join(SAVE_DIR, ui.edtSavePath.text()))


#**********************
# FUNCTIONS
#**********************
def initPath(filePath = ''):
    global FILE_NAME, SAVE_DIR

    if(filePath == ''):
        filePath = cmds.file(q=True,sn=True)

    SAVE_DIR        = os.path.dirname(filePath).replace('/','\\')
    currentFile     = os.path.basename(filePath)

    if not (SAVE_DIR):
        SAVE_DIR =  os.path.join(s.PATH['shots'], '000_TEMPLATE\\40_' + s.TASK["lighting"] + '\\WORK')
        currentFile = '000_' + s.TASK["lighting"] + '_v000_ar.' + s.SOFTWARE_FORMAT["maya"]

    if(SAVE_DIR.startswith(s.PATH_PROJECT)): # "\\\\bigfoot\\breakingpoint")):
        SAVE_DIR = SAVE_DIR.replace(s.PATH_PROJECT, s.PATH_SHORT)

    (FILE_NAME, s.SOFTWARE_FORMAT["maya"]) = currentFile.split('.')

    if (len(FILE_NAME.split('_')) == 5):
        (shot, task, version, user, comment) = FILE_NAME.split('_') 
    elif(len(FILE_NAME.split('_')) == 4):
        (shot, task, version, user) = FILE_NAME.split('_')
    else:
        (shot, task) = FILE_NAME.split('_')
        version = "v000"

    user = ui.cbxUser.currentText()[:2]

    if('v' in version): 
        version = version.replace('v', '')
        version = 'v' + str('{0:03d}'.format(int(version) + 1))

    FILE_NAME = [shot, task, version, user]

    ui.lblBanner.setPixmap(QPixmap(QImage(libFunction.setBannerImg(task))))
    ui.lblImage.setPixmap(QPixmap(QImage(libFunction.setShotImage(shot))))

    ui.edtSavePath.setText(('_').join(FILE_NAME) + '.' + s.SOFTWARE_FORMAT["maya"])
    ui.lblShotNr.setText(shot)

    if(s.STATUS["publish"] in SAVE_DIR):
        SAVE_DIR = SAVE_DIR.replace(s.STATUS["publish"], s.STATUS["work"])

    ui.edtPath.setText(os.path.join(SAVE_DIR, ui.edtSavePath.text()))
    libFunction.changeMetaData(FILE_NAME[0], ui.edtMetaData)


def saveFile():
    global SAVE_DIR, FILE_NAME

    msgText         = "File was saved!\n\n"
    sceneReference  = []

    # SAVE FILE:
    tmpSavePath = os.path.join(SAVE_DIR, ui.edtSavePath.text() + '.' + s.SOFTWARE_FORMAT["maya"])
    
    # USE ADDITIONAL PUBLISH SCRIPTS
    if(ui.cbxPublish.isChecked()):

        msgText = "File was published!\n\n"

        try:
            # CUSTOM TASK SCRIPTS
            if(s.TASK["modeling"] == FILE_NAME[1]):
                print ("PUBLISH: " + s.TASK["modeling"])


            if(s.TASK["shading"] == FILE_NAME[1]):
                print ("PUBLISH: " + s.TASK["shading"])

                try:
                    mel.eval('file -removeReference -referenceNode "SCENE_' + s.TASK["shading"] + 'RN";')
                except:
                    print("** FAIL | SAVE: Cant remove SCENE_" + s.TASK["shading"] + " reference **")

                try:
                    from scripts.SHD import uniteShaderGroup
                    uniteShaderGroup.start()
                except:
                    print ("** FAIL | Unite Shader and Shader Group **")

                sceneFile = mel.eval('file -q -l;') [1:]

                for files in sceneFile:
                    if(files.endswith("."+ s.SOFTWARE_FORMAT["maya"])):
                        tmpReference = os.path.basename(files).split(".")[0] + "RN"
                        sceneReference.append(tmpReference)

                        try:
                            cmds.file(unloadReference=tmpReference)
                        except:
                            print ("FAIL | SAVE: Reference not exists: " + tmpReference)

            if(s.TASK["rigging"] == FILE_NAME[1]):
                print ("PUBLISH: " + s.TASK["rigging"])    

            if(s.TASK["lighting"] == FILE_NAME[1]):
                print ("PUBLISH: " + s.TASK["lighting"])
                
        except:
            msgFailed = "** SORRY | SAVE: One helping script failed! **"
            print(msgFailed)
            msgText = msgText + msgFailed

    # MsgBox: File exists
    if (os.path.isfile(tmpSavePath)):
        if (QMessageBox.Cancel == libMessageBox.questionMsgBox("Overwrite", "File exists", "Overwrite the file?", QMessageBox.Warning)):
            print ("** FAIL | SAVE: Overwrite canceled **")
            return

    try:    
        cmds.file( rename = tmpSavePath)
        cmds.file( save = True, type = 'mayaAscii' )

    except:
        msgText = "FAIL | SAVE: Couldnt save file!"

    print ("SAVE: " + tmpSavePath)

    if(ui.cbxPublish.isChecked()):
        # COPY FILE WITH _PUBLISH
        tmpCopyWork = os.path.join(SAVE_DIR, ('_').join(FILE_NAME) + '_PUBLISH' + '.' + s.SOFTWARE_FORMAT["maya"])
        shutil.copy(tmpSavePath, tmpCopyWork)
        
        print ("COPY: " + tmpCopyWork)
        
        if(s.STATUS["work"] in SAVE_DIR):
            SAVE_DIR = SAVE_DIR.replace('WORK', 'PUBLISH')

        # PUBLISH FILE
        if(s.TASK["animation"] == FILE_NAME[1]):
            print ("ANIM PUBLISH")
            from scripts.ANIM import alembicExport
            msgText = "File was saved!\n\n" + alembicExport.start()
            print ("PUBLISH: ALEMBIC") 

        else:
            tmpCopyPublish = os.path.join(SAVE_DIR, ('_').join(FILE_NAME[:2]) + '.' + s.SOFTWARE_FORMAT["maya"])
            shutil.copy(tmpSavePath, tmpCopyPublish)
            print ("PUBLISH: " + tmpCopyPublish)

        if(s.TASK["shading"] == FILE_NAME[1]): 
            from scripts.SHD import referenceSCENE_SHD
            referenceSCENE_SHD.start()

            for tmpReference in sceneReference:
                if not (sceneReference == ""):
                    cmds.file(loadReference = tmpReference)

            cmds.file(s = True)

    QMessageBox.information( saveW, "Save", msgText.replace("**", "") ) 

    print ("** DONE | SAVE: Save File **")
    saveW.close() 


def comment_In(event):
    if(ui.edtComment.toPlainText() == "Comment"):
        ui.edtComment.setPlainText("")
        ui.edtComment.setStyleSheet("color: rgb(255, 255, 255);")
    ui.edtComment.setCursorWidth(1)


def comment_Out(event):
    if(ui.edtComment.toPlainText() == ""):
        ui.edtComment.setPlainText("Comment")
        ui.edtComment.setStyleSheet("color: rgb(175, 175, 175);")
    ui.edtComment.setCursorWidth(0)


#**********************
# START PROZESS
#**********************
def setSave():
    userList = libFileService.getFolderList(s.PATH['data_user'])
    ui.cbxUser.addItems(sorted(userList))
    
    if(os.getenv('username') in userList):      
        ui.cbxUser.setCurrentIndex(ui.cbxUser.findText(os.getenv('username')))

    initPath()


#**********************
# START UI
#**********************
def start():
    ui.setupUi(saveW)

    ui.lblVersion.setText(VERSION)
    
    saveW.connect(ui.btnSave, SIGNAL("clicked()"), clicked_btnSave)
    saveW.connect(ui.btnCancel, SIGNAL("clicked()"), clicked_btnCancel)
    saveW.connect(ui.btnHelp, SIGNAL("clicked()"), clicked_btnHelp)
    saveW.connect(ui.btnOpenFolder, SIGNAL("clicked()"), clicked_btnOpenFolder)
    saveW.connect(ui.btnReport, SIGNAL("clicked()"), clicked_btnReport)
    saveW.connect(ui.btnFolder, SIGNAL("clicked()"), clicked_btnMsgFolder)
    saveW.connect(ui.btnVersionUp, SIGNAL("clicked()"), clicked_btnVersionUp)
    saveW.connect(ui.btnVersionDown, SIGNAL("clicked()"), clicked_btnVersionDown)

    saveW.connect(ui.cbxUser, SIGNAL("currentIndexChanged(const QString&)"), changed_user)

    ui.cbxPublish.toggled.connect(changed_publish)  
    ui.edtSavePath.textChanged.connect(changed_edtSavePath)
    ui.edtComment.textChanged.connect(changed_edtComment)

    ui.edtComment.focusInEvent = comment_In
    ui.edtComment.focusOutEvent = comment_Out

    setSave()
    saveW.show()