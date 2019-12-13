# 游戏UI界面：目前仅显示空的填词格和中文释义

from PyQt5.QtWidgets import * # QApplication, QWidget, QMainWindow, QLabel, QHBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *

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

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.windowTitleChanged.connect(self.onWindowTitleChange)
        self.w_width = 800  # 窗口初始宽度
        self.w_height = 650  # 窗口初始高度
        self.w_left = 100  # 窗口起始位置x
        self.w_top = 100  # 窗口起始位置y
        self.cw_loc = (self.width() / 10, self.w_height / 10)  # 填词格的初始位置 x, y
        self.cw_len = 30  # 单个格子的边长
        self.def_loc = (self.w_width * 2 / 3, self.w_height * 1 / 5)  # 中文释义的初始位置 x, y

    # 初始化窗口
    def initUI(self):
        self.setWindowTitle("快乐背单词")
        self.setGeometry(self.w_left, self.w_top, self.w_width, self.w_height)

    def contextMenuEvent(self, e):
        print("Context menu requested!!")
        super(MainWindow, self).contextMenuEvent(e)

    def onWindowTitleChange(self, s):
        self.setWindowTitle(s)
        print(s)

    # 显示空的填词格
    def showCrossword(self, cw):
        cw_height = cw.nRow
        cw_width = cw.nCol
<<<<<<< HEAD
=======
        my_regex = QRegExp("[a-zA-Z]")
        flag = [[[]for i in range(cw_width)]for j in range(cw_height)]
        self.textbox = [[] for i in range(len(cw.sortedList))]
        self.textbox_word = []
        #self.textbox_map = [[[]for i in range(cw_width)]for j in range(cw_height)]
        for word in cw.sortedList.keys():
            order = cw.sortedList[word][2]['order'] - 1
            i_col = cw.sortedList[word][2]['startPos'][1]
            i_row = cw.sortedList[word][2]['startPos'][0]
            self.textbox_word.append(word)
            if self.textbox[order] != []:
                order += 1
            for i in range(cw.sortedList[word][1]['len']):
                if flag[i_row][i_col] != []:
                    self.textbox[order].append(self.textbox[flag[i_row][i_col][0]][flag[i_row][i_col][1]])
                    if cw.sortedList[word][2]['dir']:
                        i_row += 1
                    else:
                        i_col += 1
                    continue
                self.textbox[order].append(myQLineEdit(self))
                self.textbox[order][i].move(int(self.cw_loc[0] + i_col * self.cw_len), int(self.cw_loc[1] + i_row * self.cw_len))
                self.textbox[order][i].resize(self.cw_len, self.cw_len)
                self.textbox[order][i].setAlignment(Qt.AlignCenter)
                self.textbox[order][i].setFont(QFont("Arial", 16))
                self.textbox[order][i].setMaxLength(1)
                my_validator = QRegExpValidator(my_regex, self.textbox[order][i])
                self.textbox[order][i].setValidator(my_validator)
                flag[i_row][i_col] = [order, i]
                if cw.sortedList[word][2]['dir']:
                    i_row += 1
                else:
                    i_col += 1
        self.textbox_map = flag
        self.textbox[0][0].setFocus()
        current_col = cw.sortedList[self.textbox_word[0]][2]['startPos'][1]
        current_row = cw.sortedList[self.textbox_word[0]][2]['startPos'][0]
        self.current_focus = [current_row, current_col]
        print(self.textbox_word)
        '''    
>>>>>>> game
        for i_row in range(cw_height):
            for i_col in range(cw_width):

                # 逐个生成格子
                if cw.crossword[i_row][i_col] is not '#':
<<<<<<< HEAD
                    self.textbox = QLineEdit(self)
                    self.textbox.move(int(self.cw_loc[0] + i_col * self.cw_len), int(self.cw_loc[1] + i_row * self.cw_len))
                    self.textbox.resize(self.cw_len, self.cw_len)
                    self.textbox.setAlignment(Qt.AlignCenter)
                    self.textbox.setFont(QFont("Arial", 16))
                    self.textbox.setMaxLength(1)
                    textboxValue = self.textbox.text()
=======
                    self.textbox[i_row][i_col] = QLineEdit(self)
                    self.textbox[i_row][i_col].move(int(self.cw_loc[0] + i_col * self.cw_len), int(self.cw_loc[1] + i_row * self.cw_len))
                    self.textbox[i_row][i_col].resize(self.cw_len, self.cw_len)
                    self.textbox[i_row][i_col].setAlignment(Qt.AlignCenter)
                    self.textbox[i_row][i_col].setFont(QFont("Arial", 16))
                    self.textbox[i_row][i_col].setMaxLength(1)
                    my_validator = QRegExpValidator(my_regex, self.textbox[i_row][i_col])
                    self.textbox[i_row][i_col].setValidator(my_validator)
                    textboxValue = self.textbox[i_row][i_col].text()
        '''

    # 在首字母格的左上角 加上与中文释义相对应的序号
    def addLabel(self, cw):
        d_x = 2
        d_y = -9
        for word in cw.sortedList:
            label = QLabel(self)
            label.setText(str(cw.sortedList[word][2]['order']))
            x = int(self.cw_loc[0] + cw.sortedList[word][2]['startPos'][1] * self.cw_len)
            y = int(self.cw_loc[1] + cw.sortedList[word][2]['startPos'][0] * self.cw_len)
            label.move(int(x + d_x), int(y + d_y))
            label.setFont(QFont("Simsun", 8))


