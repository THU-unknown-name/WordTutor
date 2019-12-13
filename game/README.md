# WordTutor
Project for Software Engineering, THU 2019 Fall

Generate a crossword game from an example word list.

当前进度：给定单词，生成填词游戏并显示，增加了一些优化
待完成：
- [x] 生成填词游戏的算法不完备，待优化
- [ ] 数据库接口
- [ ] 测评系统（检查是否正确、打分系统、进行下一轮游戏等）
- [ ] 完善UI，（美化、按键等）

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
其中每个词的value是一个列表，[[中文释义]，{单词长度}，{放置方向（横向0/纵向1），首字母位置，排序次序}]  
例如：  
{'cue': [['线索'], {'len': 3}, {'dir': 1, 'startPos': [0, 1], 'order': 1}],    
'campus': [['校园'], {'len': 6}, {'dir': 1, 'startPos': [0, 3], 'order': 2}],  
'permission': [['允许'], {'len': 10}, {'dir': 0, 'startPos': [2, 0], 'order': 3}]}  

**self.listCross, self.listDown**: 列表，[次序，中文释义，英文单词]，分别存储横向和纵向单词列表，用于在UI中显示中文释义，例如：  
self.listCross:  
[3, '允许', 'permission']  

self.listDown:  
[1, '线索', 'cue']  
[2, '校园', 'campus']

### ui_game.py
包括MainWindow类，读取填字游戏生成游戏UI界面，目前仅显示空的填词格和中文释义

### getWordList.py
目前仅存放一个单词列表示例，待完成与生词本的接口

### mian.py
主程序
