# 当前进度：给定单词，生成填词游戏并显示
# 待完成：
# - 生成填词游戏的算法不完备，待优化
# - 数据库接口
# - 测评系统（检查是否正确、打分系统、进行下一个游戏等）
# - 完善UI，（美化、按键等）

import sys
from getWordList import wordList
from Crossword import *
from ui_game import *

# 生成填字游戏
cw = MyCrossword()  # 初始化MyCrossword类
cw.generateCrossword(wordList)  # 根据单词列表生成填词游戏 （此为示例，待完成生词本接口）
cw.display()  # 打印填词游戏
cw.printCrossword()  # 打印填词游戏变量

cw.printWordList()  # 打印全部单词列表
defCross = cw.getDefCross()    # 打印横向单词列表，获取中文释义
defDown = cw.getDefDown()     # 打印纵向单词列表，获取中文释义

# 开始创建GUI
app = QApplication(sys.argv)

window = MainWindow()  # 创建窗口
window.initUI()
window.showCrossword(cw.crossword)  # 显示空填词格
window.showDefinition(defCross, defDown)  # 显示中文释义
window.show()

# start the event loop
app.exec_()
