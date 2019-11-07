# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recite_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_no = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_no.setGeometry(QtCore.QRect(510, 380, 161, 61))
        self.pushButton_no.setObjectName("pushButton_no")
        self.pushButton_yes = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_yes.setGeometry(QtCore.QRect(130, 380, 171, 71))
        self.pushButton_yes.setMouseTracking(False)
        self.pushButton_yes.setObjectName("pushButton_yes")
        self.textBrowser_word = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_word.setGeometry(QtCore.QRect(210, 120, 381, 211))
        self.textBrowser_word.setObjectName("textBrowser_word")
        self.pushButton_revoke = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_revoke.setEnabled(True)
        self.pushButton_revoke.setGeometry(QtCore.QRect(320, 380, 171, 71))
        self.pushButton_revoke.setObjectName("pushButton_revoke")
        self.pushButton_next = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_next.setGeometry(QtCore.QRect(320, 470, 171, 71))
        self.pushButton_next.setObjectName("pushButton_next")
        self.label_stop_showing = QtWidgets.QLabel(self.centralwidget)
        self.label_stop_showing.setGeometry(QtCore.QRect(350, 350, 111, 21))
        self.label_stop_showing.setObjectName("label_stop_showing")
        self.label_show_again = QtWidgets.QLabel(self.centralwidget)
        self.label_show_again.setGeometry(QtCore.QRect(350, 340, 111, 16))
        self.label_show_again.setObjectName("label_show_again")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton_yes.clicked.connect(self.pushButton_yes.hide)
        self.pushButton_yes.clicked.connect(self.pushButton_no.hide)
        self.pushButton_no.clicked.connect(self.pushButton_no.hide)
        self.pushButton_no.clicked.connect(self.pushButton_yes.hide)
        self.pushButton_yes.clicked.connect(self.pushButton_revoke.show)
        self.pushButton_yes.clicked.connect(self.pushButton_next.show)
        self.pushButton_no.clicked.connect(self.pushButton_next.show)
        self.pushButton_yes.clicked.connect(MainWindow.show_exp)
        self.pushButton_no.clicked.connect(MainWindow.show_exp)
        self.pushButton_yes.clicked.connect(self.label_stop_showing.show)
        self.pushButton_no.clicked.connect(self.label_show_again.show)
        self.pushButton_revoke.clicked.connect(self.label_show_again.show)
        self.pushButton_revoke.clicked.connect(self.label_stop_showing.hide)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_no.setText(_translate("MainWindow", "没记住"))
        self.pushButton_yes.setText(_translate("MainWindow", "记住了"))
        self.textBrowser_word.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.SF NS Text\'; font-size:36pt;\">Word</span></p></body></html>"))
        self.pushButton_revoke.setText(_translate("MainWindow", "撤销"))
        self.pushButton_next.setText(_translate("MainWindow", "下一个"))
        self.label_stop_showing.setText(_translate("MainWindow", "今日不再安排学习"))
        self.label_show_again.setText(_translate("MainWindow", "今日继续安排学习"))
