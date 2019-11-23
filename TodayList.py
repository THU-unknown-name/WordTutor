import Vocab
from random import sample


class TodayList:
    def __init__(self, vocab):
        """
        函数名：__init__
        参数：vocab（Vocab对象）
        作用：初始化函数
        返回值：无
        """
        self.__today_list = []
        self.__vocab_num = 5  # 每日背诵单词数，以常数为例。也可以自行输入一个整数

        # 三种类型词汇的列表
        newVocabList = vocab.getNewVocabList()
        unfamiliarVocabList = vocab.getUnfamiliarVocabList()
        familiarVocabList = vocab.getFamiliarVocabList()

        # 确认在todayList中每种词汇默认占多少
        # 默认分配是：60%new + 30%unfamiliar + 10%familiar
        # 如果某一项词数不够（比如刚开始背的时候或者基本背完的时候），用其他类型词来补充
        if len(newVocabList) >= int(self.__vocab_num * 0.6):
            self.__newVocab_num = int(self.__vocab_num * 0.6)
            if len(unfamiliarVocabList) >= int(self.__vocab_num * 0.3):
                self.__unfamiliarVocab_num = int(self.__vocab_num * 0.3)
                if len(familiarVocabList) >= int(self.__vocab_num * 0.1):
                    self.__familiarVocab_num = self.__vocab_num - self.__newVocab_num - self.__unfamiliarVocab_num
                else:
                    self.__familiarVocab_num = len(familiarVocabList)
                    self.__unfamiliarVocab_num = self.__vocab_num - self.__newVocab_num - self.__familiarVocab_num
            else:
                self.__unfamiliarVocab_num = len(unfamiliarVocabList)
                if len(familiarVocabList) >= int(self.__vocab_num * 0.1):
                    self.__familiarVocab_num = int(self.__vocab_num * 0.1)
                else:
                    self.__familiarVocab_num = len(familiarVocabList)
                self.__newVocab_num = self.__vocab_num - self.__familiarVocab_num - self.__unfamiliarVocab_num
        else:
            self.__newVocab_num = len(newVocabList)
            if len(unfamiliarVocabList) >= int(self.__vocab_num * 0.3):
                if len(familiarVocabList) >= int(self.__vocab_num * 0.1):
                    self.__familiarVocab_num = int(self.__vocab_num * 0.1)
                else:
                    self.__familiarVocab_num = len(familiarVocabList)
                self.__unfamiliarVocab_num = self.__vocab_num - self.__familiarVocab_num - self.__newVocab_num
            else:
                self.__unfamiliarVocab_num = len(unfamiliarVocabList)
                self.__familiarVocab_num = self.__vocab_num - self.__unfamiliarVocab_num - self.__newVocab_num

        # 测试用，打印每种词汇数量
        print(self.__familiarVocab_num, self.__unfamiliarVocab_num, self.__newVocab_num)

        # 将三种熟悉程度词汇依次添加到todayList中
        self.__today_list = sample(familiarVocabList, self.__familiarVocab_num)
        self.__today_list.extend(sample(unfamiliarVocabList, self.__unfamiliarVocab_num))
        self.__today_list.extend(sample(newVocabList, self.__newVocab_num))

    def getTodayList(self):
        """
         函数名：getTodayList
         参数：无
         作用：返回todayList（每日计划表）
         返回值：list（如['a', 'baby', 'cat'...]）
         """
        return self.__today_list


# 测试是否能够成功生成todayList
# if __name__ == "__main__":
#     vocab = Vocab.Vocab()
#     todayList = TodayList(vocab)
#     print(todayList.getTodayList())
#     pass

