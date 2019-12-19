import time
import os
from game.Crossword import *
from StudyPlan.Vocab import Vocab
from random import sample
from WordDict.WordDict import *


class gameSystem():
    def __init__(self, WORD_DICT):
        '''
        初始化gameSystem类，设置参数
        '''
        self.time_threshold = 0.5  # 用于getBestCrossword，时间上限，如果还没有达到符合标准的结果，直接停止并输出当前结果
        self.dump_threshold = 40  # 40次放置失败，则拉黑该单词
        self.MAX_WORD_NUM = 8  # 一次最多选几个词
        self.MIN_WORD_NUM = 5  # 一个填词游戏中最少几个词

        # 加载词库
        self.WORD_DICT = WORD_DICT
        # print(os.path.dirname(os.getcwd()))
        # self.WORD_DICT.load(os.path.dirname(os.getcwd()) + '/WordDict/dict')
        self.allWords = self.WORD_DICT.word_list

        self.testMode = False

    def getWordListFromAll(self, num):
        '''
        :param num: 单词数量
        :return: list，单词列表
        '''
        randWords = sample(self.allWords, num)
        wordList = randWords

        return wordList

    def getWordListFromAllWithInfo(self, num):
        '''
        :param num: 单词数量
        :return: dict，单词及其释义
        '''
        randWords = sample(self.allWords, num)
        wordList = {}
        for word in randWords:
            wordList[word] = self.WORD_DICT.get_info(word)

        return wordList

    def getWordListFromStudy(self, WORD_DICT, errorWin):
        '''
        从生词本中获取单词列表及其释义
        :param WORD_DICT: 词库
        :param errorWin: 传递报错信息
        :return:
        '''
        vocab = Vocab(WORD_DICT)
        len_fam_list = vocab.getFamiliarVocabList().__len__()

        # 如果生词本现有词太少，从全部词库中随机抽取作为补充
        if len_fam_list < self.MAX_WORD_NUM:
            word_list_for_game = vocab.get_n_word_from_familiarVocab(len_fam_list)

            while word_list_for_game.__len__() < self.MAX_WORD_NUM:
                randWord = self.getWordListFromAll(1)
                if randWord not in word_list_for_game:
                    word_list_for_game.append(randWord[0])

        else:
            word_list_for_game = vocab.get_n_word_from_familiarVocab(self.MAX_WORD_NUM)

        wordList = {}

        for word in word_list_for_game:
            word_mean = WORD_DICT.get_mean(word)
            if word_mean == WORD_NOT_FOUND:
                errorWin.show_error("The meaning of the word:{} not found".format(word))
                return
            wordList[word] = [[word_mean], {}]

        return wordList

    def getBestCrossword(self, wordList):
        """
        生成最优填词游戏
        当前筛选机制为黑名单+时间限制，如果全部单词都成功放置，或剩余单词均在黑名单中，则视为最佳结果输出；如果运行达到时间限制，直接输出
        可增加的优化机制：棋盘格大小，越小越好；棋盘格长宽比，1:1最好
        测试效率：
        - 9个单词，生成全部放置的填词游戏，执行100次花费0.2秒
        - 10个单词，其中一个单词不可能放置，执行100次花费1.4秒（可调整要求来减少时间）
        """
        dumpList = []  # 黑名单，记录被抛弃的单词
        dumpCount = {}  # 记录每个单词失败了几次
        for word in wordList:
            dumpCount[word] = 0

        okay = False  # 如果达到要求，停止生成，返回结果
        tmp = MyCrossword()  # 初始化

        start_time = time.time()  # 计时，测试用
        count = 0  # 计达到最佳结果的次数，测试用

        alldumped = True

        # 不断生成填字游戏，直到达到要求或达到时间限制
        while not okay and time.time() - start_time < self.time_threshold:
            count = count + 1  # 计数，测试用
            tmp = MyCrossword()
            tmp.generateCrossword(wordList)  # 生成填词游戏

            # 如果列表中有单词未被成功放置
            if tmp.notPlaced:
                alldumped = True
                for word in tmp.notPlaced:
                    if word not in dumpList:  # 如果不在黑名单中
                        alldumped = False
                        dumpCount[word] += 1  # 失败计数加一
                        if dumpCount[word] >= self.dump_threshold:  # 当失败计数达到20次时，单词进入黑名单
                            dumpList.append(word)

            # 如果全部放置成功，或剩余单词均在黑名单中，认为是最优解，输出结果
            if not tmp.notPlaced or alldumped:
                okay = True

        if self.testMode: print('count:', count)
        return tmp

    def createGameFromAllWord(self):
        '''
        根据单词列表生成填词游戏
        :return: Crossword类，填词游戏
        '''
        okay = False
        wordList = self.getWordListFromAllWithInfo(self.MAX_WORD_NUM)

        while not okay:
            cw = self.getBestCrossword(wordList)  # 根据要求生成较优的填词游戏
            if cw.placed.__len__() >= self.MIN_WORD_NUM:
                okay = True
            else:
                wordList = self.getWordListFromAllWithInfo(self.MAX_WORD_NUM)

        return cw

    def createGameFromStudy(self, WORD_DICT, errorWin):
        '''
            根据生词本生成填词游戏
            :return: Crossword类，填词游戏
        '''
        wordList = self.getWordListFromStudy(WORD_DICT, errorWin)
        okay = False
        while not okay:
            cw = self.getBestCrossword(wordList)  # 根据要求生成较优的填词游戏
            if cw.placed.__len__() >= self.MIN_WORD_NUM:
                okay = True
            else:
                wordList = self.getWordListFromStudy(WORD_DICT, errorWin)

        return cw