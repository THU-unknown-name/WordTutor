from random import sample

from WordDict import WordDict
import pickle
import os

# 三种熟悉程度：NEW, UNFAMILIAR, FAMILIAR
FAMILIARITY_NEW = 0
FAMILIARITY_UNFAMILIAR = 1
FAMILIARITY_FAMILIAR = 2

# 两种生成词库Vocab的方式
CREATE_NEW_VOCAB = 0
LOAD_EXISTING_VOCAB = 1


class Vocab:
    """
    函数名：__init__
    参数：WORD_DICT
    作用：初始化函数
    返回值：无
    """

    def __init__(self, WORD_DICT):
        self.__wdDict = WORD_DICT
        self.__record_path = 'StudyPlan/Vocab.pkl'

        # 如果存在pickle文件，则直接从pickle文件中读取Vocab
        if os.path.exists(self.__record_path):
            # print("Existing Vocab......\n")
            pkl_file = open(self.__record_path, 'rb')
            self.__vocab_dict = pickle.load(pkl_file)
            pkl_file.close()
            self.init_method = LOAD_EXISTING_VOCAB

        # 如果还不存在pickle文件（即第一次使用程序），创建新的Vocab并且每个单词的熟悉度均设置为NEW
        else:
            # print("Not Existing Vocab......\n")
            self.__vocab_dict = {}
            for key, _ in self.__wdDict.navigate():
                self.__vocab_dict[key] = FAMILIARITY_NEW
            self.init_method = CREATE_NEW_VOCAB

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
        return self.__wdDict.get_info(word)

    # 返回Vocab中的某一个单词word的familiarity
    def getFamiliarity(self, word):
        """
         函数名：getFamiliarity
         参数：word（如'afternoon'）
         作用：返回Vocab中的某一个单词word的熟悉度
         返回值：0,1,2（NEW, UNFAMILIAR, FAMILIAR）.如果word不在vocab中返回-1
         """
        if word in self.__vocab_dict.keys():
            return self.__vocab_dict[word]
        else:
            return -1

    # 更新Vocab中word的familiarity
    def updateFamiliarity(self, word, familiarity):
        """
         函数名：updateFamiliarity
         参数：word（如'afternoon'），familiarity（更新后的熟悉度）
         作用：更新Vocab中word的familiarity
         返回值：word如果不在词库中返回-1，否则返回word更新后的熟悉度
         """
        if word not in self.__vocab_dict.keys():
            # print('Word is not in the vocab!')
            return -1
        else:
            if familiarity < 0:
                self.__vocab_dict[word] = 0

            elif familiarity > 2:
                self.__vocab_dict[word] = 2
            else:
                self.__vocab_dict[word] = familiarity
            return self.__vocab_dict[word]

    # 返回newVocabList（生词列表）
    def getNewVocabList(self):
        """
         函数名：getNewVocabList
         参数：无
         作用：返回newVocabList（生词列表）
         返回值：list（如['a', 'baby', 'cat'...]）
         """
        self.__newVocabList = [k for k, v in self.__vocab_dict.items() if v == FAMILIARITY_NEW]
        return self.__newVocabList

    # 返回unfamiliarVocabList（不熟悉单词列表）
    def getUnfamiliarVocabList(self):
        self.__unfamiliarVocabList = [k for k, v in self.__vocab_dict.items() if v == FAMILIARITY_UNFAMILIAR]
        return self.__unfamiliarVocabList

    # 返回familiarVocabList（熟悉单词列表）
    def getFamiliarVocabList(self):
        self.__familiarVocabList = [k for k, v in self.__vocab_dict.items() if v == FAMILIARITY_FAMILIAR]
        return self.__familiarVocabList

    # 返回整个Vocab字典
    def getVocabDict(self):
        """
         函数名：getVocabDict
         参数：无
         作用：返回整个Vocab字典
         返回值：dict（如{'a'：0, 'baby'：1, 'cat'：2,...}）
         """
        return self.__vocab_dict

    # 将Vocab存储到pickle文件（StudyPlan/Vocab.pkl）中便于下次读取
    def saveVocab(self):
        output = open(self.__record_path, 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(self.__vocab_dict, output)
        output.close()
        pass

    # 确定一个单词是否为有效的单词
    def word_is_valid(self, word):
        if self.__wdDict.get_info(word) == WordDict.WORD_NOT_FOUND:
            return False
        else:
            return True

    # 为Vocab添加一个单词（添加单词默认熟悉度为0）
    def add_word_to_vocab(self, word):
        """
         函数名：add_word_to_vocab
         参数：添加的单词 word
         作用：为Vocab添加一个单词，且默认其熟悉度为0
         返回值：False（添加失败，比如输入的不是一个正确的单词） or True（添加成功）
         """
        if self.word_is_valid(word):
            self.__vocab_dict[word] = 0
            self.saveVocab()
            return True
        else:
            return False

    # 为Vocab删除一个单词
    def remove_word_from_vocab(self, word):
        """
         函数名：remove_word_from_vocab
         参数：删除的单词 word
         作用：为Vocab删除一个单词
         返回值：无
         """
        if not self.word_is_valid(word) or (word not in self.__vocab_dict.keys()):
            # print('Invalid word!')
            return False
        if not len(self.__vocab_dict) > 1:
            # print("词库中只有1个单词，无法删除")
            return False
        self.__vocab_dict.pop(word)
        self.saveVocab()
        return True

    # 从熟悉单词列表中随机抽取n个单词
    def get_n_word_from_familiarVocab(self, n):
        """
         函数名：get_n_word_from_familiarVocab
         参数：单词个数 n
         作用：从熟悉单词列表中随机抽取n个单词，供游戏环节使用
         返回值：list（如：['afternoon','cat',...].如果生成失败则返回空列表，可以通过检测返回列表的长度确定是否成功获取）
         """
        familiar_vocab_List = self.getFamiliarVocabList()
        if 0 < n <= len(familiar_vocab_List):
            return sample(familiar_vocab_List, n)
        else:
            return []

    # 显示vocab中所有项（调试时使用）
    # def display(self):
    #     for item in self.__vocab_dict.items():
    #         print(item)
    #     pass

# 测试vocab各项函数
# if __name__ == "__main__":
#     vocab = Vocab()
#     print("Number of vocabulary：", len(vocab.getVocabDict()),'\n')
#
#     print("******Testing method: add_word_to_vocab()******")
#     print("Is 'mechanical' in the vocab?:", ('mechanical' in vocab.getVocabDict().keys()))
#     print("Add word: mechanical......\n")
#     vocab.add_word_to_vocab('mechanical')
#     print("Is 'mechanical' in the vocab now?:", ('mechanical' in vocab.getVocabDict().keys()))
#     print("Number of vocabulary now：", len(vocab.getVocabDict()),'\n')
#
#     print("******Testing method: getInfo()******")
#     print("Info of 'a':", vocab.getInfo('a'))
#     print("Info of 'mechanical':", vocab.getInfo('mechanical'), '\n')
#
#     print("******Testing method: remove_word_from_vocab()******")
#     print("Is 'mechanical' in the vocab?:", ('mechanical' in vocab.getVocabDict().keys()))
#     print("Remove word: mechanical......\n")
#     vocab.remove_word_from_vocab('mechanical')
#     print("Is 'mechanical' in the vocab now?:", ('mechanical' in vocab.getVocabDict().keys()))
#     print("Number of vocabulary now：", len(vocab.getVocabDict()), '\n')
#
#     print("******Testing method: get_n_word_from_familiarVocab()******")
#     print("n=10:", vocab.get_n_word_from_familiarVocab(10), '\n')
#     vocab.saveVocab()
#     pass
