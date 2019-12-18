# 此为示例，待完成生词本接口
from WordDict import WordDict
from random import choice, sample

# 读取词库
WORD_DICT = WordDict.WordDict()
WORD_DICT.load('WordDict/dict')
allWords = WORD_DICT.word_list

def getWordList(num):

    randWords = sample(allWords, num)
    wordList = {}
    for word in randWords:
        wordList[word] = WORD_DICT.get_info(word)

    return wordList

# print(WORD_DICT.get_info('campus'))
# print(WORD_DICT.word_list)


# wordList = {
#             'permission': [['允许'], {}],
#             'campus': [['校园'], {}],
#             'agonize': [['痛'], {}],
#             'cue': [['线索'], {}],
#             'audible': [['听'], {}],
#             'innocent': [['无辜'], {}],
#             'minister': [['牧师'], {}],
#             'taxi': [['出租车'], {}],
#             'iterator': [['迭代器'], {}],
#             'yyy': ['test',{}]
#             }


# 'zzzfe': ['test',{}]

