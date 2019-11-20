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
        其中每个词的value是一个列表，[[中文释义]，{单词长度}，{放置方向（横向0/纵向1），首字母位置，排序次序}]
        例如：
        {'cue': [['线索'], {'len': 3}, {'dir': 1, 'startPos': [0, 1], 'order': 1}],
        'campus': [['校园'], {'len': 6}, {'dir': 1, 'startPos': [0, 3], 'order': 2}],
        'permission': [['允许'], {'len': 10}, {'dir': 0, 'startPos': [2, 0], 'order': 3}]}

        self.listCross, self.listDown: 列表，分别存储横向和纵向单词列表，用于在UI中显示中文释义
        例如：
        self.listCross:
        [3, '允许', 'permission']  # [次序，中文释义，英文单词]

        self.listDown:
        [1, '线索', 'cue']
        [2, '校园', 'campus']
        """

        self.crossword = [[]]  # 存放填词游戏
        self.wordList = []  # 单词列表
        self.nRow = self.crossword.__len__()  # 填词格行数
        self.nCol = self.crossword[0].__len__()  # 填词格列数
        self.placed = {}  # 记录已放置好的单词
        self.listCross = {}  # 横向单词
        self.listDown = {}  # 纵向单词
        self.sortedList = {}  # 完成放置的所有单词，按初始字母位置排序（从棋盘格的左上角到右下角）

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

    def generateCrossword(self, wordList):
        self.wordList = wordList
        for new in self.wordList:
            self.wordList[new][1]['len'] = new.__len__()
            # print(new, new.__len__())

        print(self.wordList)

        sortedList = sorted(self.wordList, key=lambda d: d.__len__(), reverse=True)

        print('sorted: ', sortedList)

        toBePlaced = sortedList  # 待放入棋盘格的单词

        print('to be placed: ', toBePlaced)
        print(' ')

        placed = {}  # 存放已经放入棋盘格的单词
        # 开始生成填字游戏
        while toBePlaced:
            new = toBePlaced[0]  # 取出待放置队列中的第一个

            new_len = new.__len__()
            isplaced = False  # 是否放置成功
            # crossed = False  # 是否与已放置的单词有交叉的字母
            # crashed = False  # 是否与其他单词的位置冲突

            loc_x = None
            loc_y = None
            i_old = None
            i_new = None
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
                isplaced = True
                toBePlaced.remove(new)

            else:
                crossed = False
                for old in placed:  # 遍历已放置的单词，寻找重复的字母
                    print('Placing:', new, ' Checking: ', old)
                    cur_dir = placed[old]['dir']  # 正在遍历的单词方向
                    self.nRow = self.crossword.__len__()
                    self.nCol = self.crossword[0].__len__()

                    crossed = False  # whether the new word intersect with the current words
                    crashed = False  # whether the new word will crash with other words
                    ext_head = None  # how many rows or columns need to be extended
                    ext_tail = None  # how many rows or columns need to be extended

                    for letter in new:  # 遍历新单词的每一个字母
                        crashed = False
                        if old.find(letter) > -1:  # 如果与已放置单词有重合的字母
                            crossed = True
                            i_old = old.find(letter)  # 重合字母在已放置单词中的位置
                            i_new = new.find(letter)  # 重合字母在新单词中的位置

                            head = i_new  # how many letters in the new word before the intersecting letter
                            tail = new_len - i_new - 1  # how many letters in the new word after the intersecting letter

                            # 开始检查是否空余位置可以放置新单词
                            if cur_dir == 0:  # cross 如果已放置单词是横向
                                # 重合字母的坐标
                                loc_x = placed[old]['startPos'][0]
                                loc_y = placed[old]['startPos'][1] + i_old

                                # check along previous rows
                                for i in range(loc_x - head - 1, loc_x):
                                    if (i >= 0 and self.crossword[i][loc_y] is not '#') \
                                            or (i >= 0 and loc_y - 1 >= 0 and self.crossword[i][loc_y - 1] is not '#') \
                                            or (i >= 0 and loc_y + 1 < self.nCol and self.crossword[i][loc_y + 1] is not '#'):
                                        print('Crashed!')
                                        crashed = True
                                        break

                                # check following rows
                                for i in range(loc_x + 1, loc_x + tail + 1):
                                    if i >= self.nRow:  # exceeding # row of current crossword
                                        break

                                    elif self.crossword[i][loc_y] is not '#' \
                                            or (loc_y - 1 >= 0 and self.crossword[i][loc_y - 1] is not '#') \
                                            or (loc_y + 1 < self.nCol and self.crossword[i][loc_y + 1] is not '#'):
                                        print('Crashed!')
                                        crashed = True
                                        break

                                # 如果棋盘格不够大，需要在前/后分别增加多少列/行
                                ext_head = max(0, head - loc_x)
                                ext_tail = max(0, tail + loc_x + 1 - self.nRow)

                            elif cur_dir == 1:  # down 如果已放置单词是纵向
                                # 重合字母的坐标
                                loc_x = placed[old]['startPos'][0] + i_old
                                loc_y = placed[old]['startPos'][1]

                                # check along previous columns
                                # for i in range(0, loc_y - head):
                                for i in range(loc_y - head - 1, loc_y):
                                    if (i >= 0 and self.crossword[loc_x][i]) is not '#' \
                                            or (i >= 0 and loc_x - 1 >= 0 and self.crossword[loc_x - 1][i] is not '#') \
                                            or (i >= 0 and loc_x + 1 < self.nRow and self.crossword[loc_x + 1][i] is not '#'):
                                        print('Crashed!')
                                        crashed = True
                                        break

                                # check along following cols
                                for i in range(loc_y + 1, loc_y + tail + 1):
                                    if i >= self.nCol:
                                        break
                                    elif self.crossword[loc_x][i] is not '#' \
                                            or (loc_x - 1 >= 0 and self.crossword[loc_x - 1][i] is not '#') \
                                            or (loc_x + 1 < self.nRow and self.crossword[loc_x + 1][i] is not '#'):
                                        print('Crashed!')
                                        crashed = True
                                        break

                                # # 如果棋盘格不够大，需要在前/后分别增加多少列/行
                                ext_head = max(0, head - loc_y)
                                ext_tail = max(0, tail + loc_y + 1 - self.nCol)

                            else:
                                print('ERROR IN PLACEMENT DIRECTION!')

                            # 如果有重合单词且不会冲突，放置新单词
                            if crossed is True and crashed is False:
                                new_dir = 1 - cur_dir  # 新单词的方向

                                if new_dir == 1:  # down 纵向

                                    # 拓展棋盘格 insert new rows
                                    for i in range(ext_head):
                                        self.crossword.insert(0, ['#'] * self.nCol)

                                    for i in range(ext_tail):
                                        self.crossword.append(['#'] * self.nCol)

                                    # 新单词首字母坐标
                                    new_start_x = loc_x - i_new + ext_head
                                    new_start_y = loc_y

                                    # place new word
                                    for i in range(new_len):
                                        replace = new[i]
                                        self.crossword[new_start_x + i][new_start_y] = replace

                                if new_dir == 0:  # cross 横向

                                    # 拓展棋盘格 insert new cols
                                    for i in range(0, self.nRow):
                                        # crossword.insert(0, ['#'] * crossword[0].__len__())
                                        for j in range(ext_head):
                                            self.crossword[i].insert(0, '#')
                                        for j in range(ext_tail):
                                            self.crossword[i].append('#')

                                            # 新单词首字母坐标
                                    new_start_x = loc_x
                                    new_start_y = loc_y - i_new + ext_head

                                    # place new word
                                    for i in range(0, new_len):
                                        self.crossword[new_start_x][new_start_y + i] = new[i]

                                isplaced = True  # 新单词已成功放置

                            if isplaced:  # 如果新单词成功放置，停止遍历
                                break

                    if isplaced:  # 更新单词列表
                        print('+++++++ ', new, ' PLACED!\n')

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
                        break

                    else:  # 如果没有成功放置，将新单词放回队尾
                        print('------- ', new, ' FAILED!\n')
                        toBePlaced.remove(new)
                        toBePlaced.append(new)

                    print('to be placed: ', toBePlaced)

        self.placed = placed
        self.nRow = self.crossword.__len__()
        self.nCol = self.crossword[0].__len__()
        # self.crossword = crossword
        print(' ')
        print('not placed: ', toBePlaced)
        print('placed: ', self.placed)
        self.updateList()

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
        for i, (word, param) in enumerate(getWordOrder):
            cur_dir = param[1]
            self.placed[word]['order'] = i + 1
            self.sortedList[word] = [self.wordList[word][0], self.wordList[word][1], self.placed[word]]
            if cur_dir == 0:
                self.listCross[word] = self.sortedList[word]
            elif cur_dir == 1:
                self.listDown[word] = self.sortedList[word]

        print('sortedList: ', self.sortedList)

    # 获取所有单词的中文释义
    def getDefAll(self):
        print("\nall: ")
        definitions = []
        for i, word in enumerate(self.sortedList):
            definitions.append([self.sortedList[word][2]['order'], self.sortedList[word][0][0], word])
            print(definitions[i])

    # 获取横向单词的中文释义
    def getDefCross(self):
        print("cross: ")
        definitions = []
        for i, word in enumerate(self.listCross):
            # print(self.listCross[word])
            definitions.append([self.listCross[word][2]['order'], self.listCross[word][0][0], word])
            print(definitions[i])

        print('')
        return definitions

    # 获取纵向单词的中文释义
    def getDefDown(self):
        print("down: ")
        definitions = []
        for i, word in enumerate(self.listDown):
            # print(self.listDown[word])
            definitions.append([self.listDown[word][2]['order'], self.listDown[word][0][0], word])
            print(definitions[i])

        print('')
        return definitions
