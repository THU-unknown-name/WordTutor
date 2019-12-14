import os
import pickle
import datetime

from StudyPlan import Vocab
from random import sample


class TodayList:
    def __init__(self, vocab):
        """
        函数名：__init__
        参数：vocab（Vocab对象）
        作用：初始化函数
        返回值：无
        """
        self.__total_vocab_num = len(vocab.getVocabDict())
        self.__today_list = []
        self.__date = datetime.date.today()
        self.new_user = False
        print("Today:", self.__date)

        # 模仿不同日期的代码（测试用）
        # self.__date = datetime.datetime.now()
        # print("Today:", self.__date)

        # 从pickle文件中读取当前存储的todaylist
        if os.path.exists('TodayList.pkl'):
            print("Existing TodayList......\n")
            pkl_file = open('TodayList.pkl', 'rb')
            todaylist_data = pickle.load(pkl_file)
            pkl_file.close()
            if self.__date == todaylist_data[3]:  # 如果当前打开程序和上次打开程序时同一天
                print("This run and last run are on the same day......")
                self.__vocab_num = todaylist_data[1]  # 读取出今天已有的计划表的各项数据
                self.__stated_vocab_num = todaylist_data[2]
                self.__today_list = todaylist_data[0]
                self.__current_word_index = todaylist_data[4]  # 记录上次背到哪一个单词

            else:  # 如果是新的一天第一次打开程序
                print("This run and last run are on the different day......")
                self.__vocab_num = todaylist_data[2]  # 读取前一天设定的每日计划表单词数量
                self.__stated_vocab_num = todaylist_data[2]  # 暂时不改变设定值
                self.__generate_today_list(vocab)  # 生成新的计划表
                self.__current_word_index = 0  # 之后从第1个单词开始背

        # 如果还不存在pickle文件（即第一次使用程序），新建TodayList完成初始化
        else:
            print("Not existing TodayList......\n")
            self.new_user = True
            # input_num = eval(input("输入每天需要背诵的单词数:"))
            # if not (0 <= self.__total_vocab_num and isinstance(input_num, int)):
            #     raise ValueError("设定计划表长度必须为小于等于词库总词数的正整数")  # 保证输入数据有效
            # self.__vocab_num = input_num
            # self.__stated_vocab_num = input_num
            # self.__generate_today_list(vocab)
            # self.__current_word_index = 0

    # 为新用户生成今日计划
    def plan_for_new_user(self, input_num, vocab):
        if not (0 <= self.__total_vocab_num and isinstance(input_num, int)):
            raise ValueError("设定计划表长度必须为小于等于词库总词数的正整数")  # 保证输入数据有效
        self.__vocab_num = input_num
        self.__stated_vocab_num = input_num
        self.__generate_today_list(vocab)
        self.__current_word_index = 0

    # 由词库生成每日计划
    def __generate_today_list(self, vocab):
        """
        函数名：__generate_today_list
        参数：vocab（Vocab对象）
        作用：由词库生成每日计划
        返回值：list（如['a','baby','cat'...]）
        """
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
        pass

    def getTodayList(self):
        """
         函数名：getTodayList
         参数：无
         作用：返回todayList（每日计划表）
         返回值：list（如['a', 'baby', 'cat'...]）
         """
        return self.__today_list

    # 设置每日计划表的长度（此设定从第二天开始实行）
    def set_stated_todaylist_length(self, length):
        """
         函数名：set_todaylist_length
         参数：设定的每日计划表长度length
         作用：设置每日计划表的长度
         返回值：无
         """
        if not (0 < length <= self.__total_vocab_num and isinstance(length, int)):
            raise ValueError("设定计划表长度必须为小于等于词库总词数的正整数")  # 保证输入数据有效
        self.__stated_vocab_num = length
        pass

    # 读取设定的每日计划表长度
    def get_stated_todaylist_length(self):
        return self.__stated_vocab_num

    # 更新当前背到了哪个单词（一般在程序退出时调用）
    def update_current_word(self, index):
        if not (0 <= index < self.__vocab_num and isinstance(index, int)):
            raise ValueError("当前背到的单词在列表中的下标设置有误")  # 保证输入数据有效
        self.__current_word_index = index
        pass

    # 获取当前背到了哪个单词（一般在同一天多次打开程序时调用）
    def get_current_word(self):
        return self.__current_word_index

    # 添加单词到每日计划中
    # ***注意：此时并没有添加到词库中！***
    def add_word_to_todaylist(self, word):
        """
         函数名：add_word_to_todaylist
         参数：添加的单词 word
         作用：添加单词到每日计划中
         返回值：无
         """
        if word not in self.__today_list:
            self.__today_list.append(word)
            self.__vocab_num += 1
            self.save_todaylist()
        pass

    def get_n_word_from_todaylist(self, n):
        """
        函数名：get_n_word_from_todaylist
        参数：单词个数 n
        作用：从每日计划中随机抽取n个单词，供游戏环节使用
        返回值：list（如：['afternoon','cat',...]）
        """
        return sample(self.__today_list, n)  # sample()函数本身自带异常处理

    # 将__today_list, __vocab_num, __stated_vocab_num, __date， __current_word_index等变量存到pickle文件中，运行时读取
    # ***注意：一定要在结束背单词的动作后执行该函数，保存数据！
    def save_todaylist(self):
        output = open('TodayList.pkl', 'wb')
        # Pickle dictionary using protocol 0.
        todaylist_data = [self.__today_list, self.__vocab_num, self.__stated_vocab_num, self.__date,
                          self.__current_word_index]
        pickle.dump(todaylist_data, output)
        output.close()
        pass


