# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mymainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from lookup import look_up
from StudyPlan.recite_action import ReciteGUI
from game.ui_game import gameWindow
from game.gameSystem import *
from StudyPlan.Vocab import Vocab
from WordDict.WordDict import *
from StudyPlan.setting_action import SettingGUI


class ErrorWin(object):
    def __init__(self):
        self.errorWin = QtWidgets.QWidget()

    def show_error(self, error_msg):
        reply = QtWidgets.QMessageBox.question(self.errorWin, 'Message', 
            error_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            pass

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, WORD_DICT):
        super(Ui_MainWindow, self).__init__()
        self.WORD_DICT = WORD_DICT
        self.errorWin = ErrorWin()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(360, 80, 150, 60))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setStyleSheet('''
                    QLabel{color:white;font-size:25px;  font-weight:700;
                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                ''')
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)        #查询单词
        self.pushButton.setGeometry(QtCore.QRect(320, 150, 150, 60))
        self.pushButton.setIcon(QtGui.QIcon('./lookup.jpg'))
        self.pushButton.setStyleSheet('''
            QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
        ''')
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)      #退出
        self.pushButton_2.setGeometry(QtCore.QRect(320, 430, 150, 60))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setIcon(QtGui.QIcon('./exit.jpg'))
        self.pushButton_2.setStyleSheet('''
                           QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                       ''')
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)      #背单词
        self.pushButton_3.setGeometry(QtCore.QRect(320, 220, 150, 60))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setIcon(QtGui.QIcon('./recite.jpg'))
        self.pushButton_3.setStyleSheet('''
                    QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                ''')

        self.game_button = QtWidgets.QPushButton(self.centralwidget)      #游戏
        self.game_button.setGeometry(QtCore.QRect(320, 290, 150, 60))
        self.game_button.setObjectName("game_button")
        self.game_button.setIcon(QtGui.QIcon('./game1.jpg'))
        self.game_button.setStyleSheet('''
                           QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                       ''')
        
        self.plan_button = QtWidgets.QPushButton(self.centralwidget)  # 计划管理
        self.plan_button.setGeometry(QtCore.QRect(320, 360, 150, 60))
        self.plan_button.setObjectName("game_button")
        self.plan_button.setIcon(QtGui.QIcon('./plan.jpg'))
        self.plan_button.setStyleSheet('''
                                   QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                               ''')
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.pushButton.clicked.connect(self.word_search)
        self.pushButton_2.clicked.connect(QCoreApplication.instance().quit)
        self.pushButton_3.clicked.connect(self.my_test)
        self.game_button.clicked.connect(self.game_window)
        self.plan_button.clicked.connect(self.plan_manage)

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setStyleSheet("#MainWindow{border-image:url(bak1.jpg);}")
    def word_search(self):
        self.ui_search=look_up(self.WORD_DICT)
        #self.ui_search.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.ui_search.show()
    def my_test(self):
        self.ui_recite=ReciteGUI(self.WORD_DICT)
        self.ui_recite.setStyleSheet("#MainWindow{border-image:url(bak1.jpg)}")
        #self.ui_recite.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        if not  self.ui_recite.finished:
            self.ui_recite.show()
    def game_window(self):
        self.myGame = gameSystem(self.WORD_DICT)
        cw = self.myGame.createGameFromStudy(self.WORD_DICT, self.errorWin)
        self.ui_game = gameWindow()
        self.ui_game.initUI(cw, self.WORD_DICT, self.errorWin)
        self.ui_game.setStyleSheet("#MainWindow{border-image:url(bak1.jpg)}")
        # self.ui_game.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.ui_game.show()
        pass
    def plan_manage(self):
        self.plan_ui = SettingGUI(self.WORD_DICT)
        self.plan_ui.setStyleSheet("#MainWindow{border-image:url(bak1.jpg)}")
        self.plan_ui.show()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "主菜单"))
        self.pushButton.setText(_translate("MainWindow", "查询单词"))
        self.pushButton_2.setText(_translate("MainWindow", "退出"))
        self.pushButton_3.setText(_translate("MainWindow", "背单词"))
        self.game_button.setText(_translate("MainWindow", "进入游戏"))
        self.plan_button.setText(_translate("MainWindow", "计划管理"))
