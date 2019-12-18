# 当前进度：给定单词，生成填词游戏并显示
"""
    待完成：
    - 生成填词游戏的算法较为完备，有一定优化，可进一步优化
    - 测评系统（打分系统、进行下一个游戏等）
"""

import sys
from ui_game import *
from gameSystem import *

cw = createGameFromAllWord()
cw.display()  # 打印填词游戏

# 开始创建GUI
app = QApplication(sys.argv)

window = gameWindow()  # 创建窗口
window.initUI(cw)
window.show()

# start the event loop
app.exec_()
