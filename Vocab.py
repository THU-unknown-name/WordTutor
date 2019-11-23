from WordDict import WordDict
import pickle
import os

# 三种熟悉程度：NEW, UNFAMILIAR, FAMILIAR
FAMILIARITY_NEW = 0
FAMILIARITY_UNFAMILIAR = 1
FAMILIARITY_FAMILIAR = 2


class Vocab:
    """
    函数名：__init__
    参数：无
    作用：初始化函数
    返回值：无
    """

    def __init__(self):
        # 如果存在pickle文件，则直接从pickle文件中读取Vocab
        if os.path.exists('Vocab.pkl'):
            print("Existing Vocab......")
            pkl_file = open('Vocab.pkl', 'rb')
            self.__vocab_dict = pickle.load(pkl_file)
            pkl_file.close()

        # 如果还不存在pickle文件（即第一次使用程序），创建新的Vocab并且每个单词的熟悉度均设置为NEW
        else:
            self.wdDict = WordDict.WordDict()
            self.wdDict.load("WordDict/dict")
            self.wdDict.get_wordlist()
            print("Not Existing Vocab......")
            self.__vocab_dict = {}
            for key in self.wdDict.word_list:
                self.__vocab_dict[key] = FAMILIARITY_NEW

        # 为三种熟悉程度的单词分别创建一个列表，便于后续生成TodayList
        self.__newVocabList = []
        self.__unfamiliarVocabList = []
        self.__familiarVocabList = []
        for key in self.__vocab_dict.keys():
            if self.getFamiliarity(key) == FAMILIARITY_NEW:
                self.__newVocabList.append(key)
            elif self.getFamiliarity(key) == FAMILIARITY_UNFAMILIAR:
                self.__unfamiliarVocabList.append(key)
            else:
                self.__familiarVocabList.append(key)
        pass

    # 返回Vocab中的某一个单词word的信息
    def getInfo(self, word):
        """
        函数名：getInfo
        参数：word（如'afternoon'）
        作用：返回Vocab中的某一个单词word的信息
        返回值：list[information,extra]
        """
        return self.wdDict.get_info(word)

    # 返回Vocab中的某一个单词word的familiarity
    def getFamiliarity(self, word):
        """
         函数名：getFamiliarity
         参数：word（如'afternoon'）
         作用：返回Vocab中的某一个单词word的熟悉度
         返回值：0,1,2（NEW, UNFAMILIAR, FAMILIAR）
         """
        return self.__vocab_dict[word]

    # 更新Vocab中word的familiarity
    def updateFamiliarity(self, word, familiarity):
        """
         函数名：updateFamiliarity
         参数：word（如'afternoon'），familiarity（更新后的熟悉度）
         作用：更新Vocab中word的familiarity
         返回值：无
         """
        if familiarity < 0:
            self.__vocab_dict[word] = 0
        elif familiarity > 2:
            self.__vocab_dict[word] = 2
        else:
            self.__vocab_dict[word] = familiarity
        pass

    # 返回newVocabList（生词列表）
    def getNewVocabList(self):
        """
         函数名：getNewVocabList
         参数：无
         作用：返回newVocabList（生词列表）
         返回值：list（如['a', 'baby', 'cat'...]）
         """
        return self.__newVocabList

    # 返回unfamiliarVocabList（不熟悉单词列表）
    def getUnfamiliarVocabList(self):
        return self.__unfamiliarVocabList

    # 返回familiarVocabList（熟悉单词列表）
    def getFamiliarVocabList(self):
        return self.__familiarVocabList

    # 返回整个Vocab字典
    def getVocabDict(self):
        """
         函数名：getVocabDict
         参数：无
         作用：返回整个Vocab字典
         返回值：dict（如{'a'：'[...]', 'baby'：'[...]', 'cat'：'[...]',...}）
         """
        return self.__vocab_dict

    # 将Vocab存储到pickle文件（Vocab.pkl）中便于下次读取
    def saveVocab(self):
        output = open('Vocab.pkl', 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(self.__vocab_dict, output)
        output.close()
        pass

    # 显示vocab中所有项（调试时使用）
    def display(self):
        for item in self.__vocab_dict.items():
            print(item)
        pass

# 测试vocab是否成功初始化
# if __name__ == "__main__":
#     vocab = Vocab()
#     vocab.display()
#     vocab.saveVocab()
#     pass
