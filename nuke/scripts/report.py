#*************************************************************
# title:        Report Error
#
# software:     Maya
#
# content:      Send a error report
#
# dependencies: "PYTHONPATH=%SOFTWARE_PATH%;%PYTHONPATH%"
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************

import os
import sys
import shutil
import subprocess
import webbrowser
from datetime import datetime

from PySide.QtGui import *
from PySide.QtCore import *


# from ui import report
from scripts.ui import report
import settings as s

sys.path.append(s.PATH['lib'])
from lib import *


#**********************
# RUN DOS RUN
#**********************
#app         = QApplication(sys.argv)
REPORTW     = QWidget()
ui          = report.Ui_report()


#**********************
# VARIABLE
#**********************
CURRENT_USER    = ""
REPORTS         = ""
REPORT_INDEX    = 0

reportList      = ["Bug", "Suggestion"]
scriptList      = ["Save", "Reference SHD_SCENE", "Combine SHD and Model", "Alembic Export", "Alembic Import", "other"]


#**********************
# CLICKED_TRIGGER
#**********************
def clicked_report():
    global REPORTW
    print ("** DONE: REPORT **")
    saveFile()
    REPORTW.close() 


def clicked_cancel():
    global REPORTW
    REPORTW.close()


def clicked_help():
    webbrowser.open(s.LINK["software"])


def clicked_showReport():
    global REPORTS
    
    if not (ui.edtComment.isReadOnly()):

        ui.edtComment.setReadOnly(True)
        ui.edtScript.setReadOnly(True)
        ui.edtErrorMsg.setReadOnly(True)
        
        ui.btnReport.hide()
        ui.btnCancel.hide()     

        ui.btnBefore.show()
        ui.btnNext.show() 
        ui.btnSaveToHistory.show() 
        ui.btnFolder.show() 
       
        REPORTS = libFileService.getFolderList(s.PATH["data_report"], "*.json")

        ui.btnShowReport.setIcon(QPixmap(QImage(s.PATH["img_shelf"] + "\\" + "shelf_report35.png")))

        setReports(len(REPORTS) - 1)

    else:
        ui.edtComment.setReadOnly(False)
        ui.edtScript.setReadOnly(False)
        ui.edtErrorMsg.setReadOnly(False)
        
        ui.btnReport.show()
        ui.btnCancel.show()     

        ui.btnBefore.hide()
        ui.btnNext.hide()  
        ui.btnSaveToHistory.hide()  
        ui.btnFolder.hide()  

        ui.cbxReport.clear()
        ui.cbxScript.clear()

        ui.btnShowReport.setIcon(QPixmap(QImage(s.PATH["img_shelf"] + "\\" + "shelf_outliner35.png")))
        
        setScript()


def clicked_before():
    setReports(-1)


def clicked_next():
    setReports(1)


def clicked_saveToHistory():
    global REPORTS
    print ("Save To History")
    
    if(len(REPORTS) - 1 < 0):
        return

    src = s.PATH["data_report"] + "\\" + REPORTS[REPORT_INDEX] + ".json"
    dst = s.PATH["data_report"] + "\\history\\" + REPORTS[REPORT_INDEX] + ".json"

    shutil.move(src, dst)
    REPORTS = libFileService.getFolderList(s.PATH["data_report"], "*.json")
    setReports(1)


def clicked_folder():
    webbrowser.open(s.PATH["data_report"])


