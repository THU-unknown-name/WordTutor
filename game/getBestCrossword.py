import time
from Crossword import *

# 获取最佳填词游戏（可增加更多优化方法）
"""
当前筛选机制为黑名单+时间限制，如果全部单词都成功放置，或剩余单词均在黑名单中，则视为最佳结果输出；如果运行达到时间限制，直接输出
可增加的优化机制：棋盘格大小，越小越好；棋盘格长宽比，1:1最好
测试效率：
- 9个单词，生成全部放置的填词游戏，执行100次花费0.2秒
- 10个单词，其中一个单词不可能放置，执行100次花费1.4秒（可调整要求来减少时间）
"""
testMode = False

time_threshold = 0.5  # 时间限制，如果还没有达到符合标准的结果，直接停止并输出当前结果

# 黑名单机制：如果有X次以上 某个单词都放置失败的话，则认为这个单词不适合生成填词游戏，拉黑这个单词
dump_threshold = 40  # 40次放置失败，则拉黑该单词
def getBestCrossword(wordList):

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
    while not okay and time.time() - start_time < time_threshold:
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
                    if dumpCount[word] >= dump_threshold:  # 当失败计数达到20次时，单词进入黑名单
                        dumpList.append(word)

        # 如果全部放置成功，或剩余单词均在黑名单中，认为是最优解，输出结果
        if not tmp.notPlaced or alldumped:
            okay = True

    if testMode: print('count:', count)
    return tmp