"""
    黑盒测试
"""

import time
import sys
from game.gameSystem import *
from game.Crossword import *
from random import choice
from WordDict.WordDict import *
from mymainwindow import ErrorWin
from game.ui_game import *

MAX_WORD_NUM = 8  # 一次最多选几个词

WORD_DICT = WordDict()
WORD_DICT.load(os.path.dirname(os.getcwd()) + '/WordDict/dict')


def testGenerateCrossword(num_word):
    print('Running testGenerateCrossword()...')

    myGame = gameSystem(WORD_DICT)
    start_time = time.time()
    wordList = myGame.getWordListFromAllWithInfo(num_word)

    cw = MyCrossword()
    cw.generateCrossword(wordList)
    cw.display()

    print('Crossword generated!')
    if cw.crossword:
        print('Test passed! Time lapsed:', time.time() - start_time)


# 测试随机选取8个单词，生成填词游戏
testGenerateCrossword(8)
print('')


def testBestCrossword(num_test):
    print('Running testBestCrossword()...')
    print('Randomly picking 6 - 10 words...')
    print('Generating crossword', num_test, 'times...')
    count_times, count_fewwords, count_allplaced = 0, 0, 0
    MIN_WORD_NUM = 5  # 一个填词游戏中最少几个词
    myGame = gameSystem(WORD_DICT)
    start_time = time.time()
    for i in range(num_test):
        num_word = choice(range(6, 11))
        wordList = myGame.getWordListFromAllWithInfo(num_word)
        cw = myGame.getBestCrossword(wordList)  # 根据要求生成较优的填词游戏

        # 循环直到生成符合要求的填词游戏
        okay = False
        while not okay:
            if cw.placed.__len__() >= MIN_WORD_NUM:
                okay = True
            else:
                wordList = myGame.getWordListFromAllWithInfo(num_word)
                cw = myGame.getBestCrossword(wordList)

        if not cw.crossword:
            print('生成失败！')
        elif cw.crossword and cw.placed.__len__() < MIN_WORD_NUM:
            print('单词少于', str(MIN_WORD_NUM), '个！')
            count_fewwords += 1
        else:
            count_times += 1
            if cw.placed.__len__() == num_word:
                count_allplaced += 1

    print(count_times, 'test passed! Time lapsed:', time.time() - start_time)
    print(count_fewwords, 'crosswords have less than', MIN_WORD_NUM, 'words')
    print(count_allplaced, 'crosswords placed all words in the list')


# 从词库中随机选取6-10个单词，生成填词游戏，要求：最终结果包含不少于5个单词
num_test = 100  # 进行100次
testBestCrossword(num_test)


# GUI测试，从全部词库中随机抽取，生成并显示填词游戏
myGame = gameSystem(WORD_DICT)
cw = myGame.createGameFromAllWord()

app = QApplication(sys.argv)

ui_game = gameWindow()
errorWin = ErrorWin()
ui_game.initUI(cw, WORD_DICT, errorWin)
ui_game.setStyleSheet("#MainWindow{border-image:url(%s/bak1.jpg)}" % os.path.dirname(os.getcwd()))
ui_game.show()

app.exec_()