#**********************
# CHANGED_TRIGGER
#**********************
def changed_report():
    global REPORTW
    currentImgPath = os.path.join(s.PATH['img_shelf'], "shelf_" + ui.cbxReport.currentText() + "35.png")
    
    if(ui.cbxScript.currentText() == "other"):
        changeY = 30 
    else:
        changeY = 0

    if(ui.cbxReport.currentText() == "Suggestion"):

        ui.edtErrorMsg.hide()
        
        REPORTW.resize(REPORTW.width(), 160 + changeY)

        ui.edtComment.resize(341, 77)

        ui.edtComment.move(10, 50 + changeY)
        ui.edtMsg.move(10, 135 + changeY)

        ui.btnReport.move(360, 50 + changeY)
        ui.btnCancel.move(360, 100 + changeY)

        ui.btnBefore.move(360, 50 + changeY)
        ui.btnNext.move(405, 50 + changeY)
        ui.btnFolder.move(360, 100 + changeY)
        ui.btnSaveToHistory.move(405, 100 + changeY)

        ui.lblUser.move(360, 135 + changeY)
        ui.btnShowReport.move(400, 135 + changeY)
        ui.btnHelp.move(425, 135 + changeY)
            
    else:
        ui.edtErrorMsg.show()

        REPORTW.resize(REPORTW.width(), 250 + changeY)

        ui.edtComment.resize(431, 77)

        ui.edtComment.move(10, 50 + changeY)
        ui.edtMsg.move(10, 223 + changeY)
        ui.edtErrorMsg.move(10, 137 + changeY)

        ui.btnReport.move(360, 138 + changeY)
        ui.btnCancel.move(360, 188 + changeY)

        ui.btnBefore.move(360, 138 + changeY)
        ui.btnNext.move(405, 138 + changeY)
        ui.btnFolder.move(360, 188 + changeY)
        ui.btnSaveToHistory.move(405, 188 + changeY)

        ui.lblUser.move(360, 223 + changeY)
        ui.btnShowReport.move(400, 223 + changeY)
        ui.btnHelp.move(425, 223 + changeY)


    if not(os.path.isfile(currentImgPath)):
        currentImgPath = os.path.join(s.PATH['img_shelf'], "shelf_report35.png")

    ui.lblReport.setPixmap(QPixmap(QImage(currentImgPath)))
    ui.edtMsg.setText(ui.cbxReport.currentText() + ": " + ui.cbxScript.currentText())


def changed_script():
    script = ui.cbxScript.currentText().replace(' ', '')
    currentImgPath = os.path.join(s.PATH['img_shelf'], "shelf_" + script + "35.png")
    changeY = 30

    if(ui.cbxScript.currentText() == "other"):
        ui.edtScript.show()
        changed_report()
        currentImgPath = os.path.join(s.PATH['img_shelf'], "shelf_default35.png")
        
    else:
        ui.edtScript.hide()     
        changed_report()

    if not(os.path.isfile(currentImgPath)):
        currentImgPath = os.path.join(s.PATH['img_shelf'], "shelf_default35.png")

    ui.lblScript.setPixmap(QPixmap(QImage(currentImgPath)))


def errorMsg_In(event):
    if(ui.edtErrorMsg.toPlainText() == "Error Message"):
        ui.edtErrorMsg.setPlainText("")
        ui.edtErrorMsg.setStyleSheet("color: rgb(255, 255, 255);")
    ui.edtErrorMsg.setCursorWidth(1)


def errorMsg_Out(event):
    if(ui.edtErrorMsg.toPlainText() == ""):
        ui.edtErrorMsg.setPlainText("Error Message")
        ui.edtErrorMsg.setStyleSheet("color: rgb(175, 175, 175);")
    ui.edtErrorMsg.setCursorWidth(0)


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
# FUNCTIONS
#**********************
def saveFile():
    global CURRENT_USER

    dataPath = s.PATH["data_report"] + '\\' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".json" # append .json
    
    if(ui.cbxScript.currentText() == "other"):
        script = ui.edtScript.text()
    else:
        script = ui.cbxScript.currentText()

    if(ui.edtComment.toPlainText() == "Comment"):
        ui.edtComment.setPlainText("")  

    if(ui.edtErrorMsg.toPlainText() == "Error Message"):
        ui.edtErrorMsg.setPlainText("")

    filePath = ""
    # filePath = cmds.file(q=True,sn=True)
    
    report = libReport.Report(user = CURRENT_USER, filePath = filePath, reason = ui.cbxReport.currentText(), script = script, comment = ui.edtComment.toPlainText(), error = ui.edtErrorMsg.toPlainText() )

    libFileService.saveJsonFile(dataPath, report)


