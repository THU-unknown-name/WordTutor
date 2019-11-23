# 游戏UI界面：目前仅显示空的填词格和中文释义

from PyQt5.QtWidgets import * # QApplication, QWidget, QMainWindow, QLabel, QHBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *

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
    def showCrossword(self, crossword):
        cw_height = crossword.__len__()
        cw_width = crossword[0].__len__()
        for i_row in range(cw_height):
            for i_col in range(cw_width):

                # 逐个生成格子
                if crossword[i_row][i_col] is not '#':
                    self.textbox = QLineEdit(self)
                    self.textbox.move(int(self.cw_loc[0] + i_col * self.cw_len), int(self.cw_loc[1] + i_row * self.cw_len))
                    self.textbox.resize(self.cw_len, self.cw_len)
                    self.textbox.setAlignment(Qt.AlignCenter)
                    self.textbox.setMaxLength(1)
                    textboxValue = self.textbox.text()

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
