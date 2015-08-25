# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../_sandbox/maya/scripts/ui/qt/save.ui'
#
# Created: Tue Aug 25 13:35:49 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_save(object):
    def setupUi(self, save):
        save.setObjectName("save")
        save.resize(613, 325)
        save.setMinimumSize(QtCore.QSize(613, 325))
        save.setMaximumSize(QtCore.QSize(613, 325))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setWeight(75)
        font.setBold(True)
        save.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/shelf/img/shelf/shelf_save35.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        save.setWindowIcon(icon)
        save.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(31, 31, 31);")
        self.lblImage = QtGui.QLabel(save)
        self.lblImage.setGeometry(QtCore.QRect(10, 6, 416, 171))
        self.lblImage.setText("")
        self.lblImage.setPixmap(QtGui.QPixmap(":/shot/img/shot/000.png"))
        self.lblImage.setScaledContents(True)
        self.lblImage.setObjectName("lblImage")
        self.cbxPublish = QtGui.QCheckBox(save)
        self.cbxPublish.setGeometry(QtCore.QRect(520, 197, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.cbxPublish.setFont(font)
        self.cbxPublish.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cbxPublish.setStyleSheet("")
        self.cbxPublish.setTristate(False)
        self.cbxPublish.setObjectName("cbxPublish")
        self.edtSavePath = QtGui.QLineEdit(save)
        self.edtSavePath.setGeometry(QtCore.QRect(85, 195, 361, 26))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.edtSavePath.setFont(font)
        self.edtSavePath.setReadOnly(True)
        self.edtSavePath.setObjectName("edtSavePath")
        self.btnFolder = QtGui.QPushButton(save)
        self.btnFolder.setGeometry(QtCore.QRect(485, 196, 24, 24))
        self.btnFolder.setStyleSheet("background-color: rgb(56, 56, 56);")
        self.btnFolder.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/btn/img/btn/folderBtn24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFolder.setIcon(icon1)
        self.btnFolder.setIconSize(QtCore.QSize(22, 22))
        self.btnFolder.setObjectName("btnFolder")
        self.btnSave = QtGui.QPushButton(save)
        self.btnSave.setGeometry(QtCore.QRect(520, 231, 81, 31))
        self.btnSave.setStyleSheet("background-color: rgb(56, 56, 56);")
        self.btnSave.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/btn/img/btn/btnSave.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSave.setIcon(icon2)
        self.btnSave.setIconSize(QtCore.QSize(32, 32))
        self.btnSave.setObjectName("btnSave")
        self.btnCancel = QtGui.QPushButton(save)
        self.btnCancel.setGeometry(QtCore.QRect(520, 271, 81, 23))
        self.btnCancel.setStyleSheet("background-color: rgb(56, 56, 56);")
        self.btnCancel.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/btn/img/btn/denialBtn24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCancel.setIcon(icon3)
        self.btnCancel.setIconSize(QtCore.QSize(23, 23))
        self.btnCancel.setObjectName("btnCancel")
        self.edtComment = QtGui.QPlainTextEdit(save)
        self.edtComment.setGeometry(QtCore.QRect(10, 231, 501, 61))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.edtComment.setFont(font)
        self.edtComment.setStyleSheet("color: rgb(168, 168, 168);")
        self.edtComment.setFrameShape(QtGui.QFrame.Box)
        self.edtComment.setFrameShadow(QtGui.QFrame.Plain)
        self.edtComment.setLineWidth(1)
        self.edtComment.setMidLineWidth(0)
        self.edtComment.setBackgroundVisible(False)
        self.edtComment.setCenterOnScroll(False)
        self.edtComment.setObjectName("edtComment")
        self.edtMetaData = QtGui.QPlainTextEdit(save)
        self.edtMetaData.setGeometry(QtCore.QRect(440, 41, 161, 131))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(9)
        font.setWeight(50)
        font.setBold(False)
        self.edtMetaData.setFont(font)
        self.edtMetaData.setFrameShape(QtGui.QFrame.Box)
        self.edtMetaData.setFrameShadow(QtGui.QFrame.Plain)
        self.edtMetaData.setLineWidth(1)
        self.edtMetaData.setReadOnly(True)
        self.edtMetaData.setObjectName("edtMetaData")
        self.btnHelp = QtGui.QPushButton(save)
        self.btnHelp.setGeometry(QtCore.QRect(585, 301, 16, 16))
        self.btnHelp.setStyleSheet("background-color: rgb(56, 56, 56);")
        self.btnHelp.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/btn/img/btn/helpBtn24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnHelp.setIcon(icon4)
        self.btnHelp.setIconSize(QtCore.QSize(16, 16))
        self.btnHelp.setObjectName("btnHelp")
        self.btnReport = QtGui.QPushButton(save)
        self.btnReport.setGeometry(QtCore.QRect(560, 301, 16, 16))
        self.btnReport.setStyleSheet("background-color: rgb(56, 56, 56);")
        self.btnReport.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/btn/img/btn/mailBtn24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnReport.setIcon(icon5)
        self.btnReport.setIconSize(QtCore.QSize(16, 16))
        self.btnReport.setObjectName("btnReport")
        self.btnOpenFolder = QtGui.QPushButton(save)
        self.btnOpenFolder.setGeometry(QtCore.QRect(495, 301, 16, 16))
        self.btnOpenFolder.setStyleSheet("background-color: rgb(56, 56, 56);")
        self.btnOpenFolder.setText("")
        self.btnOpenFolder.setIcon(icon1)
        self.btnOpenFolder.setIconSize(QtCore.QSize(14, 14))
        self.btnOpenFolder.setObjectName("btnOpenFolder")
        self.line = QtGui.QFrame(save)
        self.line.setGeometry(QtCore.QRect(10, 176, 596, 20))
        self.line.setStyleSheet("")
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.lblShotNr = QtGui.QLabel(save)
        self.lblShotNr.setGeometry(QtCore.QRect(280, 151, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lblShotNr.setFont(font)
        self.lblShotNr.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblShotNr.setStyleSheet("background-color: \'transparent\';")
        self.lblShotNr.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblShotNr.setObjectName("lblShotNr")
        self.lblBanner = QtGui.QLabel(save)
        self.lblBanner.setGeometry(QtCore.QRect(400, 11, 24, 24))
        self.lblBanner.setStyleSheet("background-color: \'transparent\';")
        self.lblBanner.setText("")
        self.lblBanner.setPixmap(QtGui.QPixmap(":/banner/img/banner/LIGHT.png"))
        self.lblBanner.setScaledContents(True)
        self.lblBanner.setObjectName("lblBanner")
        self.lblVersion = QtGui.QLabel(save)
        self.lblVersion.setGeometry(QtCore.QRect(15, 161, 46, 13))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setWeight(75)
        font.setBold(True)
        self.lblVersion.setFont(font)
        self.lblVersion.setStyleSheet("background-color: \'transparent\';")
        self.lblVersion.setObjectName("lblVersion")
        self.cbxUser = QtGui.QComboBox(save)
        self.cbxUser.setGeometry(QtCore.QRect(470, 10, 131, 22))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.cbxUser.setFont(font)
        self.cbxUser.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cbxUser.setStyleSheet("background-color: rgb(56, 56, 56);")
        self.cbxUser.setEditable(False)
        self.cbxUser.setInsertPolicy(QtGui.QComboBox.InsertAtBottom)
        self.cbxUser.setFrame(False)
        self.cbxUser.setObjectName("cbxUser")
        self.lblUser = QtGui.QLabel(save)
        self.lblUser.setGeometry(QtCore.QRect(440, 6, 30, 30))
        self.lblUser.setStyleSheet("background-color: \'transparent\';")
        self.lblUser.setText("")
        self.lblUser.setPixmap(QtGui.QPixmap(":/user/img/user/_default.png"))
        self.lblUser.setScaledContents(True)
        self.lblUser.setObjectName("lblUser")
        self.lblStatus = QtGui.QLabel(save)
        self.lblStatus.setGeometry(QtCore.QRect(13, 193, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.lblStatus.setFont(font)
        self.lblStatus.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblStatus.setObjectName("lblStatus")
        self.lblSlash = QtGui.QLabel(save)
        self.lblSlash.setGeometry(QtCore.QRect(72, 193, 10, 31))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.lblSlash.setFont(font)
        self.lblSlash.setTextFormat(QtCore.Qt.AutoText)
        self.lblSlash.setObjectName("lblSlash")
        self.btnVersionUp = QtGui.QPushButton(save)
        self.btnVersionUp.setGeometry(QtCore.QRect(455, 196, 21, 12))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setWeight(75)
        font.setBold(True)
        self.btnVersionUp.setFont(font)
        self.btnVersionUp.setStyleSheet("background-color: rgb(56, 56, 56);")
        self.btnVersionUp.setObjectName("btnVersionUp")
        self.btnVersionDown = QtGui.QPushButton(save)
        self.btnVersionDown.setGeometry(QtCore.QRect(455, 208, 21, 12))
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setWeight(75)
        font.setBold(True)
        self.btnVersionDown.setFont(font)
        self.btnVersionDown.setStyleSheet("background-color: rgb(56, 56, 56);")
        self.btnVersionDown.setObjectName("btnVersionDown")
        self.edtPath = QtGui.QLineEdit(save)
        self.edtPath.setEnabled(True)
        self.edtPath.setGeometry(QtCore.QRect(10, 300, 476, 18))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.edtPath.setFont(font)
        self.edtPath.setFrame(False)
        self.edtPath.setReadOnly(True)
        self.edtPath.setObjectName("edtPath")

        self.retranslateUi(save)
        QtCore.QMetaObject.connectSlotsByName(save)

    def retranslateUi(self, save):
        save.setWindowTitle(QtGui.QApplication.translate("save", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.cbxPublish.setText(QtGui.QApplication.translate("save", "PUBLISH", None, QtGui.QApplication.UnicodeUTF8))
        self.edtSavePath.setText(QtGui.QApplication.translate("save", "140_LIGHT_v003_ar.ma", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSave.setShortcut(QtGui.QApplication.translate("save", "Return", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setShortcut(QtGui.QApplication.translate("save", "Esc", None, QtGui.QApplication.UnicodeUTF8))
        self.edtComment.setPlainText(QtGui.QApplication.translate("save", "Comment", None, QtGui.QApplication.UnicodeUTF8))
        self.edtMetaData.setPlainText(QtGui.QApplication.translate("save", "Resolution:    2048 x 1152\n"
"\n"
"FPS:    25 FPS\n"
"\n"
"Frames:    1001 - ", None, QtGui.QApplication.UnicodeUTF8))
        self.lblShotNr.setText(QtGui.QApplication.translate("save", "140", None, QtGui.QApplication.UnicodeUTF8))
        self.lblVersion.setText(QtGui.QApplication.translate("save", "v.0.01", None, QtGui.QApplication.UnicodeUTF8))
        self.lblStatus.setText(QtGui.QApplication.translate("save", "WORK", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSlash.setText(QtGui.QApplication.translate("save", "|", None, QtGui.QApplication.UnicodeUTF8))
        self.btnVersionUp.setText(QtGui.QApplication.translate("save", "↑", None, QtGui.QApplication.UnicodeUTF8))
        self.btnVersionDown.setText(QtGui.QApplication.translate("save", "↓", None, QtGui.QApplication.UnicodeUTF8))
        self.edtPath.setText(QtGui.QApplication.translate("save", "P:/2_production/2_shots/140_magneto/4_LIGHT/WORK/140_LIGHT_v003_ar.ma", None, QtGui.QApplication.UnicodeUTF8))

import maya_rc