# 测试是否能够成功生成todayList
# if __name__ == "__main__":
#     if os.path.exists('TodayList.pkl'):
#         os.remove('TodayList.pkl')
#
#     vocab = Vocab.Vocab()
#     print("******Testing the initialization of TodayList******")
#     todayList = TodayList(vocab)
#     print(todayList.getTodayList(), '\n')
#     todayList.save_todaylist()
#
#     print("******Testing the pickle file of TodayList******")
#     todayList = TodayList(vocab)
#     print(todayList.getTodayList(), '\n')
#
#     print("******Testing the method: get_n_word_from_todaylist()******")
#     print("n=3:", todayList.get_n_word_from_todaylist(3), '\n')
#
#     print("******Testing the method: add_word_to_todaylist()******")
#     print("Is 'mechanical' in todaylist?:", ('mechanical' in todayList.getTodayList()))
#     print(todayList.getTodayList(), '\n')
#     print("Add word: mechanical......\n")
#     todayList.add_word_to_todaylist('mechanical')
#     print("Is 'mechanical' in todaylist now?:", ('mechanical' in todayList.getTodayList()))
#     print(todayList.getTodayList(), '\n')
#
#     # 此处一般模仿的是同一天多次打开软件，若模仿不同天打开软件，可在__init__改变日期的定义方法,采用下面代码进行测试
#     print("******Suppose we have recited some words******")
#     print("Update current_word...\n")
#     todayList.update_current_word(len(todayList.getTodayList())-3)
#     todayList.save_todaylist()
#     print("......Restart the app......\n")
#     todayList = TodayList(vocab)
#     print("Continue to recite todaylist:", todayList.getTodayList()[todayList.get_current_word():])
#
#     # 此处一般模仿的是不同天打开软件
#     # print("******Suppose we use the app on different day******")
#     # print("First day:", todayList.getTodayList())
#     # print("Current stated todaylist length:", todayList.get_stated_todaylist_length())
#     # todayList.set_stated_todaylist_length(todayList.get_stated_todaylist_length() + 1)
#     # print("Set the stated todaylist length:", todayList.get_stated_todaylist_length(), '\n')
#     # todayList.save_todaylist()
#     # print("......Restart the app......\n")
#     # todayList = TodayList(vocab)
#     # print("Second day:", todayList.getTodayList())
#     # print("Current stated todaylist length:", todayList.get_stated_todaylist_length())
#
#     pass
