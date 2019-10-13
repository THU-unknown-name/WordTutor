# 词库
## 基本功能接口介绍
词库信息将存于数据(dict) WordDict中：
+ key:英文单词
+ value: [information, extra]
	+ information: [释义,发音]
	+ extra:{'例句'：[[例句1,例句1释义,例句1发音], ...],
	         '形似词': ,
	         ...}

函数：
+ Open(self,DictPath):打开词库文件，录入WordDict中
+ ListOfWord(self):获取整个词库所有的单词
+ Navigate(self):遍历词库
+ MatchWord(self,word,matcher,parameter):匹配单词
+ GetInfo(self,word):获取单词的信息
+ GetSound(self, word):获取发音文件路径
+ update(self):更新词库
## 词库爬取方式
