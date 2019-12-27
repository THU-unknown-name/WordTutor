import time
import os
from game.Crossword import *
from StudyPlan.Vocab import Vocab
from random import sample
from WordDict.WordDict import *
import pickle

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
        # print('cur: ', os.getcwd())
        if os.path.exists('game'):
            self.__record_path = 'game/Game.pkl'
        else:
            self.__record_path = 'Game.pkl'
        self.game_data = []

        # 如果存在pickle文件，则直接从pickle文件中读取Game历史
        if os.path.exists(self.__record_path):
            # print("Existing Vocab......\n")
            pkl_file = open(self.__record_path, 'rb')
            self.game_data = pickle.load(pkl_file)
            self.vocab_dict = self.game_data[0]
            self.vocab_tier = self.game_data[1]
            self.updateWordTier()
            self.saveGame()
            pkl_file.close()

        # 如果还不存在pickle文件（即第一次使用程序），创建新的Game.pkl并且每个单词的正确率均设置为[0, 0, 0]
        else:
            # print("Not Existing Vocab......\n")
            self.vocab_dict = {}
            for word in self.allWords:
                self.vocab_dict[word] = [0, 0, 0]  # (正确率, 正确次数, 测试次数)

            self.vocab_tier = [[], []]
            self.game_data = [self.vocab_dict, self.vocab_tier]
            self.updateWordTier()
            self.saveGame()

    def updateGameHist(self, wordACC):
        '''
        # 更新单词的测试正确率
        :param wordACC: dict, {'word': True/False}, 本次游戏的结果
        '''
        # print('updating...')
        for word in wordACC:
            self.vocab_dict[word][2] += 1
            if wordACC[word] == True:
                self.vocab_dict[word][1] += 1

            self.vocab_dict[word][0] = self.vocab_dict[word][1] / self.vocab_dict[word][2]

        self.updateWordTier()
        self.saveGame()

    def updateWordTier(self):
        '''
        单词分为两个不同的优先级，供生成填词游戏时选取
        第一级：即最高级，熟悉但正确率低的词
        第二级：熟悉但正确率高的词
        :return:
        '''
        vocab = Vocab(self.WORD_DICT)
        famWords = vocab.getFamiliarVocabList()
        self.vocab_tier = [[], []]
        for word in famWords:
            if self.vocab_dict[word][0] < 0.5:
                self.vocab_tier[0].append(word)
            else:
                self.vocab_tier[1].append(word)

    def saveGame(self):
        '''
        更新单词的测试正确率，存储到pickle文件（game/Game.pkl）中便于下次读取
        '''
        output = open(self.__record_path, 'wb')
        pickle.dump(self.game_data, output)
        output.close()
        pass

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
        从生词本中获取单词列表及其释义，优先抽取测试正确率低的词，比例为3：1
        :param WORD_DICT: 词库
        :param errorWin: 传递报错信息
        :return:
        '''
        vocab = Vocab(WORD_DICT)
        len_fam_list = vocab.getFamiliarVocabList().__len__()

        n_tier_1 = round(3 / 4 * self.MAX_WORD_NUM)
        n_tier_2 = self.MAX_WORD_NUM - n_tier_1

        # 如果生词本现有词太少，从全部词库中随机抽取作为补充
        if len_fam_list < self.MAX_WORD_NUM:
            # print('add from dict!')
            word_list_for_game = vocab.get_n_word_from_familiarVocab(len_fam_list)
            tmp_list = vocab.getUnfamiliarVocabList()
            while word_list_for_game.__len__() < self.MAX_WORD_NUM:
                if tmp_list:
                    randWord = sample(tmp_list, 1)
                    tmp_list.remove(randWord[0])
                else:
                    randWord = self.getWordListFromAll(1)

                if randWord not in word_list_for_game:
                    word_list_for_game.append(randWord[0])

        else:
            try:
                if self.testMode: print(self.vocab_tier)
                word_list_for_game = sample(self.vocab_tier[0], n_tier_1) + sample(self.vocab_tier[1], n_tier_2)
            except:
                try:
                    if self.testMode: print('pick more from tier 1')
                    word_list_for_game = sample(self.vocab_tier[0], self.MAX_WORD_NUM - min(self.vocab_tier[1].__len__(), n_tier_2)) \
                                         + sample(self.vocab_tier[1], min(self.vocab_tier[1].__len__(), n_tier_2))
                except:
                    if self.testMode: print('pick more from tier 2')
                    word_list_for_game = sample(self.vocab_tier[0], min(self.vocab_tier[0].__len__(), n_tier_1)) + \
                                         sample(self.vocab_tier[1],
                                                self.MAX_WORD_NUM - min(self.vocab_tier[0].__len__(), n_tier_1))

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