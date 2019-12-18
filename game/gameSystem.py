from game.getBestCrossword import *
from StudyPlan.Vocab import Vocab
from random import sample
from WordDict.WordDict import *

MAX_WORD_NUM = 8  # 一次最多选几个词
MIN_WORD_NUM = 5  # 一个填词游戏中最少几个词
# INIT_POINTS = 50
# COST_TIP = 100
# EARN_PER_WORD = 5

WORD_DICT = WordDict()
WORD_DICT.load('WordDict/dict')
allWords = WORD_DICT.word_list


def getWordListFromAll(num):
    '''
    :param num: 单词数量
    :return: list，单词列表
    '''
    randWords = sample(allWords, num)
    wordList = randWords

    return wordList


def getWordListFromAllWithInfo(num):
    '''
    :param num: 单词数量
    :return: dict，单词及其释义
    '''
    randWords = sample(allWords, num)
    wordList = {}
    for word in randWords:
        wordList[word] = WORD_DICT.get_info(word)

    return wordList

def getWordListFromStudy(WORD_DICT, errorWin):
    vocab = Vocab(WORD_DICT)
    len_fam_list = vocab.getFamiliarVocabList().__len__()

    # 如果生词本现有词太少，从全部词库中随机抽取作为补充
    if len_fam_list < MAX_WORD_NUM:
        word_list_for_game = vocab.get_n_word_from_familiarVocab(len_fam_list)

        while word_list_for_game.__len__() < MAX_WORD_NUM:
            randWord = getWordListFromAll(1)
            if randWord not in word_list_for_game:
                word_list_for_game.append(randWord[0])

    else:
        word_list_for_game = vocab.get_n_word_from_familiarVocab(MAX_WORD_NUM)

    wordList = {}

    for word in word_list_for_game:
        word_mean = WORD_DICT.get_mean(word)
        if word_mean == WORD_NOT_FOUND:
            errorWin.show_error("The meaning of the word:{} not found".format(word))
            return
        wordList[word] = [[word_mean], {}]

    return wordList


def createGameFromAllWord():
    '''
    根据单词列表生成填词游戏
    :return: Crossword类，填词游戏
    '''
    okay = False
    wordList = getWordListFromAllWithInfo(MAX_WORD_NUM)

    while not okay:
        cw = getBestCrossword(wordList)  # 根据要求生成较优的填词游戏
        if cw.placed.__len__() >= MIN_WORD_NUM:
            okay = True
        else:
            wordList = getWordListFromAllWithInfo(MAX_WORD_NUM)

    return cw


def createGameFromStudy(WORD_DICT, errorWin):
    '''
        根据生词本生成填词游戏
        :return: Crossword类，填词游戏
    '''
    wordList = getWordListFromStudy(WORD_DICT, errorWin)
    okay = False
    while not okay:
        cw = getBestCrossword(wordList)  # 根据要求生成较优的填词游戏
        if cw.placed.__len__() >= MIN_WORD_NUM:
            okay = True
        else:
            wordList = getWordListFromStudy(WORD_DICT, errorWin)

    return cw


class myGame(object):
    def __init__(self):
        self.points = 0
