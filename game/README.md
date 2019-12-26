# WordTutor
Project for Software Engineering, THU 2019 Fall  

从已经背过且记住的单词中抽取，生成填词游戏并显示；可点击“下一轮”开启新的游戏    

待完成：  
- [x] 记录每个单词的测试总正确率
- [x] 词库接口（改为与生词本对接）  
- [x] 完善UI  
    - [x] 填词游戏和中文释义可能会重叠  
    - [x] 按键：检查答案，错误显示红色  
    - [x] 按键：下一轮游戏  
    - [x] 光标debug  
- [x] 完备的填词游戏算法  
- [x] 数据库接口  
- [x] 每个词筛选部分释义显示  
- [x] UI背景，统一窗口大小  

### gameSystem.py - added on Dec 18, 2019  
原getWordList.py合并到这里  
- getWordListFromAll(num): 从全部词库中抽取单词，返回单词列表  
- getWordListFromAllWithInfo(num): 从全部词库中抽取单词，返回单词列表及其中文释义  
- getWordListFromStudy(WORD_DICT, errorWin): 从生词本中抽取单词，根据单词的历史测试正确率优先抽去正确率低的词，返回单词列表及其中文释义  
- getBestCrossword(wordList): 对特定的单词列表，生成最优填词游戏，返回MyCrossword类  
- updateGameHist(wordACC): 根据当前游戏更新pickle文件（单词的历史测试正确率）  
- updateWordTier(): 把已记住的单词按照历史测试正确率分为两级，优先抽区正确率低的词进行测试  
- saveGame(): 存储pickle文件  
- createGameFromAllWord(): 生成优化的填词游戏，保证总单词数不少于5个（从全部词库中抽取）  
- createGameFromStudy(WORD_DICT, errorWin): **供程序主函数使用**，生成优化的填词游戏，保证总单词数不少于5个（从生词本中抽取）  

### Game.pkl  
[dict, list]  
- dict: 所有单词的历史正确率, {'word:', [正确率, 正确次数, 总测试次数]}
- list: [[已记住但正确率低的词，优先抽取], [已记住且正确率高的词]]

### ui_game.py
包括gameWindow类，读取填词游戏，显示游戏及交互UI界面  
- 包括“检查答案”、“下一轮”、“退出”按键

### Crossword.py
包括MyCrossword类，用于存储、生成、读取填字游戏
**部分变量说明**:
**self.crossword**: 二维数组，存储填字游戏  
        如果某个元素'#'则代表该格为空，如果为字母则为某个单词的一部分  
        例如cue, camp, permission三个单词形成的填词游戏如下：  
            [  
            ['#', 'c', '#', 'c', '#', '#', '#', '#', '#', '#'],  
            ['#', 'u', '#', 'a', '#', '#', '#', '#', '#', '#'],  
            ['p', 'e', 'r', 'm', 'i', 's', 's', 'i', 'o', 'n'],  
            ['#', '#', '#', 'p', '#', '#', '#', '#', '#', '#']  
            ]  
        打印效果（这里没有等距显示...）：  
            #c#c######  
            #u#a######  
            permission  
            ###p######  

**self.generateCrossword(self, wordList)**: 把从数据库获取的单词列表传递到self.wordList中  

**self.sortedList**: 字典，存储成功放入填词格的单词，按照首字母在棋盘格中的位置排序（左上角到右下角）  
其中每个词的value是一个列表，[[中文释义]，{单词长度}，{放置方向（横向0/纵向1），首字母位置，与中文释义对应的编号，在单词列表中的排序次序}]  
例如：  
{'cue': [['线索'], {'len': 3}, {'dir': 1, 'startPos': [0, 1], 'order': 1, 'id': 0}],    
'campus': [['校园'], {'len': 6}, {'dir': 1, 'startPos': [0, 3], 'order': 2 'id': 1}],  
'permission': [['允许'], {'len': 10}, {'dir': 0, 'startPos': [2, 0], 'order': 3 'id': 2}]}   

**self.listCross, self.listDown**: 列表，[次序，中文释义，英文单词]，分别存储横向和纵向单词列表，用于在UI中显示中文释义，例如：  
self.listCross:  
[3, '允许', 'permission']  

self.listDown:  
[1, '线索', 'cue']  
[2, '校园', 'campus']  

### test.py  
测试程序，主要测试填词游戏生成算法的效率及UI界面的显示  
