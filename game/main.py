# 当前进度：给定单词，生成填词游戏并显示
# 待完成：
# - 生成填词游戏的算法较为完备，有一定优化，可进一步优化
# - 数据库接口
# - 测评系统（检查是否正确、打分系统、进行下一个游戏等）
# - 完善UI，（美化、按键等）

import sys
from getWordList import wordList
from Crossword import *
from getBestCrossword import *
import time
from ui_game import *

# 根据单词列表生成填词游戏 （此为示例，待完成生词本接口）
start_time = time.time()
for i in range(100):  # 测试效率
    cw = getBestCrossword(wordList)  # 根据要求生成较优的填词游戏

print('time lapsed:', time.time() - start_time)  # 打印花费的时间

cw.display()  # 打印填词游戏
cw.printCrossword()  # 打印填词游戏变量

cw.printPlacedList()  # 打印全部单词列表
defCross = cw.getDefCross()    # 打印横向单词列表，获取中文释义
defDown = cw.getDefDown()     # 打印纵向单词列表，获取中文释义

# 开始创建GUI
app = QApplication(sys.argv)

window = MainWindow()  # 创建窗口
window.initUI()
window.showCrossword(cw)  # 显示空填词格
window.showDefinition(defCross, defDown)  # 显示中文释义
window.addLabel(cw)  # 标号
window.show()

# start the event loop
app.exec_()
