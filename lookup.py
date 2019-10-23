# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lookup.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette,QBrush,QPixmap

class Ui_MainWindow2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow2,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 560)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(189, 100, 71, 30))
        font = QtGui.QFont()
        font.setFamily("华文琥珀")
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(270, 100, 221, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(520, 100, 60, 30))
        font = QtGui.QFont()
        font.setFamily("华文细黑")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(190, 150, 400, 300))
        self.label_2.setObjectName("label_2")
        self.label_2.setWordWrap(True)
        self.label_2.setAlignment(Qt.AlignTop)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 460, 75, 31))
        font = QtGui.QFont()
        font.setFamily("华文细黑")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.mysearchword)
        MainWindow.setStyleSheet("#MainWindow{border-image:url(background.jpg);}")







    def mysearchword(self):
        word_to_search = self.lineEdit.text()
        #这里的代码需要根据word_to_search查找相关的解释
        search_result = "我们的快乐"

        #返回结果为search_result
        self.label_2.setText(search_result)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "单词搜索"))
        self.label.setText(_translate("MainWindow", "输入单词："))
        self.pushButton.setText(_translate("MainWindow", "确定"))
        self.pushButton_2.setText(_translate("MainWindow", "退出"))

