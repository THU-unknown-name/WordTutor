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
from game.Crossword import MyCrossword
#from game.getWordList import wordList
from game.getBestCrossword import *
from StudyPlan.Vocab import Vocab
from WordDict.WordDict import *


class ErrorWin(object):
    def __init__(self):
        self.errorWin = QtWidgets.QWidget()

    def show_error(self, error_msg):
        reply = QtWidgets.QMessageBox.question(self.errorWin, 'Message', 
            error_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            pass

class Ui_MainWindow(object):
    def __init__(self, WORD_DICT):
        self.WORD_DICT = WORD_DICT
        self.errorWin = ErrorWin()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(340, 100, 101, 40))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)        #查询单词
        self.pushButton.setGeometry(QtCore.QRect(340, 150, 120, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)      #退出
        self.pushButton_2.setGeometry(QtCore.QRect(340, 300, 120, 41))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)      #背单词
        self.pushButton_3.setGeometry(QtCore.QRect(340, 200, 120, 41))
        self.pushButton_3.setObjectName("pushButton_3")

        self.game_button = QtWidgets.QPushButton(self.centralwidget)      #游戏
        self.game_button.setGeometry(QtCore.QRect(340, 250, 120, 41))
        self.game_button.setObjectName("game_button")

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
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setStyleSheet("#MainWindow{border-image:url(background.png);}")
    def word_search(self):
        self.ui_search=look_up(self.WORD_DICT)
        self.ui_search.show()
    def my_test(self):
        self.ui_recite=ReciteGUI(self.WORD_DICT)
        if not self.ui_recite.finished:
            self.ui_recite.show()
    def game_window(self):
        vocab = Vocab(self.WORD_DICT)
        word_list_for_game = vocab.get_n_word_from_familiarVocab(8)
        wordList = {}
        for word in word_list_for_game:
            word_mean = self.WORD_DICT.get_mean(word)
            if word_mean == WORD_NOT_FOUND:
                self.errorWin.show_error("The meaning of the word:{} not found".format(word))
                return
            wordList[word] = [[word_mean], {}]
        cw = getBestCrossword(wordList)        
        defCross = cw.getDefCross()    # 打印横向单词列表，获取中文释义
        defDown = cw.getDefDown()     # 打印纵向单词列表，获取中文释义
        self.ui_game = gameWindow()
        self.ui_game.initUI(cw)
        self.ui_game.showCrossword()  # 显示空填词格
        self.ui_game.showDefinition(defCross, defDown)  # 显示中文释义
        self.ui_game.addLabel()
        self.ui_game.addButtons()
        self.ui_game.show()
        pass
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "   主菜单"))
        self.pushButton.setText(_translate("MainWindow", "查询单词"))
        self.pushButton_2.setText(_translate("MainWindow", "退   出"))
        self.pushButton_3.setText(_translate("MainWindow", "背 单 词"))
        self.game_button.setText(_translate("MainWindow", "进入游戏"))