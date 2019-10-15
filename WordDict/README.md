# 词库
## 基本功能接口介绍
词库信息将存于class WordDict的私有成员__word_dict: dict中：
+ key:英文单词
+ value: [information, extra]
	+ information: [释义,发音]
	+ extra:{'例句'：[[例句1,例句1释义,例句1发音], ...],
	         '形似词': ,
	         ...}

函数：
+ load(self, rootpath):打开词库文件，录入WordDict中；rootpath为程序运行根目录
+ get_wordlist(self):获取整个词库所有的单词
+ navigate(self):遍历词库
+ match_word(self,word,matcher,parameter):匹配单词
+ get_info(self,word):获取单词的信息
+ get_sound(self, word):获取发音文件路径
+ update(self):更新词库
## 词库爬取方式
Run Grep.py to grep information of words stored in utf-8.txt and store the result into save.txt
The current format used to store in save.txt is a list printed as string.
+ The first dimension of the list defines diffrent records for words
+ The second dimension of the lis defines the different aspects of information for the word.
	+ 0 -> Word: The word
	+ 1 -> Pronounciation: The pronounciation of the word
	+ 2 -> Explanation: Chinese meaning
	+ 3 -> Example: Example sentenses
Usage:
+ Run Grep.py.
	+ Input -2 to grep Inforamtion of words stored in utf-8.txt or upgrade the current List.
		+ Failure may occur during this procedure, just input and run again to fill in the missing entries.
	+ Input -1 to save the current greped information(word list included).
	+ Input a non-negative number to see the details of a specific entry(in the order of storage in List).
		+ Attention, if the ubound exceed the count of entries, the program would crash.
	+ Input a negative number less than -2 to exit.

