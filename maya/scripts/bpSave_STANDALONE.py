#*************************************************************
# title:        bpSave
#
# content:      automatic save work and publish files
#
# dependencies: "PYTHONPATH=%SOFTWARE_PATH%/maya;%PYTHONPATH%"
#
# author:       Alexander Richter 
# email:        alexander.richter@filmakademie.de
#*************************************************************
# -*- coding: utf-8 -*-

import os, sys
import subprocess
import shutil
import webbrowser

from PySide.QtGui import *
from PySide.QtCore import *

#from scripts.ui import bpSave
from ui import bpSave

sys.path.append('../../../')
import settings as s
sys.path.append(s.PATH['lib'])
import libMessageBox as msg


#**********************
# VARIABLE
#**********************
VERSION         = "v0.02"
CURRENT_USER    = os.getenv('username')

FILE_NAME		= ['140', 'SHD', 'v001', 'ar']
FILE_FORMAT		= 'ma'
SAVE_PATH		= ''

SHOT_DEFAULT	= '000'




#**********************
# SETTINGS
#**********************



#**********************
# CLICKED_TRIGGER
#**********************
def clicked_btnSave():
	print ("clicked_btnSave")


def clicked_btnCancel():
	print ("clicked_btnCancel")
	bpS.close() 


def clicked_btnUser():
	print ("clicked_btnUser")


def clicked_btnHelp():
	print ("clicked_btnHelp")
	webbrowser.open("https://www.filmakademie.de/wiki/display/AISPD/BREAKINGPOINT+-+Pipeline")


def clicked_btnEmail():
	print ("clicked_btnEmail")


def clicked_btnMessage():
	print ("clicked_btnMessage")


def clicked_btnMsgFolder():
	print("clicked_btnMsgFolder")
	msg.folderMsgBox(bpS, "Maya Files (*.mb *.ma)")


def changed_publish():
	print ("changed_publish")

	ui.edtComment.setEnabled(True)
	
	ui.edtComment.setEnabled(False)
	



#**********************
# CHANGED_TRIGGER
#**********************
def changed_user():
	print("user changed")
	
	global FILE_FORMAT
	
	# CHANGE USER IMG
	changeUserImg(ui.cbxUser.currentText())

	# CHANGE USER TOKEN
	FILE_NAME[3] = ui.cbxUser.currentText()[:2]
	ui.edtSavePath.setText(('_').join(FILE_NAME) + '.' + FILE_FORMAT)


#**********************
# FUNCTIONS
#**********************
def changeUserImg(user):
	currentImgPath = os.path.join(s.PATH['img'], 'user', user + ".png")
	if(os.path.isfile(currentImgPath)):
		ui.lblUser.setPixmap(QPixmap(QImage(currentImgPath)))
	else:
		ui.lblUser.setPixmap(QPixmap(QImage(os.path.join(s.PATH['img'], 'user', "_default.png"))))


def initPath():
	global FILE_NAME, FILE_FORMAT, SAVE_PATH

	SAVE_PATH 		= "P:/_pipeline" 
	currentFile 	= "women_SHD_v001_ml_geht.ma"

	(FILE_NAME, FILE_FORMAT) = currentFile.split('.')

	if (len(FILE_NAME.split('_')) == 5):
		(shot, task, version, user, comment) = FILE_NAME.split('_')
	else:
		(shot, task, version, user) = FILE_NAME.split('_')

	user = ui.cbxUser.currentText()[:2]

	if('v' in version): 
		version = version.replace('v', '')
		version = 'v' + str('{0:03d}'.format(int(version) + 1))

	FILE_NAME = [shot, task, version, user]

	ui.lblBanner.setPixmap(QPixmap(QImage(os.path.join(s.PATH['img'], 'banner', task + ".png"))))
	
	imgShotPath = os.path.join(s.PATH['img'], 'shot', shot + ".png")
	if not os.path.isfile(imgShotPath):	
		imgShotPath = os.path.join(s.PATH['img'], 'shot', SHOT_DEFAULT + ".png")

	ui.lblImage.setPixmap(QPixmap(QImage(imgShotPath)))

	ui.edtSavePath.setText(('_').join(FILE_NAME) + '.' + FILE_FORMAT)
	ui.lblShotNr.setText(shot)


#**********************
# START PROZESS
#**********************
def setSave():
	print("setSave")

	global CURRENT_USER
	CURRENT_USER = os.getenv('username')

	userList = os.listdir(s.PATH['data_user'])
	ui.cbxUser.addItems(sorted(userList))
	
	if(os.getenv('username') in userList):      
		ui.cbxUser.setCurrentIndex(ui.cbxUser.findText(os.getenv('username')))

	#setLOGO IMG
	initPath()

#**********************
# RUN DOS RUN
#**********************
app     = QApplication(sys.argv)
bpS     = QWidget()
ui   	= bpSave.Ui_bpSave()




if __name__ == "__main__":
	ui.setupUi(bpS)
	# ui.setupUi(bpSave)

	ui.lblVersion.setText(VERSION)
	
	bpS.connect(ui.btnSave, SIGNAL("clicked()"), clicked_btnSave)
	bpS.connect(ui.btnCancel, SIGNAL("clicked()"), clicked_btnCancel)
	bpS.connect(ui.btnHelp, SIGNAL("clicked()"), clicked_btnHelp)
	bpS.connect(ui.btnEmail, SIGNAL("clicked()"), clicked_btnEmail)
	bpS.connect(ui.btnMessage, SIGNAL("clicked()"), clicked_btnMessage)
	bpS.connect(ui.btnFolder, SIGNAL("clicked()"), clicked_btnMsgFolder)

	bpS.connect(ui.cbxUser, SIGNAL("currentIndexChanged(const QString&)"), changed_user)

	ui.btnMessage.hide()
	ui.btnEmail.hide()


	ui.cbxPublish.toggled.connect(changed_publish)
	setSave()

	# ui.edtQuestionNr.returnPressed.connect(changed_questionNr)
	# ui.edtQuestionNr.lostFocus.connect(changed_questionNr)

	bpS.show()

	
	sys.exit(app.exec_())

	#sys.exit()