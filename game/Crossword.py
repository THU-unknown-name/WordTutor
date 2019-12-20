import re
from random import choice

"""
20191128:
- 算法较为完善，无死循环
- 增加检查机制，避免死循环
- 放置单词时，从两个单词的所有交叉可能性中随机选取一种；此前为固定选取第一种可能性，导致算法不完备
- 结合优化机制，效率较高，见getBestCrossword.py
"""

class MyCrossword(object):
    def __init__(self):
        """
        self.crossword: 二维数组，存储填字游戏
        如果某个元素'#'则代表该格为空，如果为字母则为某个单词的一部分
        例如cue, camp, permission三个单词形成的填词游戏如下：
            [
            ['#', 'c', '#', 'c', '#', '#', '#', '#', '#', '#'],
            ['#', 'u', '#', 'a', '#', '#', '#', '#', '#', '#'],
            ['p', 'e', 'r', 'm', 'i', 's', 's', 'i', 'o', 'n'],
            ['#', '#', '#', 'p', '#', '#', '#', '#', '#', '#']
            ]
        打印效果：
            #c#c######
            #u#a######
            permission
            ###p######

        从数据库获取的单词列表需要通过self.generateCrossword(self, wordList)传递到self.wordList中

        self.sortedList: 字典，存储成功放入填词格的单词，按照首字母在棋盘格中的位置排序（左上角到右下角）
        其中每个词的value是一个列表，[[中文释义]，{单词长度}，{放置方向（横向0/纵向1），首字母位置，单词编号，中文排序次序}]
        例如：
        {'cue': [['线索'], {'len': 3}, {'dir': 1, 'startPos': [0, 1], 'id': 0, 'order': 1}],
        'campus': [['校园'], {'len': 6}, {'dir': 1, 'startPos': [0, 3], 'id': 1, 'order': 2}],
        'permission': [['允许'], {'len': 10}, {'dir': 0, 'startPos': [2, 0], 'id': 2, 'order': 3}]}

        self.listCross, self.listDown: 列表，分别存储横向和纵向单词列表，用于在UI中显示中文释义
        例如：
        self.listCross:
        [3, '允许', 'permission']  # [次序，中文释义，英文单词]

        self.listDown:
        [1, '线索', 'cue']
        [2, '校园', 'campus']
        """

        self.crossword = [[]]  # 存放填词游戏
        # self.bestCrossword = [[]]
        self.wordList = {}  # 单词列表
        self.nRow = self.crossword.__len__()  # 填词格行数
        self.nCol = self.crossword[0].__len__()  # 填词格列数
        self.placed = {}  # 记录已放置好的单词
        self.notPlaced = {}
        self.listCross = {}  # 横向单词
        self.listDown = {}  # 纵向单词
        self.sortedList = {}  # 完成放置的所有单词，按初始字母位置排序（从棋盘格的左上角到右下角）
        self.testMode = False


    def display(self):  # 打印填词游戏
        for i in range(self.nRow):
            newline = ''
            for j in range(0, self.nCol):
                newline = newline + self.crossword[i][j]
            print(newline)

    def printCrossword(self):  # 打印填词游戏（变量）
        print(self.crossword)

    def printWordList(self):  # 打印原始单词列表
        print('wordList:', self.wordList)

    def printPlacedList(self):  # 打印原始单词列表
        print('wordList:', self.sortedList)

    def generateCrossword(self, wordList):
        crossword = [[]]
        self.wordList = {}
        for word in wordList:
            self.wordList[word] = wordList[word] + [{}]
            self.wordList[word][2]['len'] = word.__len__()

        if self.testMode: print(self.wordList)

        sortedList = sorted(self.wordList, key=lambda d: d.__len__(), reverse=True)

        # for i, word in enumerate(sortedList):
        #     self.wordList[word][2]['id'] = i

        if self.testMode: print('sorted: ', sortedList)

        toBePlaced = sortedList  # 待放入棋盘格的单词

        if self.testMode: print('to be placed: ', toBePlaced)
        if self.testMode: print(' ')

        placed = {}  # 存放已经放入棋盘格的单词
        numChecked = 0  # 检查待放置队列是否循环，如果连续失败次数与队列长度相同，说明队列里所有单词均无法放置
        # 开始生成填字游戏
        while toBePlaced:
            new = toBePlaced[0]  # 取出待放置队列中的第一个

            new_len = new.__len__()
            isplaced = False  # 是否放置成功

            loc_x = None
            loc_y = None
            new_start_x = None
            new_start_y = None

            if not placed:  # 如果第一个单词，直接放入空棋盘格
                cur_dir = 0  # 初始单词方向为横向
                placed[new] = {'dir': cur_dir, 'startPos': [0, 0]}
                if cur_dir == 0:
                    # crossword.append([])
                    for i in range(0, new_len):
                        self.crossword[0].append(new[i])
                elif cur_dir == 1:
                    self.crossword.pop()
                    for i in range(0, new_len):
                        self.crossword.append([new[i]])
                toBePlaced.remove(new)

            else:
                for old in placed:  # 遍历已放置的单词，寻找重复的字母
                    if self.testMode: print('Placing:', new, ' Checking: ', old)
                    cur_dir = placed[old]['dir']  # 正在遍历的单词方向
                    self.nRow = self.crossword.__len__()
                    self.nCol = self.crossword[0].__len__()

                    intersect = self.getIntersectList(old, new)  # 两个单词交叉的所有可能性

                    # for letter in new:  # 遍历新单词的每一个字母
                    #     if old.find(letter) > -1:  # 如果与已放置单词有重合的字母
                    while intersect:
                        randInter = choice(intersect)  # 随机选取一个交叉方式
                        intersect.remove(randInter)

                        i_new = randInter[0]  # 重合字母在新单词中的位置
                        i_old = randInter[1]  # 重合字母在已放置单词中的位置

                        head = i_new  # 新单词中，交叉字母之前还有多少个字母
                        tail = new_len - i_new - 1  # 新单词中，交叉字母之后还有多少个字母

                        # 开始检查是否空余位置可以放置新单词
                        # 重合字母的坐标
                        if cur_dir == 0:  # cross 如果已放置单词是横向
                            loc_x = placed[old]['startPos'][0]
                            loc_y = placed[old]['startPos'][1] + i_old
                        elif cur_dir == 1:  # down 如果已放置单词是纵向
                            loc_x = placed[old]['startPos'][0] + i_old
                            loc_y = placed[old]['startPos'][1]
                        else:
                            print('ERROR IN PLACEMENT DIRECTION!')

                        crashed, ext_head, ext_tail = self.checkCrash(cur_dir, loc_x, loc_y, head, tail)

                        # 如果有重合单词且不会冲突，放置新单词
                        if crashed is False:
                            new_dir = 1 - cur_dir  # 新单词的方向

                            self.extendSize(new_dir, ext_head, ext_tail)

                            # 新单词首字母坐标
                            if new_dir == 1:  # down 纵向
                                new_start_x = loc_x - i_new + ext_head
                                new_start_y = loc_y
                            elif new_dir == 0:  # cross 横向
                                new_start_x = loc_x
                                new_start_y = loc_y - i_new + ext_head
                            else:
                                print('ERROR IN PLACEMENT DIRECTION!')

                            self.placeNewWord(new, new_dir, new_start_x, new_start_y)

                            isplaced = True  # 新单词已成功放置

                        if isplaced:  # 如果新单词成功放置，停止遍历
                            break
                    if isplaced:  # 如果新单词成功放置，停止遍历
                        break

                if isplaced is True:  # 更新单词列表
                    numChecked = 0
                    if self.testMode: print('+++++++ ', new, ' PLACED!\n')

                    # 更新已放置单词的首字母位置
                    for word in placed:
                        if new_dir == 1:  # down
                            placed[word]['startPos'][0] += ext_head
                        elif new_dir == 0:  # cross
                            placed[word]['startPos'][1] += ext_head

                    # 更新已放置单词列表
                    placed[new] = {'dir': new_dir, 'startPos': [new_start_x, new_start_y]}

                    # 将新单词从待放置队列中删除
                    toBePlaced.remove(new)

                else:  # 如果没有成功放置，将新单词放回队尾
                    if self.testMode: print('------- ', new, ' FAILED!\n')
                    toBePlaced.remove(new)
                    toBePlaced.append(new)
                    numChecked = numChecked + 1

                    if numChecked == toBePlaced.__len__():  # 连续放置失败次数与未放置队列长度相同，停止检查避免循环
                        if self.testMode: print('These words cannot be placed!')
                        if self.testMode: print(toBePlaced)
                        break

                if self.testMode: print('to be placed: ', toBePlaced)

        self.placed = placed
        self.nRow = self.crossword.__len__()
        self.nCol = self.crossword[0].__len__()
        # self.crossword = crossword
        if self.testMode: print(' ')
        if self.testMode: print('not placed: ', toBePlaced)
        if self.testMode: print('placed: ', self.placed)
        self.notPlaced = toBePlaced
        self.updateList()

        return crossword

    def getIntersectList(self, oldword, newword):
        # for old in placed:  # 遍历已放置的单词，寻找重复的字母
        List = []
        for i, letter in enumerate(newword):  # 遍历新单词的每一个字母
            for m in re.finditer(letter, oldword):
                List.append([i, m.start()])

        return List

    def extendSize(self, direction, ext_head, ext_tail):
        if direction == 1:  # down 纵向
            # 拓展棋盘格 insert new rows
            for i in range(ext_head):
                self.crossword.insert(0, ['#'] * self.nCol)

            for i in range(ext_tail):
                self.crossword.append(['#'] * self.nCol)

        elif direction == 0:  # cross 横向

            # 拓展棋盘格 insert new cols
            for i in range(0, self.nRow):
                # crossword.insert(0, ['#'] * crossword[0].__len__())
                for j in range(ext_head):
                    self.crossword[i].insert(0, '#')
                for j in range(ext_tail):
                    self.crossword[i].append('#')

        else:
            print('ERROR IN PLACEMENT DIRECTION!')

    def placeNewWord(self, word, direction, start_x, start_y):  # 单词，单词方向，起始坐标
        word_len = word.__len__()
        if direction == 1:  # down 纵向

            # place new word
            for i in range(word_len):
                self.crossword[start_x + i][start_y] = word[i]

        elif direction == 0:  # cross 横向

            # place new word
            for i in range(0, word_len):
                self.crossword[start_x][start_y + i] = word[i]
        else:
            print('ERROR IN PLACEMENT DIRECTION!')

    def checkCrash(self, cur_dir, loc_x, loc_y, head, tail):  # 当前已放置单词的方向，重合字母的坐标，新单词在重合字母前后还有多少字母
        crashed = False
        # 开始检查是否空余位置可以放置新单词
        if cur_dir == 0:  # cross 如果已放置单词是横向

            # check along previous rows
            for i in range(loc_x - head - 1, loc_x):
                if (i >= 0 and self.crossword[i][loc_y] is not '#') \
                        or (i == loc_x - head - 1 and i - 1 >= 0 and self.crossword[i - 1][loc_y] is not '#') \
                        or (i >= 0 and loc_y - 1 >= 0 and self.crossword[i][loc_y - 1] is not '#') \
                        or (i >= 0 and loc_y + 1 < self.nCol and self.crossword[i][loc_y + 1] is not '#'):
                    if self.testMode: print('Crashed!')
                    crashed = True
                    break

            # check following rows
            for i in range(loc_x + 1, loc_x + tail + 1):
                if i >= self.nRow:  # exceeding # row of current crossword
                    break

                elif self.crossword[i][loc_y] is not '#' \
                        or (i == loc_x + tail and i + 1 < self.nRow and self.crossword[i + 1][loc_y] is not '#') \
                        or (loc_y - 1 >= 0 and self.crossword[i][loc_y - 1] is not '#') \
                        or (loc_y + 1 < self.nCol and self.crossword[i][loc_y + 1] is not '#'):
                    if self.testMode: print('Crashed!')
                    crashed = True
                    break

            # 如果棋盘格不够大，需要在前/后分别增加多少列/行
            ext_head = max(0, head - loc_x)
            ext_tail = max(0, tail + loc_x + 1 - self.nRow)

            return crashed, ext_head, ext_tail

        elif cur_dir == 1:  # down 如果已放置单词是纵向

            # check along previous columns
            # for i in range(0, loc_y - head):
            for i in range(loc_y - head - 1, loc_y):
                if (i >= 0 and self.crossword[loc_x][i]) is not '#' \
                        or (i == loc_y - head - 1 and i -1 >= 0 and self.crossword[loc_x][i-1] is not '#')\
                        or (i >= 0 and loc_x - 1 >= 0 and self.crossword[loc_x - 1][i] is not '#') \
                        or (i >= 0 and loc_x + 1 < self.nRow and self.crossword[loc_x + 1][i] is not '#'):
                    if self.testMode: print('Crashed!')
                    crashed = True
                    break

            # check along following cols
            for i in range(loc_y + 1, loc_y + tail + 1):
                if i >= self.nCol:
                    break
                elif self.crossword[loc_x][i] is not '#' \
                        or (i == loc_y + tail and i + 1 < self.nCol and self.crossword[loc_x][i + 1] is not '#') \
                        or (loc_x - 1 >= 0 and self.crossword[loc_x - 1][i] is not '#') \
                        or (loc_x + 1 < self.nRow and self.crossword[loc_x + 1][i] is not '#'):
                    if self.testMode: print('Crashed!')
                    crashed = True
                    break

            # 如果棋盘格不够大，需要在前/后分别增加多少列/行
            ext_head = max(0, head - loc_y)
            ext_tail = max(0, tail + loc_y + 1 - self.nCol)

            return crashed, ext_head, ext_tail

    # 将已放置单词列表按照首字母位置排序，获取纵向单词列表和横向单词列表，方便与GUI对接
    def updateList(self):

        # 按照首字母位置排序
        tmp = {}
        for word in self.placed:
            cur_dir = self.placed[word]['dir']
            tmp[word] = [self.placed[word]['startPos'][0] * self.nCol + self.placed[word]['startPos'][1], cur_dir]

        getWordOrder = sorted(tmp.items(), key=lambda d: d[1][0])
        # print('getWordOrder: ', getWordOrder)

        # 将单词列表或划分为纵向和横向两个子列表
        tmp_pos = -1  # 如果有起始位置相同的单词，序号也相同
        tmp_order = 0
        for i, (word, param) in enumerate(getWordOrder):
            cur_dir = param[1]
            self.placed[word]['id'] = i
            if param[0] == tmp_pos:
                self.placed[word]['order'] = tmp_order
            else:
                self.placed[word]['order'] = tmp_order + 1

            self.sortedList[word] = [self.wordList[word][0], self.wordList[word][2], self.placed[word]]

            if cur_dir == 0:
                self.listCross[word] = self.sortedList[word]
            elif cur_dir == 1:
                self.listDown[word] = self.sortedList[word]

                if self.testMode: print('sortedList: ', self.sortedList)
            tmp_pos = param[0]
            tmp_order = self.placed[word]['order']


    # 获取所有单词的中文释义
    def getDefinitions(self, wordList):
        MAX_SPLIT = 4
        definitions = []
        for i, word in enumerate(wordList):
            raw_def = self.sortedList[word][0][0]
            tmp = raw_def.split('\n', MAX_SPLIT + 1)
            if MAX_SPLIT - 1 < tmp.__len__():

                if tmp[MAX_SPLIT - 1][tmp[MAX_SPLIT - 1].__len__() - 1] is '.' and MAX_SPLIT < tmp.__len__():
                    numShow = min(MAX_SPLIT + 1, tmp.__len__())
                else:
                    numShow = min(MAX_SPLIT, tmp.__len__())

            else:
                numShow = min(MAX_SPLIT, tmp.__len__())

            show_def = ''
            for i in range(numShow):
                if tmp[i][tmp[i].__len__() - 1] is '.':
                    if i != 0:
                        show_def += '\n    '
                    show_def += tmp[i]
                    show_def += ' '
                else:
                    show_def += tmp[i]

            if self.testMode: print(show_def)

            definitions.append([self.sortedList[word][2]['order'], show_def, word])

        return definitions

    def getDefAll(self, isPrint = False):
        definitions = self.getDefinitions(self.sortedList)
        if isPrint:
            print("all: ")
            for item in definitions:
                print(item)

            print('')
        return definitions

    # 获取横向单词的中文释义
    def getDefCross(self, isPrint = False):
        definitions = self.getDefinitions(self.listCross)
        if isPrint:
            print("cross: ")
            for item in definitions:
                print(item)

            print('')
        return definitions

    # 获取纵向单词的中文释义
    def getDefDown(self, isPrint = False):
        definitions = self.getDefinitions(self.listDown)
        if isPrint:
            print("down: ")
            for item in definitions:
                print(item)

            print('')
        return definitions