def setReports(index = 0):
    global REPORTS, REPORT_INDEX

    reportLength = len(REPORTS) - 1

    ui.cbxReport.clear()
    ui.cbxScript.clear()

    if(reportLength < 0):
        ui.edtMsg.setText("No Reports at the time")
        ui.edtComment.setPlainText("Comment")
        ui.edtErrorMsg.setPlainText("Error Message")
        return

    REPORT_INDEX += index

    if (REPORT_INDEX < 0):
        REPORT_INDEX = reportLength
    elif (REPORT_INDEX > (reportLength)):
        REPORT_INDEX = 0

    currentReport = libReport.Report()
    currentReport = libFileService.loadJsonFile(s.PATH["data_report"] + "\\" + REPORTS[REPORT_INDEX] + ".json")

    ui.cbxReport.addItem(currentReport["reason"])
    ui.cbxScript.addItem(currentReport["script"])

    ui.edtErrorMsg.setPlainText(currentReport["error"]) 
    ui.edtComment.setPlainText(currentReport["comment"]) 

    ui.edtMsg.setText(str(REPORT_INDEX) + ":" + str(reportLength) + " - " + REPORTS[REPORT_INDEX])
    libFunction.changeUserImg(currentReport["user"], ui.lblUser)

#**********************
# START PROZESS
#**********************
def setScript(currentScript = "other"):
    global CURRENT_USER
    CURRENT_USER = os.getenv('username')

    libFunction.changeUserImg(CURRENT_USER, ui.lblUser)

    if not(CURRENT_USER in s.ADMIN):
        ui.btnShowReport.hide()

    ui.cbxReport.addItems(reportList)
    ui.cbxScript.addItems(scriptList)

    ui.edtComment.setPlainText("Comment")
    ui.edtErrorMsg.setPlainText("Error Message")

    tmpIndex = ui.cbxScript.findText(currentScript)
    if(tmpIndex != -1 ):
        ui.cbxScript.setCurrentIndex(tmpIndex)


#**********************
# START UI
#**********************
# if __name__ == "__main__":
def start(currentScript = 'other'):
    global REPORTW

    REPORTW     = QWidget()

    ui.setupUi(REPORTW)

    REPORTW.connect(ui.btnReport, SIGNAL("clicked()"), clicked_report)
    REPORTW.connect(ui.btnCancel, SIGNAL("clicked()"), clicked_cancel)
    REPORTW.connect(ui.btnHelp, SIGNAL("clicked()"), clicked_help)
    REPORTW.connect(ui.btnShowReport, SIGNAL("clicked()"), clicked_showReport)    

    REPORTW.connect(ui.btnBefore, SIGNAL("clicked()"), clicked_before)
    REPORTW.connect(ui.btnNext, SIGNAL("clicked()"), clicked_next)
    REPORTW.connect(ui.btnSaveToHistory, SIGNAL("clicked()"), clicked_saveToHistory)
    REPORTW.connect(ui.btnFolder, SIGNAL("clicked()"), clicked_folder)

    REPORTW.connect(ui.cbxReport, SIGNAL("currentIndexChanged(const QString&)"), changed_report)
    REPORTW.connect(ui.cbxScript, SIGNAL("currentIndexChanged(const QString&)"), changed_script)
    
    ui.edtErrorMsg.focusInEvent = errorMsg_In
    ui.edtErrorMsg.focusOutEvent = errorMsg_Out    

    ui.edtComment.focusInEvent = comment_In
    ui.edtComment.focusOutEvent = comment_Out

    # REPORTW.setAttribute(Qt.WA_DeleteOnClose)

    ui.btnBefore.hide()
    ui.btnNext.hide() 
    ui.btnSaveToHistory.hide() 
    ui.btnFolder.hide() 

    setScript(currentScript)

    REPORTW.show()
    # sys.exit(app.exec_())