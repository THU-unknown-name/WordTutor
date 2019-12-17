# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lookup.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette,QBrush,QPixmap
from WordDict import WordDict
import win32com.client
import numpy as np
from PyQt5.QtWidgets import QMessageBox
from StudyPlan.Vocab import Vocab

def link(lList):
    if type(lList) is list:
        if len(lList)>0:
            sResult = link(lList[0])
            for iLoop in range(1,len(lList)):
                sResult+="\n"+link(lList[iLoop])
            return sResult
        else:
            return ""
    else:
        return str(lList)


class look_up(QtWidgets.QMainWindow):
    def __init__(self, WORD_DICT):
        super(look_up,self).__init__()
        self.WORD_DICT = WORD_DICT
        self.setupUi(self)
        self.retranslateUi(self)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.suggestion_label = QtWidgets.QLabel(self.centralwidget)
        self.suggestion_label.setGeometry(QtCore.QRect(100, 100, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.suggestion_label.setFont(font)
        self.suggestion_label.setObjectName("suggestion_label")
        self.suggestion_label.setStyleSheet('''
                    QLabel{border:none;color:white;font-weight:700;
                        }
                ''')
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(230, 100, 300, 40))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFont(QtGui.QFont("Arial", 20))

        self.sure_Button = QtWidgets.QPushButton(self.centralwidget)
        self.sure_Button.setGeometry(QtCore.QRect(550, 100, 70, 30))
        font = QtGui.QFont()
        font.setFamily("华文细黑")
        self.sure_Button.setFont(font)
        self.sure_Button.setObjectName("sure_Button")
        self.sure_Button.setStyleSheet('''
                    QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                ''')

        self.browser = QtWidgets.QTextBrowser(self.centralwidget)
        self.browser.setGeometry(QtCore.QRect(190, 150, 400, 300))
        self.browser.setObjectName("my_browser")

        self.browser.setStyleSheet("#QTextBrowser{border-image:url(bak1.jpg);}")
        #self.browser.setWordWrap(True)
        #self.browser.setAlignment(Qt.AlignTop)
        self.exit_Button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_Button.setGeometry(QtCore.QRect(150, 460, 150, 31))
        self.exit_Button.setObjectName("exit_Button")
        self.exit_Button.setStyleSheet('''
                            QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                        ''')
        self.exit_Button.setIcon(QtGui.QIcon('./exit.jpg'))


        self.add_Button = QtWidgets.QPushButton(self.centralwidget)
        self.add_Button.setGeometry(QtCore.QRect(440, 460, 150, 31))
        self.add_Button.setObjectName("add_Button")
        self.add_Button.setStyleSheet('''
                                    QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                ''')

        self.sound_button = QtWidgets.QPushButton(self.centralwidget)
        self.sound_button.setGeometry(QtCore.QRect(650, 100, 70, 30))
        font = QtGui.QFont()
        font.setFamily("华文细黑")
        self.sound_button.setFont(font)
        self.sound_button.setObjectName("sound_button")
        self.sound_button.clicked.connect(self.mywordsound)
        self.sound_button.setStyleSheet('''
                            QPushButton{border:none;color:white;font-size:25px;  font-weight:700;
                                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                        ''')
        self.sound_button.setIcon(QtGui.QIcon('./sound.jpg'))

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
        self.exit_Button.clicked.connect(self.close)
        self.sure_Button.clicked.connect(self.mysearchword)
        self.add_Button.clicked.connect(self.add_to_wordkeeper)
        MainWindow.setStyleSheet("#MainWindow{border-image:url(bak1.jpg)}")


    def mywordsound(self):          #发音
        word_to_pronounce = self.lineEdit.text()
        spk = win32com.client.Dispatch("SAPI.SpVoice")
        #spk.Voice = spk.GetVoices("language=409").Item(0)
        spk.Speak(word_to_pronounce)


    def add_to_wordkeeper(self):     #添加生词本
        word_to_add =  self.lineEdit.text()
        reply = QMessageBox.question(self, 'Message', '是否确认添加?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            '''添加word_to_add到生词本中的操作'''
            vocab = Vocab(self.WORD_DICT)
            vocab.add_word_to_vocab(word_to_add)
            pass
        else:
            pass
    def mysearchword(self):           #搜索单词
        # WORD_DICT = WordDict.WordDict()
        # load_err = WORD_DICT.load('WordDict\\dict')
        # if load_err != WordDict.WORD_DICT_LOAD_SUCCEED:
        #     print(load_err)
        #     exit(0)
        word_to_search = self.lineEdit.text()
        #这里的代码需要根据word_to_search查找相关的解释
        #search_result = "heheda"
        if word_to_search=="": pass
        else:

            search_result=self.WORD_DICT.get_info(word_to_search)

            if search_result==-1:
                xiu_result = "没有查询到相应的单词\n"
            # max_recorder = 0
            # max_word ="happy"
            # for word,haha in self.WORD_DICT.navigate():
            #     common_len = longestCommonSequence(word,word_to_search)
            #     if common_len>max_recorder:
            #         max_word = word
            #         max_recorder = common_len
                [likelihood, wordlist] = self.WORD_DICT.match_word(word_to_search)
                top5index = np.argsort(likelihood)[:5]
                top5word = [wordlist[i] for i in top5index]
                max_word = top5word[0]
                xiu_result=xiu_result+"您要查找的是不是下面的单词？\n"+max_word+"\n"
                temp = self.WORD_DICT.get_info(max_word)
                #print(temp)
                xiu_result+=temp[0][1]+"\n"+temp[0][0]+"\n"+temp[1]['hennkou']+"\n"+link(temp[1]['reiku'])
            else:
                #print(search_result)
                xiu_result = search_result[0][1]+"\n"+search_result[0][0]+"\n"+search_result[1]['hennkou']+"\n"+link(search_result[1]['reiku'])

                #返回结果为search_result
                self.browser.setText(xiu_result)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "单词搜索"))
        self.suggestion_label.setText(_translate("MainWindow", "输入单词"))
        self.exit_Button.setText(_translate("MainWindow", "退出"))
        self.sound_button.setText(_translate("MainWindow", "发音"))
        self.add_Button.setText(_translate("MainWindow", "加入背诵计划"))
        self.sure_Button.setText(_translate("MainWindow", "确定"))


def longestCommonSequence(str_one, str_two, case_sensitive=True):     #寻找最大公有子串

    len_str1 = len(str_one)
    len_str2 = len(str_two)
    # 定义一个列表来保存最长公共子序列的长度，并初始化
    record = [[0 for i in range(len_str2 + 1)] for j in range(len_str1 + 1)]
    for i in range(len_str1):
        for j in range(len_str2):
            if str_one[i] == str_two[j]:
                record[i + 1][j + 1] = record[i][j] + 1
            elif record[i + 1][j] > record[i][j + 1]:
                record[i + 1][j + 1] = record[i + 1][j]
            else:
                record[i + 1][j + 1] = record[i][j + 1]

    return record[-1][-1]
