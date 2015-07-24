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
#import maya.cmds as cmds

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
SAVE_DIR		= ''

SHOT_DEFAULT	= '000'




#**********************
# SETTINGS
#**********************



#**********************
# CLICKED_TRIGGER
#**********************
def clicked_btnSave():
	print ("clicked_btnSave")
	saveFile()

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


def clicked_btnVersionUp():
	print("Version Up")
	global FILE_NAME

	if('v' in FILE_NAME[2]): 
		FILE_NAME[2] = FILE_NAME[2].replace('v', '')
		FILE_NAME[2] = 'v' + str('{0:03d}'.format(int(FILE_NAME[2]) + 1))

	ui.edtSavePath.setText(('_').join(FILE_NAME) + '.' + FILE_FORMAT)


def clicked_btnVersionDown():
	print ("Version Down")
	global FILE_NAME

	if('v' in FILE_NAME[2] and FILE_NAME[2] != "v000"): 
		FILE_NAME[2] = FILE_NAME[2].replace('v', '')
		FILE_NAME[2] = 'v' + str('{0:03d}'.format(int(FILE_NAME[2]) - 1))

	ui.edtSavePath.setText(('_').join(FILE_NAME) + '.' + FILE_FORMAT)


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
	ui.lblPath.setText(os.path.join(SAVE_DIR, ui.edtSavePath.text()))


def changed_publish():
	print ("changed_publish")
	global SAVE_DIR

	if(ui.cbxPublish.isChecked()):
		ui.edtComment.setEnabled(False)
		ui.edtComment.setPlainText('')
		ui.edtSavePath.setText(('_').join(FILE_NAME[:2]) + '.' + FILE_FORMAT)

		ui.btnVersionUp.setEnabled(False)
		ui.btnVersionDown.setEnabled(False)

		ui.lblStatus.setText("PUBLISH")

		if('WORK' in SAVE_DIR):
			SAVE_DIR = SAVE_DIR.replace('WORK', 'PUBLISH')
		else:
			ui.lblPath.setText('WORK MISSING: There is no WORK in your file path')
		
	else:
		ui.edtComment.setEnabled(True)
		ui.lblStatus.setText("WORK")
		ui.edtSavePath.setText(('_').join(FILE_NAME) + '.' + FILE_FORMAT)
		
		ui.btnVersionUp.setEnabled(True)
		ui.btnVersionDown.setEnabled(True)

		if('PUBLISH' in SAVE_DIR):
			SAVE_DIR = SAVE_DIR.replace('PUBLISH', 'WORK')
		else:
			ui.lblPath.setText('PUBLISH MISSING: There is no PUBLISH in your file path')

	ui.lblPath.setText(os.path.join(SAVE_DIR, ui.edtSavePath.text()))


def changed_edtSavePath():
	print ("change")
	currentFile 	= ui.lblPath.text()

	if(len(currentFile.split('.')) > 1):
		(FILE_NAME, FILE_FORMAT) = currentFile.split('.')

		if (len(FILE_NAME.split('_')) > 4):
			FILE_NAME = FILE_NAME.split('_')
		else:
			ui.lblPath.setText('NAME CONVENTION: Not conform name setting - 010_SHD_v001_ar.ma')

	ui.lblPath.setText(os.path.join(SAVE_DIR, ui.edtSavePath.text()))


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
	global FILE_NAME, FILE_FORMAT, SAVE_DIR

	SAVE_DIR 		= "H:\\bp\\140\\3_SHD\WORK"     # os.path.dirname(cmds.file(q=True,sn=True))
	currentFile 	= "140_SHD_v001_ml_geht.ma"		# os.path.basename(cmds.file(q=True,sn=True))

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

	ui.lblPath.setText(os.path.join(SAVE_DIR, ui.edtSavePath.text()))


def saveFile():
	global SAVE_DIR, FILE_FORMAT, FILE_NAME


	if('PUBLISH' in SAVE_DIR):
			SAVE_DIR = SAVE_DIR.replace('PUBLISH', 'WORK')

	# SAVE FILE:
	tmpSavePath = os.path.join(SAVE_DIR, ('_').join(FILE_NAME) + '.' + FILE_FORMAT)
	
	# cmds.file( rename=('_').join(FILE_NAME))
	# cmds.file( save=True, type='mayaAscii' )

	# with open(tmpSavePath, 'w') as outfile:
	# 	outfile.write('CONTENT')	

	print (tmpSavePath)

	if(ui.cbxPublish.isChecked()):
		print ("PUBLISH")

		# COPY 
		tmpCopyWork = os.path.join(SAVE_DIR, ('_').join(FILE_NAME) + '_PUBLISH' + '.' + FILE_FORMAT)
		shutil.copy(tmpSavePath, tmpCopyWork)
		print (tmpCopyWork)
		
		if('WORK' in SAVE_DIR):
			SAVE_DIR = SAVE_DIR.replace('WORK', 'PUBLISH')

		# COPY
		tmpCopyPublish = os.path.join(SAVE_DIR, ('_').join(FILE_NAME[:2]) + '.' + FILE_FORMAT)
		shutil.copy(tmpSavePath, tmpCopyPublish)
		print (tmpCopyPublish)


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
	bpS.connect(ui.btnVersionUp, SIGNAL("clicked()"), clicked_btnVersionUp)
	bpS.connect(ui.btnVersionDown, SIGNAL("clicked()"), clicked_btnVersionDown)

	bpS.connect(ui.cbxUser, SIGNAL("currentIndexChanged(const QString&)"), changed_user)

	ui.btnMessage.hide()
	ui.btnEmail.hide()

	ui.cbxPublish.toggled.connect(changed_publish)	
	ui.edtSavePath.textChanged.connect(changed_edtSavePath)

	setSave()

	# ui.edtQuestionNr.returnPressed.connect(changed_questionNr)
	# ui.edtQuestionNr.lostFocus.connect(changed_questionNr)

	bpS.show()

	
	sys.exit(app.exec_())

	#sys.exit()