>>>>>>> game

    # 在首字母格的左上角 加上与中文释义相对应的序号
    def addLabel(self, cw):
        d_x = 2
        d_y = -9
        for word in cw.sortedList:
            label = QLabel(self)
            label.setText(str(cw.sortedList[word][2]['order']))
            x = int(self.cw_loc[0] + cw.sortedList[word][2]['startPos'][1] * self.cw_len)
            y = int(self.cw_loc[1] + cw.sortedList[word][2]['startPos'][0] * self.cw_len)
            label.move(int(x + d_x), int(y + d_y))
            label.setFont(QFont("Simsun", 8))



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

        print('')
        print(text)
        dispDef = QLabel(self)
        dispDef.setText(text)
        dispDef.move(int(self.def_loc[0]), int(self.def_loc[1]))
        dispDef.setFont(QFont("Simsun", 20))
        dispDef.adjustSize()  # 根据文字自动调整控件大小

    def keyPressEvent(self, a0):
        if(a0.key() == Qt.Key_Up):
            tmp_col = self.current_focus[1]
            tmp_row = self.current_focus[0] - 1
            if(self.textbox_map[tmp_row][tmp_col] != []):
                nextFocusTextBox = self.textbox_map[tmp_row][tmp_col]
                self.textbox[nextFocusTextBox[0]][nextFocusTextBox[1]].setFocus()
                self.current_focus = [tmp_row, tmp_col]
        elif(a0.key() == Qt.Key_Down):
            tmp_col = self.current_focus[1]
            tmp_row = self.current_focus[0] + 1
            if(self.textbox_map[tmp_row][tmp_col] != []):
                nextFocusTextBox = self.textbox_map[tmp_row][tmp_col]
                self.textbox[nextFocusTextBox[0]][nextFocusTextBox[1]].setFocus()
                self.current_focus = [tmp_row, tmp_col]
        elif(a0.key() == Qt.Key_Left):
            tmp_col = self.current_focus[1] - 1
            tmp_row = self.current_focus[0]
            if(self.textbox_map[tmp_row][tmp_col] != []):
                nextFocusTextBox = self.textbox_map[tmp_row][tmp_col]
                self.textbox[nextFocusTextBox[0]][nextFocusTextBox[1]].setFocus()
                self.current_focus = [tmp_row, tmp_col]
        elif(a0.key() == Qt.Key_Right):
            tmp_col = self.current_focus[1] + 1
            tmp_row = self.current_focus[0]
            if(self.textbox_map[tmp_row][tmp_col] != []):
                nextFocusTextBox = self.textbox_map[tmp_row][tmp_col]
                self.textbox[nextFocusTextBox[0]][nextFocusTextBox[1]].setFocus()
                self.current_focus = [tmp_row, tmp_col]
        else:
            super().keyPressEvent(a0)
            pass
    