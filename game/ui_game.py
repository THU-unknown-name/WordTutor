# 游戏UI界面：目前仅显示空的填词格和中文释义

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from game.gameSystem import *
from game.getBestCrossword import *
import numpy as np


class myQLineEdit(QLineEdit):
    def __init__(self, parent, row, col):
        super(myQLineEdit, self).__init__(parent)
        self.parent = parent
        self.row = row
        self.col = col

    def keyPressEvent(self, a0):
        if (a0.key() == Qt.Key_Up) | (a0.key() == Qt.Key_Down) | (a0.key() == Qt.Key_Left) | (a0.key() == Qt.Key_Right):
            self.parent.keyPressEvent(a0)
        else:
            super().keyPressEvent(a0)

    def focusInEvent(self, QFocusEvent):
        self.parent.current_focus = [self.row, self.col]
        super().focusInEvent(QFocusEvent)
    pass

class gameWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(gameWindow, self).__init__(*args, **kwargs)

        self.windowTitleChanged.connect(self.onWindowTitleChange)
        self.w_width = 800  # 窗口初始宽度 1000
        self.w_height = 600  # 窗口初始高度 650
        self.w_left = 10  # 窗口起始位置x
        self.w_top = 10  # 窗口起始位置y
        self.gap = 30  # 模块之间、模块与边界的距离
        self.cw_loc = (0, 0)  # 经过居中调整后的填词格的初始位置
        self.init_cw_len = 30  # 单个格子的默认边长
        self.cw_len = 30  # 单个格子的实际边长
        self.def_loc = (self.w_width * 1 / 2 + 10, 0)  # 中文释义的初始位置 x, y
        self.def_w = self.w_width - self.def_loc[0] - self.w_width / 20
        self.def_h = 500
        self.tbEdgeColor = "rgb(150, 150, 150)"
        self.btn_top = 525  # 按键的y轴位置
        # self.textbox = []
        self.testMode = False


    # 初始化窗口
    def initUI(self, cw, WORD_DICT, errorWin):
        self.WORD_DICT =WORD_DICT
        self.errorWin = errorWin
        self.cw = cw
        self.setWindowTitle("快乐背单词")
        self.resize(self.w_width, self.w_height)
        self.checkOverlap()
        self.showCrossword()  # 显示空填词格
        self.showDefinition(cw.getDefCross(), cw.getDefDown())  # 显示中文释义
        self.addLabel()  # 标号
        self.addButtons()
        self.setObjectName("MainWindow")

    def addButtons(self):
        '''
        添加按键
        '''
        self.showAns = QPushButton('显示答案', self)
        self.showAns.setGeometry(QRect(150, self.btn_top, 100, 41))
        self.showAns.clicked.connect(self.showAnswer)
        self.showAns.setStyleSheet('''
                                            QPushButton{border:none;color:white;font-size:25px;font-weight:700;
                                                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                        ''')
        self.hideAns = QPushButton('隐藏答案', self)
        self.hideAns.setGeometry(QRect(150, self.btn_top, 100, 41))
        self.hideAns.clicked.connect(self.hideAnswer)
        self.hideAns.setVisible(False)
        self.hideAns.setStyleSheet('''
                            QPushButton{border:none;color:white;font-size:25px;font-weight:700;
                            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                    ''')

        self.checkAns = QPushButton('检查答案', self)
        self.checkAns.setGeometry(QRect(270, self.btn_top, 100, 41))
        self.checkAns.clicked.connect(self.checkAnswer)
        self.checkAns.setStyleSheet('''
                            QPushButton{border:none;color:white;font-size:25px;font-weight:700;
                                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                        ''')

        self.exit = QPushButton('退出', self)
        self.exit.setGeometry(QRect(390, self.btn_top, 100, 41))
        self.exit.clicked.connect(self.close)
        self.exit.setStyleSheet('''
                            QPushButton{border:none;color:white;font-size:25px;font-weight:700;
                                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                        ''')

        self.nextGame = QPushButton('下一轮', self)
        self.nextGame.setGeometry(QRect(510, self.btn_top, 100, 41))
        self.nextGame.clicked.connect(self.getNextGame)
        self.nextGame.setStyleSheet('''
                                    QPushButton{border:none;color:white;font-size:25px;font-weight:700;
                                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
                                ''')

    def checkOverlap(self):
        '''
        检查填词游戏和中文释义显示是否重合，根据此调整显示比例
        :return: shift_def_w 中文释义模块需要向右移动的距离
        '''
        MIN_DEF_W = 250
        lSideCw = 10
        rSideCw = lSideCw + self.cw.nCol * self.init_cw_len
        dSideCW = self.cw.nRow * self.init_cw_len
        lSideDef = self.def_loc[0]

        # 如果填词游戏和中文释义重叠
        shift_def_w = 0
        if lSideDef < rSideCw + self.gap:
            lapped = rSideCw + self.gap - lSideDef
            shift_def_w = self.def_w - max(self.def_w - lapped, MIN_DEF_W)

        # 如果中文释义模块已达到最小宽度后仍然重叠，缩小填词格的宽度
        new_cw_len_1 = self.init_cw_len
        if self.def_loc[0] + shift_def_w < rSideCw:
            max_cw_w = self.def_loc[0] - 2 * self.gap - lSideCw

            new_cw_len_1 = max_cw_w/(self.cw.nCol * self.init_cw_len) * self.init_cw_len

        # 如果填词游戏和按键重叠
        new_cw_len_2 = self.init_cw_len
        if dSideCW > self.btn_top:
            max_cw_h = self.btn_top - 2 * self.gap
            new_cw_len_2 = max_cw_h/(self.cw.nRow * self.init_cw_len) * self.init_cw_len

        self.cw_len = min(new_cw_len_1, new_cw_len_2)

        # 填词游戏在左侧居中显示
        cw_loc_x = (lSideDef + shift_def_w) / 2 - self.cw.nCol * self.cw_len / 2
        cw_loc_y = self.btn_top / 2 - self.cw.nRow * self.cw_len / 2

        self.cw_loc = (cw_loc_x, cw_loc_y)

        return shift_def_w

    def showCrossword(self):
        '''
        显示空的填词格
        '''
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
                self.textbox[word_id].append(myQLineEdit(self, i_row, i_col))
                self.textbox[word_id][i].move(int(self.cw_loc[0] + i_col * self.cw_len), int(self.cw_loc[1] + i_row * self.cw_len))
                self.textbox[word_id][i].resize(self.cw_len - 1, self.cw_len - 1)
                self.textbox[word_id][i].setAlignment(Qt.AlignCenter)
                self.textbox[word_id][i].setFont(QFont("Arial", 16))
                self.textbox[word_id][i].setMaxLength(1)
                self.textbox[word_id][i].setStyleSheet("border: 0.5px solid %s;" % self.tbEdgeColor)
                my_validator = QRegExpValidator(my_regex, self.textbox[word_id][i])
                self.textbox[word_id][i].setValidator(my_validator)
                flag[i_row][i_col] = [word_id, i]
                if self.cw.sortedList[word][2]['dir']:
                    i_row += 1
                else:
                    i_col += 1

        self.textbox_map = flag
        self.textbox[0][0].setFocus()
        current_row = self.textbox[0][1].row
        current_col = self.textbox[0][1].col
        self.current_focus = [current_row, current_col]
        if self.testMode: print('textbox: ', self.textbox)
        if self.testMode: print('textmap: ', self.textbox_map)

    def getNextGame(self):
        '''
        加载下一轮游戏
        '''
        self.clearAll()
        cw = createGameFromStudy(self.WORD_DICT, self.errorWin)
        self.cw = cw
        self.close()
        self.initUI(cw, self.WORD_DICT, self.errorWin)
        self.show()
        # QApplication.processEvents()

    def clearAll(self):
        '''
        清除上一轮游戏的控件
        '''
        self.dispDef.deleteLater()

        for item in self.label:
            item.deleteLater()

        for item in self.textbox:
            for textbox in item:
                textbox.deleteLater()

        self.textbox = [[] for i in range(len(self.cw.sortedList))]
        self.label = []

    def checkAnswer(self):
        '''
        检查答案
        :return:
        '''
        print('检查答案！')
        cw_height = self.cw.nRow
        cw_width = self.cw.nCol
        for i_row in range(cw_height):
            for i_col in range(cw_width):
                # 逐个生成格子
                if self.textbox_map[i_row][i_col]:
                    word_id = self.textbox_map[i_row][i_col][0]
                    i = self.textbox_map[i_row][i_col][1]
                    ans = self.cw.crossword[i_row][i_col]
                    usr_input = self.textbox[word_id][i].text()

                    if usr_input.upper() != ans.upper():
                        self.textbox[word_id][i].setStyleSheet("border: 0.5px solid %s; "
                                                               "background-color:rgba(255,225,225);" % self.tbEdgeColor)
                        if usr_input:
                            self.textbox[word_id][i].setStyleSheet("border: 0.5px solid %s;"
                                                                   "color:red; "
                                                                   "background-color: rgb(255,225,225);" % self.tbEdgeColor)
                    else:
                        self.textbox[word_id][i].setStyleSheet("border: 0.5px solid %s;"
                                                               "background-color: rgb(255,255,255)" % self.tbEdgeColor)

    def showAnswer(self):
        '''
        显示答案
        '''
        print('显示答案！')
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

        QApplication.processEvents()

    def hideAnswer(self):
        '''
        隐藏答案
        '''
        print('隐藏答案！')
        self.hideAns.setVisible(False)
        self.showAns.setVisible(True)
        for item in self.textbox:
            for textbox in item:
                textbox.setText('')

        QApplication.processEvents()

    def addLabel(self):
        '''
        在首字母格的左上角 加上与中文释义相对应的序号
        :return:
        '''
        d_x = 2
        d_y = -9
        self.label = []
        for word in self.cw.sortedList:
            label = QLabel(self)
            label.setText(str(self.cw.sortedList[word][2]['order']))
            x = int(self.cw_loc[0] + self.cw.sortedList[word][2]['startPos'][1] * self.cw_len)
            y = int(self.cw_loc[1] + self.cw.sortedList[word][2]['startPos'][0] * self.cw_len)
            label.move(int(x + d_x), int(y + d_y))
            label.setFont(QFont("Simsun", 7))
            self.label.append(label)

    def showDefinition(self, defCross, defDown):
        '''
        显示中文释义
        :param defCross: 横向单词列表
        :param defDown: 纵向单词列表
        :return:
        '''
        shift_def_w = self.checkOverlap()
        if self.testMode: print('shift_def_w: ', shift_def_w)
        if self.testMode: print('cw_len: ', self.cw_len)
        if self.testMode: print('def_w: ', self.def_w - shift_def_w)
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

        self.dispDef = QLabel(self)
        self.dispDef.setText(text)
        self.dispDef.setGeometry(QRect(int(self.def_loc[0] + shift_def_w), int(self.def_loc[1]), self.def_w - shift_def_w, self.def_h))
        self.dispDef.setWordWrap(True)
        self.dispDef.setAlignment(Qt.AlignVCenter)
        self.dispDef.setFont(QFont("Simsun", 16))
        self.dispDef.setStyleSheet('''
                                    QLabel{border:none;color:white;font-weight:00;
                                        }
                                ''')

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

    def contextMenuEvent(self, e):
        print("Context menu requested!!")
        super(gameWindow, self).contextMenuEvent(e)

    def onWindowTitleChange(self, s):
        self.setWindowTitle(s)
