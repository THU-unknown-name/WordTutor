# 当前进度：给定单词，生成填词游戏并显示
"""
    待完成：
    - 生成填词游戏的算法较为完备，有一定优化，可进一步优化
    - 数据库接口
    - 测评系统（检查是否正确、打分系统、进行下一个游戏等）
    - 完善UI，（美化、按键等）
"""

import sys
from getWordList import getWordList
from Crossword import *
from getBestCrossword import *
import time
from ui_game import *

MAX_WORD_NUM = 8  # 一次最多选几个词
MIN_WORD_NUM = 5  # 一个填词游戏中最少几个词

# 根据单词列表生成填词游戏 （此为示例，待完成生词本接口）
start_time = time.time()
for i in range(1):  # 测试效率

    okay = False
    wordList = getWordList(MAX_WORD_NUM)
    # print(wordList)

    while not okay:
        cw = getBestCrossword(wordList)  # 根据要求生成较优的填词游戏
        if cw.placed.__len__() >= MIN_WORD_NUM:
            okay = True
        else:
            wordList = getWordList(MAX_WORD_NUM)


print('time lapsed:', time.time() - start_time)  # 打印花费的时间
# wordList = ['cotton', 'nothing', 'newspaper', 'loud', 'form','forward']

cw.display()  # 打印填词游戏

# cw.printPlacedList()  # 打印全部单词列表
defCross = cw.getDefCross()    # 打印横向单词列表，获取中文释义
defDown = cw.getDefDown()     # 打印纵向单词列表，获取中文释义
# print(cw.wordList)

# 开始创建GUI
app = QApplication(sys.argv)

window = gameWindow()  # 创建窗口
window.initUI(cw)
window.showCrossword()  # 显示空填词格
window.showDefinition(defCross, defDown)  # 显示中文释义
window.addLabel()  # 标号
window.addButtons()

window.show()

# start the event loop
app.exec_()
