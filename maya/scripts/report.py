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


import os, sys
import shutil
import webbrowser

from PySide.QtGui import *
from PySide.QtCore import *

# from scripts.ui import reportError
from ui import report

# import maya.cmds as cmds
# import maya.mel as mel

sys.path.append('../../../')
import settings as s
sys.path.append(s.PATH['lib'])
import libMessageBox as msg


#**********************
# RUN DOS RUN
#**********************
app 		= QApplication(sys.argv)
reportW   	= QWidget()
ui   		= report.Ui_report()



#**********************
# VARIABLE
#**********************
CURRENT_USER 	= ""

reportList		= ["Bug", "Suggestion"]
scriptList 		= ["Save", "Reference SHD_SCENE", "Combine SHD and Model", "Alembic Export", "Alembic Import", "other"]


#**********************
# CLICKED_TRIGGER
#**********************
def clicked_btnReport():
    print ("REPORT")
    #saveFile()
    reportW.close() 


def clicked_btnCancel():
    reportW.close()


def clicked_btnHelp():
    webbrowser.open(s.LINK["software"])

#**********************
# CHANGED_TRIGGER
#**********************
def changed_report():
	print ("changed_report")
	
	currentImgPath = os.path.join(s.PATH['img_shelf'], "shelf_" + ui.cbxReport.currentText() + "35.png")
	changeY = 0#123
	resizeY = 35

	if(ui.cbxReport.currentText() == "Suggestion"):

		ui.edtErrorMsg.hide()
		
		if(ui.cbxScript.currentText() == "other"):
			changeY = 30 

		reportW.resize(reportW.width(), 160 + changeY)

		ui.edtComment.resize(341, 77)

		ui.edtComment.move(10, 50 + changeY)
		ui.edtMsg.move(10, 135 + changeY)

		ui.btnReport.move(360, 50 + changeY)
		ui.btnCancel.move(360, 100 + changeY)

		ui.lblUser.move(360, 135 + changeY)
		ui.btnHelp.move(425, 135 + changeY)
			
	else:
		ui.edtErrorMsg.show()

		if(ui.cbxScript.currentText() == "other"):
			changeY = 30 
		
		reportW.resize(reportW.width(), 250 + changeY)

		ui.edtComment.resize(431, 77)

		ui.edtComment.move(10, 50 + changeY)
		ui.edtMsg.move(10, 223 + changeY)
		ui.edtErrorMsg.move(10, 137 + changeY)

		ui.btnReport.move(360, 138 + changeY)
		ui.btnCancel.move(360, 188 + changeY)

		ui.lblUser.move(360, 223 + changeY)
		ui.btnHelp.move(425, 223 + changeY)


	if not(os.path.isfile(currentImgPath)):
		currentImgPath = os.path.join(s.PATH['img_shelf'], "shelf_report35.png")

	ui.lblReport.setPixmap(QPixmap(QImage(currentImgPath)))


def changed_script():
	print ("changed_script")
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


#**********************
# FUNCTIONS
#**********************
def changeUserImg(user):
    currentImgPath = os.path.join(s.PATH['img_user'], user + ".png")

    if not(os.path.isfile(currentImgPath)):
        currentImgPath = os.path.join(s.PATH['img_user'], "_default.png")

    ui.lblUser.setPixmap(QPixmap(QImage(currentImgPath)))


#**********************
# START PROZESS
#**********************
def setScript(currentScript = 'other'):
	global CURRENT_USER
	CURRENT_USER = os.getenv('username')

	changeUserImg(CURRENT_USER)

	ui.cbxReport.addItems(reportList)
	ui.cbxScript.addItems(scriptList)

	tmpIndex = ui.cbxScript.findText(currentScript)
	if(tmpIndex != -1 ):
		ui.cbxScript.setCurrentIndex(tmpIndex)



#**********************
# START UI
#**********************
if __name__ == "__main__":
#def start(currentScript = 'other'):
	ui.setupUi(reportW)

	reportW.connect(ui.btnReport, SIGNAL("clicked()"), clicked_btnReport)
	reportW.connect(ui.btnCancel, SIGNAL("clicked()"), clicked_btnCancel)
	reportW.connect(ui.btnHelp, SIGNAL("clicked()"), clicked_btnHelp)

	reportW.connect(ui.cbxReport, SIGNAL("currentIndexChanged(const QString&)"), changed_report)
	reportW.connect(ui.cbxScript, SIGNAL("currentIndexChanged(const QString&)"), changed_script)

    # ui.btnMessage.hide()
    # ui.btnEmail.hide()

    # ui.cbxPublish.toggled.connect(changed_publish)  
    # ui.edtSavePath.textChanged.connect(changed_edtSavePath)

 	setScript()

	reportW.show()
	sys.exit(app.exec_())