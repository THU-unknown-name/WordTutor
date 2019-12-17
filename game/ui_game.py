# 游戏UI界面：目前仅显示空的填词格和中文释义

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np


class myQLineEdit(QLineEdit):
    def __init__(self, parent):
        super(myQLineEdit, self).__init__(parent)
        self.parent = parent
    def keyPressEvent(self, a0):
        if((a0.key() == Qt.Key_Up) | (a0.key() == Qt.Key_Down) | (a0.key() == Qt.Key_Left) | (a0.key() == Qt.Key_Right)):
            self.parent.keyPressEvent(a0)
        else:
            super().keyPressEvent(a0)
    pass

class gameWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(gameWindow, self).__init__(*args, **kwargs)

        self.windowTitleChanged.connect(self.onWindowTitleChange)
        self.w_width = 800  # 窗口初始宽度 1000
        self.w_height = 600  # 窗口初始高度 650
        self.w_left = 10  # 窗口起始位置x
        self.w_top = 10  # 窗口起始位置y
        self.cw_loc = (self.width() / 10, self.w_height / 10)  # 填词格的初始位置 x, y
        self.cw_len = 30  # 单个格子的边长
        self.def_loc = (self.w_width * 1 / 2, self.w_height * 1 / 10)  # 中文释义的初始位置 x, y
        self.textbox = []
        self.testMode = True


    # 初始化窗口
    def initUI(self, cw):
        self.cw = cw
        self.setWindowTitle("快乐背单词")
        self.setGeometry(self.w_left, self.w_top, self.w_width, self.w_height)

        self.showCrossword()  # 显示空填词格
        self.showDefinition(cw.getDefCross(), cw.getDefDown())  # 显示中文释义
        self.addLabel()  # 标号
        self.addButtons()
        self.setObjectName("MainWindow")
        self.setStyleSheet("#MainWindow{border-image:url(background1.jpg);}")


    def contextMenuEvent(self, e):
        print("Context menu requested!!")
        super(gameWindow, self).contextMenuEvent(e)

    def onWindowTitleChange(self, s):
        self.setWindowTitle(s)
        print(s)

    # 显示空的填词格
    def showCrossword(self):
        cw_height = self.cw.nRow
        cw_width = self.cw.nCol
        my_regex = QRegExp("[a-zA-Z]")
        flag = [[[]for i in range(cw_width)]for j in range(cw_height)]
        self.textbox = [[] for i in range(len(self.cw.sortedList))]
        self.textbox_word = []
        for word in self.cw.sortedList.keys():
            word_id = self.cw.sortedList[word][2]['id']
            i_col = self.cw.sortedList[word][2]['startPos'][1]
            i_row = self.cw.sortedList[word][2]['startPos'][0]
            self.textbox_word.append(word)
            for i in range(self.cw.sortedList[word][1]['len']):
                if flag[i_row][i_col] != []:
                    self.textbox[word_id].append(self.textbox[flag[i_row][i_col][0]][flag[i_row][i_col][1]])
                    if self.cw.sortedList[word][2]['dir']:
                        i_row += 1
                    else:
                        i_col += 1
                    continue
                self.textbox[word_id].append(myQLineEdit(self))
                self.textbox[word_id][i].move(int(self.cw_loc[0] + i_col * self.cw_len), int(self.cw_loc[1] + i_row * self.cw_len))
                self.textbox[word_id][i].resize(self.cw_len, self.cw_len)
                self.textbox[word_id][i].setAlignment(Qt.AlignCenter)
                self.textbox[word_id][i].setFont(QFont("Arial", 16))
                self.textbox[word_id][i].setMaxLength(1)
                my_validator = QRegExpValidator(my_regex, self.textbox[word_id][i])
                self.textbox[word_id][i].setValidator(my_validator)
                flag[i_row][i_col] = [word_id, i]
                if self.cw.sortedList[word][2]['dir']:
                    i_row += 1
                else:
                    i_col += 1

        self.textbox_map = flag
        self.textbox[0][1].setFocus()
        current_col = self.cw.sortedList[self.textbox_word[0]][2]['startPos'][1]
        current_row = self.cw.sortedList[self.textbox_word[0]][2]['startPos'][0]
        self.current_focus = [current_row, current_col]
        if self.testMode: print('textbox: ', self.textbox)
        if self.testMode: print('textmap: ', self.textbox_map)

        # print('focs: ',self.textbox[0][0].setFocus())
        # self.textbox[0][1].cursorPositionChanged.connect(self.updateFocus)

    def updateFocus(self):
        print('yay')

    # 在首字母格的左上角 加上与中文释义相对应的序号
    def addLabel(self):
        d_x = 2
        d_y = -9
        for word in self.cw.sortedList:
            label = QLabel(self)
            label.setText(str(self.cw.sortedList[word][2]['order']))
            x = int(self.cw_loc[0] + self.cw.sortedList[word][2]['startPos'][1] * self.cw_len)
            y = int(self.cw_loc[1] + self.cw.sortedList[word][2]['startPos'][0] * self.cw_len)
            label.move(int(x + d_x), int(y + d_y))
            label.setFont(QFont("Simsun", 7))

    # 显示中文释义
    def showDefinition(self, defCross, defDown):
        # defCross, defDown: 横向和纵向两个答词列表
        text = ''
        text = text + '横向：\n'
        for item in defCross:
            text = text + str(item[0]) + '. ' + item[1] + '\n'

        text = text + '\n纵向：\n'
        for item in defDown:
            text = text + str(item[0]) + '. ' + item[1] + '\n'

        if self.testMode:
            print('')
            print(text)

        dispDef = QLabel(self)
        dispDef.setText(text)
        dispDef.move(int(self.def_loc[0]), int(self.def_loc[1]))
        dispDef.setFont(QFont("Simsun", 13))
        dispDef.setStyleSheet('''
                            QLabel{border:none;color:white;font-weight:700;
                                }
                        ''')
        dispDef.adjustSize()  # 根据文字自动调整控件大小

    # 按键
    def addButtons(self):
        self.showAns = QPushButton('显示答案', self)
        self.showAns.setGeometry(QRect(150, 500, 120, 41))
        self.showAns.clicked.connect(self.showAnswer)
        self.showAns.setStyleSheet('''
                                            QPushButton{border:none;color:white;font-size:25px;font-weight:700;
                                                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                        ''')
        self.hideAns = QPushButton('隐藏答案', self)
        self.hideAns.setGeometry(QRect(150, 500, 120, 41))
        self.hideAns.clicked.connect(self.hideAnswer)
        self.hideAns.setVisible(False)
        self.hideAns.setStyleSheet('''
                                                    QPushButton{border:none;color:white;font-size:25px;font-weight:700;
                                                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                                ''')
        self.exit = QPushButton('退出', self)
        self.exit.setGeometry(QRect(300, 500, 120, 41))
        self.exit.clicked.connect(self.close)
        self.exit.setStyleSheet('''
                                                    QPushButton{border:none;color:white;font-size:25px;font-weight:700;
                                                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                                ''')

    # 显示答案
    def showAnswer(self):
        print('显示答案！')
        # self.showAns.setText('隐藏答案')
        self.showAns.setVisible(False)
        self.hideAns.setVisible(True)
        cw_height = self.cw.nRow
        cw_width = self.cw.nCol
        for i_row in range(cw_height):
            for i_col in range(cw_width):
                # 逐个生成格子
                if self.textbox_map[i_row][i_col]:
                    word_id = self.textbox_map[i_row][i_col][0]
                    i = self.textbox_map[i_row][i_col][1]
                    self.textbox[word_id][i].setText(self.cw.crossword[i_row][i_col])

        # self.showAns.clicked.connect(self.hideAnswer)
        # self.showAns.clicked.connect(self.hideAnswer)
        QApplication.processEvents()

    def hideAnswer(self):
        print('隐藏答案！')
        # self.showAns.setText('显示答案')
        self.hideAns.setVisible(False)
        self.showAns.setVisible(True)
        for item in self.textbox:
            for textbox in item:
                textbox.setText('')

        # self.showAns.clicked.connect(self.showAnswer)
        QApplication.processEvents()

    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key_Up:
            tmp_col = self.current_focus[1]
            tmp_row = self.current_focus[0] - 1
            if self.textbox_map[tmp_row][tmp_col] != []:
                nextFocusTextBox = self.textbox_map[tmp_row][tmp_col]
                self.textbox[nextFocusTextBox[0]][nextFocusTextBox[1]].setFocus()
                self.current_focus = [tmp_row, tmp_col]

        elif a0.key() == Qt.Key_Down:
            tmp_col = self.current_focus[1]
            tmp_row = min(self.cw.nRow - 1, self.current_focus[0] + 1)
            if self.textbox_map[tmp_row][tmp_col] != []:
                nextFocusTextBox = self.textbox_map[tmp_row][tmp_col]
                self.textbox[nextFocusTextBox[0]][nextFocusTextBox[1]].setFocus()
                self.current_focus = [tmp_row, tmp_col]

        elif a0.key() == Qt.Key_Left:
            tmp_col = self.current_focus[1] - 1
            tmp_row = self.current_focus[0]
            if self.textbox_map[tmp_row][tmp_col] != []:
                nextFocusTextBox = self.textbox_map[tmp_row][tmp_col]
                self.textbox[nextFocusTextBox[0]][nextFocusTextBox[1]].setFocus()
                self.current_focus = [tmp_row, tmp_col]

        elif a0.key() == Qt.Key_Right:
            tmp_col = min(self.cw.nCol - 1, self.current_focus[1] + 1)
            tmp_row = self.current_focus[0]
            if (self.textbox_map[tmp_row][tmp_col] != []):
                nextFocusTextBox = self.textbox_map[tmp_row][tmp_col]
                self.textbox[nextFocusTextBox[0]][nextFocusTextBox[1]].setFocus()
                self.current_focus = [tmp_row, tmp_col]
        else:
            super().keyPressEvent(a0)
            pass
