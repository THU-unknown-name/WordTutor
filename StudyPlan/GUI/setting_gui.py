# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting_gui.ui'
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
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 70, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setStyleSheet('''
                            QLabel{color:white;  font-weight:700;
                                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                        ''')
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(300, 70, 91, 30))
        self.textBrowser.setObjectName("textBrowser")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(400, 70, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet('''
                                    QLabel{color:white;  font-weight:700;
                                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                ''')
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(480, 65, 111, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet('''
                                           QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                                               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                       ''')
        self.pushButton.setIcon(QtGui.QIcon('./eraser.png'))
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(480, 160, 20, 301))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(160, 160, 431, 301))
        self.listWidget.setAutoFillBackground(True)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setProperty("isWrapping", False)
        self.listWidget.setWordWrap(True)
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        self.exButton = QtWidgets.QPushButton(self.centralwidget)  # 退出
        self.exButton.setGeometry(QtCore.QRect(320, 470, 150, 60))
        self.exButton.setObjectName("exButton")
        self.exButton.setIcon(QtGui.QIcon('./exit.jpg'))
        self.exButton.setStyleSheet('''
                                   QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                               ''')
        self.exButton.clicked.connect(self.close)
        self.pushButton.setIcon(QtGui.QIcon('./eraser.png'))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.modify_num)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "当前学习计划："))
        self.label_2.setText(_translate("MainWindow", "个/天"))
        self.pushButton.setText(_translate("MainWindow", "修改"))
        self.exButton.setText(_translate("MainWindow", "退出"))
