from StudyPlan import TodayList
from StudyPlan import Vocab
import random

# 先生成词汇表vocab
vocab = Vocab.Vocab()

# 根据词汇表生成今日计划todayList
todayList = TodayList.TodayList(vocab).getTodayList()
print(todayList)  # 打印todayList检查是否符合要求

# 测试用代码，确认vocab中词汇的熟悉程度可以更新
familiarity = [0, 1, 2]
for key in vocab.getVocabDict().keys():
    vocab.updateFamiliarity(key, random.choice(familiarity))  # 给每个词随机赋予熟悉程度
vocab.display()
vocab.saveVocab()
