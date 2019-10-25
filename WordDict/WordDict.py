import os
import re

class WordDict:
	def __init__(self):
		'''
		__word_dict: dict
			key:英文单词
			value: [information, extra]
				information: [释义,发音]
				extra:{'例句'：[[例句1,例句1释义,例句1发音], ...],
						'形似词': ,
						...}
		'''
		self.__word_dict = {} #私有成员，只能在模块内调用，外部无法调用

		pass

	def load(self, rootpath):
		'''打开词库文件，录入WordDict中'''
		self.__rootpath=rootpath
		filepath = os.path.join(rootpath, 'WordList.txt')
		fs = open(filepath, 'r')
		for line in fs:
			word=line.strip()
			with open(os.path.join(rootpath,word)) as fWord:
				self.__word_dict[word]=eval(fWord.read())
		fs.close()
		
	def get_wordlist(self):
		'''获取整个词库所有的单词'''
		filepath = os.path.join(self.__rootpath,'WordList.txt')
		word_list = []
		fs = open(filepath, 'r')
		for line in fs:
			words = re.split(' ', line.strip())
			word_list += words
		fs.close()
		return word_list
		#return [word1,word2,...]

	def navigate(self):
		'''遍历词库
		output：
			yield (word,[information,extra])
		'''
		for word, info in self.__word_dict.items():
			yield (word,info)
		pass
		#yield (word,[information,extra])

	def match_word(self,word,matcher,parameter):
		'''匹配单词
		input：
			word：要匹配的单词
			matcher：匹配方法函数
			parameter：函数matcher的参数
		output：
			list[likelihood,word,information,extra]
		'''
		pass
		#return [likelihood,word,information,extra]

	def get_info(self,word):
		'''获取单词的信息
		input：
			word：单词
		output：
			list[information,extra]
		'''
		if word in self.__word_dict.keys():
			return self.__word_dict[word]
		else:
			#不在词典中，解决方案：1、上网爬取；2、显示错误信息
			return WORD_NOT_FOUND
		pass
		#return [information,extra]

	def get_sound(self, word):
		'''获取发音文件路径
		output：
			PathOfSound
		'''
		if word in self.__word_dict.keys():
			return self.__word_dict[word][0][1]
		else:
			return WORD_NOT_FOUND
		pass
		#return PathOfSound

	def update(self):
		'''更新词库
		'''
		pass

WORD_NOT_FOUND = -1
WORD_DICT = WordDict()
