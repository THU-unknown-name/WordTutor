# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recite_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from . import congrats


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_no = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_no.setGeometry(QtCore.QRect(510, 380, 161, 50))
        self.pushButton_no.setObjectName("pushButton_no")
        self.pushButton_yes = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_yes.setGeometry(QtCore.QRect(130, 380, 171, 50))
        self.pushButton_yes.setIcon(QtGui.QIcon('./exit.jpg'))
        self.pushButton_no.setIcon(QtGui.QIcon('./exit.jpg'))
        self.pushButton_yes.setMouseTracking(False)
        self.pushButton_yes.setStyleSheet('''
                                  QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                                      font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                              ''')
        self.pushButton_no.setStyleSheet('''
                                         QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                                             font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                     ''')
        self.pushButton_yes.setObjectName("pushButton_yes")


        self.pushButton_revoke = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_revoke.setEnabled(True)
        self.pushButton_revoke.setGeometry(QtCore.QRect(320, 380, 171, 30))
        self.pushButton_revoke.setIcon(QtGui.QIcon('./exit.jpg'))
        
        self.pushButton_revoke.setObjectName("pushButton_revoke")
        self.pushButton_next = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_next.setGeometry(QtCore.QRect(320, 470, 171, 30))
        self.pushButton_next.setObjectName("pushButton_next")
        self.pushButton_next.setIcon(QtGui.QIcon('./exit.jpg'))

        self.pushButton_revoke.setStyleSheet('''
                                          QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                                              font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                      ''')
        self.pushButton_next.setStyleSheet('''
                                                 QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                                                     font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                             ''')

        self.label_stop_showing = QtWidgets.QLabel(self.centralwidget)
        self.label_stop_showing.setGeometry(QtCore.QRect(320, 480, 171, 30))
        self.exit_Button.setObjectName("exit_Button")
        self.exit_Button.setStyleSheet('''
                                    QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                ''')
        self.exit_Button.setIcon(QtGui.QIcon('./exit.jpg'))
        self.exit_Button.clicked.connect(self.close)

        
        self.label_stop_showing = QtWidgets.QLabel(self.centralwidget)
        self.label_stop_showing.setGeometry(QtCore.QRect(330, 350, 200, 30))
        self.label_stop_showing.setObjectName("label_stop_showing")
        self.label_stop_showing.setStyleSheet('''
                                                  QLabel{border:none;color:white;font-size:20px;  font-weight:700;
                                                      font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                              ''')
        self.label_show_again = QtWidgets.QLabel(self.centralwidget)
        self.label_show_again.setGeometry(QtCore.QRect(330, 350, 200, 30))
        self.label_show_again.setObjectName("label_show_again")
        self.label_show_again.setStyleSheet('''
                                                          QLabel{border:none;color:white;font-size:20px;  font-weight:700;
                                                              font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                                      ''')
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 121, 16))
        self.label.setObjectName("label")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(105, 81, 581, 231))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(32)
        item.setFont(font)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.listWidget.addItem(item)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(80, 10, 721, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.progressBar.setTextVisible(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 70, 301, 391))
        self.label_2.setStyleSheet("image: url(:/congrats/congrats.jpg);")
        self.label_2.setText("")
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(200, 450, 421, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.pushButton_exit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_exit.setGeometry(QtCore.QRect(320, 490, 171, 71))
        self.pushButton_exit.setObjectName("pushButton_exit")
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
        self.pushButton_no.clicked.connect(MainWindow.forget)
        self.pushButton_revoke.clicked.connect(MainWindow.forget)
        self.pushButton_next.clicked.connect(MainWindow.next_word)
        self.pushButton_next.clicked.connect(MainWindow.hide_exp)
        self.pushButton_next.clicked.connect(self.pushButton_next.hide)
        self.pushButton_next.clicked.connect(self.pushButton_revoke.hide)
        self.pushButton_next.clicked.connect(self.label_show_again.hide)
        self.pushButton_next.clicked.connect(self.label_stop_showing.hide)
        self.pushButton_exit.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_no.setText(_translate("MainWindow", "没记住"))
        self.pushButton_yes.setText(_translate("MainWindow", "记住了"))
        self.exit_Button.setText(_translate("MainWindow", "退   出"))
        self.pushButton_revoke.setText(_translate("MainWindow", "撤   销"))
        self.pushButton_next.setText(_translate("MainWindow", "下一个"))
        self.label_stop_showing.setText(_translate("MainWindow", "今日不再安排学习"))
        self.label_show_again.setText(_translate("MainWindow", "今日继续安排学习"))
        self.label.setText(_translate("MainWindow", "今日进度"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setWordWrap(True)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "word"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "pron"))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "meaning"))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "sent1"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label_3.setText(_translate("MainWindow", "恭喜！您已完成今日学习任务！"))
        self.pushButton_exit.setText(_translate("MainWindow", "退出"))
