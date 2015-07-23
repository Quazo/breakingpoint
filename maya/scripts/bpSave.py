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

from scripts.ui import bpSave
#from ui import bpSave

#**********************
# VARIABLE
#**********************
VERSION         = "v0.02"
CURRENT_USER    = os.getenv('username')








#**********************
# FUNKTIONS
#**********************
def clicked_btnSave():
	print ("clicked_btnSave")


def clicked_btnCancel():
	print ("clicked_btnCancel")


def clicked_btnUser():
	print ("clicked_btnUser")


def clicked_btnHelp():
	print ("clicked_btnHelp")
    #webbrowser.open("https://www.filmakademie.de/wiki/display/AISPD/BREAKINGPOINT+-+Pipeline")

def clicked_btnEmail():
	print ("clicked_btnEmail")


def clicked_btnMessage():
	print ("clicked_btnMessage")


def changed_publish():
	print ("changed_publish")





#**********************
# START PROZESS
#**********************
def setSave():
    print("setSave")

    global CURRENT_USER
    CURRENT_USER = os.getenv('username')


#**********************
# RUN DOS RUN
#**********************
# app = QApplication(sys.argv)
bpS     = QWidget()
ui   	= bpSave.Ui_bpSave()



def main():
    ui.setupUi(bpS)
    # ui.setupUi(bpSave)

    ui.lblVersion.setText(VERSION)
    
    bpS.connect(ui.btnSave, SIGNAL("clicked()"), clicked_btnSave)
    bpS.connect(ui.btnCancel, SIGNAL("clicked()"), clicked_btnCancel)
    bpS.connect(ui.btnHelp, SIGNAL("clicked()"), clicked_btnHelp)
    bpS.connect(ui.btnEmail, SIGNAL("clicked()"), clicked_btnEmail)
    bpS.connect(ui.btnMessage, SIGNAL("clicked()"), clicked_btnMessage)

    ui.cbxPublish.toggled.connect(changed_publish)


    # ui.edtQuestionNr.returnPressed.connect(changed_questionNr)
    # ui.edtQuestionNr.lostFocus.connect(changed_questionNr)

    bpS.show()

    
    #sys.exit(app.exec_())

    sys.exit()

if __name__ == "__main__":
    ui.setupUi(bpS)
    # ui.setupUi(bpSave)

    ui.lblVersion.setText(VERSION)
    
    bpS.connect(ui.btnSave, SIGNAL("clicked()"), clicked_btnSave)
    bpS.connect(ui.btnCancel, SIGNAL("clicked()"), clicked_btnCancel)
    bpS.connect(ui.btnHelp, SIGNAL("clicked()"), clicked_btnHelp)
    bpS.connect(ui.btnEmail, SIGNAL("clicked()"), clicked_btnEmail)
    bpS.connect(ui.btnMessage, SIGNAL("clicked()"), clicked_btnMessage)

    ui.cbxPublish.toggled.connect(changed_publish)


    # ui.edtQuestionNr.returnPressed.connect(changed_questionNr)
    # ui.edtQuestionNr.lostFocus.connect(changed_questionNr)

    bpS.show()

    
    #sys.exit(app.exec_())

    sys.exit()