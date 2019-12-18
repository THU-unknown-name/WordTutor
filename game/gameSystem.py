from getBestCrossword import *
from StudyPlan.Vocab import Vocab
from random import sample
from WordDict.WordDict import *

MAX_WORD_NUM = 8  # 一次最多选几个词
MIN_WORD_NUM = 5  # 一个填词游戏中最少几个词

def getWordList(num):
    WORD_DICT = WordDict()
    WORD_DICT.load('WordDict/dict')
    allWords = WORD_DICT.word_list
    randWords = sample(allWords, num)
    wordList = {}
    for word in randWords:
        wordList[word] = WORD_DICT.get_info(word)

    return wordList


def createGameFromAllWord():
    # 根据单词列表生成填词游戏
    okay = False
    wordList = getWordList(MAX_WORD_NUM)

    while not okay:
        cw = getBestCrossword(wordList)  # 根据要求生成较优的填词游戏
        if cw.placed.__len__() >= MIN_WORD_NUM:
            okay = True
        else:
            wordList = getWordList(MAX_WORD_NUM)

    return cw

def createGameFromStudy(WORD_DICT, errorWin):
    # 根据生词本生成填词游戏
    vocab = Vocab(WORD_DICT)
    word_list_for_game = vocab.get_n_word_from_familiarVocab(MAX_WORD_NUM)
    wordList = {}
    print('word_list_for_game: ', word_list_for_game)

    for word in word_list_for_game:
        word_mean = WORD_DICT.get_mean(word)
        if word_mean == WORD_NOT_FOUND:
            errorWin.show_error("The meaning of the word:{} not found".format(word))
            return
        wordList[word] = [[word_mean], {}]

    okay = False
    print('wordList:', wordList)

    while not okay:
        cw = getBestCrossword(wordList)  # 根据要求生成较优的填词游戏
        if cw.placed.__len__() >= MIN_WORD_NUM:
            okay = True
        else:
            wordList = getWordList(MAX_WORD_NUM)

    return cw

class myGame(object):
    def __init__(self):
        self.points = 0
