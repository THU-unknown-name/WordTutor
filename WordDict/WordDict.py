import os
import re
import numpy as np
from . import Grep
from . import Extract

class WordDict:
	def __init__(self):
		'''
		__word_dict: dict\n
			key:英文单词\n
			value: [information, extra]\n
				information: [释义,发音]\n
				extra:{'例句'：[[例句1,例句1释义,例句1发音], ...],\n
						'形似词': ,\n
						...}
		'''
		self.__word_dict = {}		#私有成员，只能在模块内调用，外部无法调用
		self.__rootpath = ""		#词库根目录
		self.word_list = []			#单词目录
		pass

	def load(self, rootpath):
		'''打开词库文件，录入WordDict中\n
		input:\n
			rootpath:词库根目录
		if succeed:\n
			return WORD_DICT_LOAD_SUCCEED
		else:\n
			return error_message'''
		self.__rootpath=rootpath
		load_wordlist = self.get_wordlist()
		if load_wordlist != GET_WORDLIST_SUCCEED:
			return load_wordlist
		for word in self.word_list:
			try:
				with open(os.path.join(rootpath,word), encoding='utf-8') as fWord:
					self.__word_dict[word]=eval(fWord.read())
			except FileNotFoundError:
				return "File {} not found".format(os.path.join(rootpath,word))
			except IsADirectoryError:
				return "{} is not a directory".format(os.path.join(rootpath,word))
			except PermissionError:
				return "you are denied to open file {}".format(os.path.join(rootpath,word))
		return WORD_DICT_LOAD_SUCCEED
		
	def get_wordlist(self):
		'''获取整个词库所有的单词\n
		if succeed:\n
			return GET_WORDLIST_SUCCEED
		else:\n
			return error_message'''
		filepath = os.path.join(self.__rootpath,'WordList.txt')
		word_list = []
		try:
			fs = open(filepath, 'r')
		except FileNotFoundError:
			return "File {} not found".format(filepath)
		except IsADirectoryError:
			return "{} is not a directory".format(filepath)
		except PermissionError:
			return "you are denied to open file {}".foemat(filepath)
		else:
			for line in fs:
				words = re.split(' ', line.strip())
				word_list += words
			fs.close()
			self.word_list = word_list
			return GET_WORDLIST_SUCCEED

	def navigate(self):
		'''遍历词库\n
		output：\n
			yield (word,[information,extra])
		'''
		for word, info in self.__word_dict.items():
			yield (word,info)
		pass
		#yield (word,[information,extra])

	def match_word(self,word):
		'''匹配单词\n
		input：\n
			word：要匹配的单词\n
		output：\n
			list[likelihood,wordlist]:\n
				likelihood:与wordlist中的单词的匹配度\n
				wordlist:单词列表，word与wordlist中的单词分别进行匹配
		'''
		wordlist = self.word_list
		likelihood = np.zeros(len(wordlist))		#相似度
		for num in range(len(wordlist)):
			mword = wordlist[num]
			if mword[0] != word[0]:
				likelihood[num] = float('inf')		#首字母不相同，相似度为正无穷
			elif mword == word:
				likelihood[num] = 0					#单词相同，相似度为0
			else:
				[likelihood[num],_] = self.matcher(mword, word)#首字母相同，求相似度

		return [likelihood,wordlist]

	def matcher(self, template_str, match_str):	
		'''采用DTW算法进行字符串匹配\n
		input:\n
			template_str:模板字符串\n
			match_str:需要匹配的字符串\n
		output:\n
			list[score, match]:\n
				score:匹配度，值越小匹配度越高，最小为0\n
				match:匹配情况
		'''
		W = np.zeros(len(template_str))						#DTW算法中的权值
		tstr_len = len(template_str)
		mstr_len = len(match_str)
		match_path = np.zeros([tstr_len, mstr_len], int)	#记录DTW算法路径
		errornum = np.zeros(tstr_len)						#记录连续不相等的的字母个数
		for i in range(mstr_len):
			for j in range(1, tstr_len + 1):
				minW = np.argmin(W[:tstr_len-j+1])			#当前权值最小的位置
				if(template_str[-j] != match_str[i]):		#
					errornum[-j] += 1
				else:
					errornum[-j] = 0
				W[-j] = W[minW] + pow(tstr_len-j-i, 2) + pow(errornum[-j], 2)
				match_path[-j][i] = minW
			#print(W)
		#print(match_path)
		path = np.zeros(mstr_len, int)
		stage = tstr_len - 1
		path[-1] = stage
		for j in range(2, mstr_len + 1):
			path[-j] = match_path[stage][-j+1]
		#print(path)
		match = [[],[]]
		i = 0
		while i < mstr_len - 1:
			j = i + 1
			while (j < mstr_len) and (path[i] == path[j]):
				j += 1
			if j == mstr_len:
				match[1].append(match_str[i:j])
				match[0].append(template_str[path[i]])
			else:
				match[1].append(match_str[i:j])
				match[0].append(template_str[path[i]:path[j]])
			i = j
		if i == mstr_len - 1:
			match[1].append(match_str[-1])
			match[0].append(template_str[path[-1]])
		return [W[-1], match]
		pass

	def get_info(self,word):
		'''获取单词的信息\n
		input：\n
			word：单词\n
		if succeed:\n
			return list[information,extra]\n
		else:\n
			return WORD_NOT_FOUND
		'''
		if word in self.__word_dict.keys():
			return self.__word_dict[word]
		else:
			#不在词典中，解决方案：1、上网爬取；2、显示错误信息
			lSpace=Grep.Get(word,Grep.Info)
			if lSpace!=None:
				return Extract.Extract(lSpace)
			else:
				return WORD_NOT_FOUND
		pass
		#return [information,extra]

	def get_sound(self, word):
		'''获取发音文件路径\n
		output：\n
			PathOfSound
		'''
		if word in self.__word_dict.keys():
			return self.__word_dict[word][0][1]
		else:
			return WORD_NOT_FOUND
		pass
		#return PathOfSound

	@staticmethod
	def update(wordlist,rootpath):
		'''更新词库\n
		input: \n
			wordlist: Danngo \n
			rootpath: root path to store greped word
		'''
		result=[]
		with open(wordlist,"r") as fSource:
			for sLine in fSource:
				sSpace=sLine.strip()
				if len(sSpace)>0:
					result.append([sSpace])
		while True:
			def CallBack(iIndex):
				print(">>%d/%d"%(iIndex+1,len(result)))
			Grep.Update(result,CallBack)
			iCount=0
			for iLoop1 in range(len(result)):
				if len(result[iLoop1])>1:
					iCount+=1
			print("%d/%d"%(iCount,len(result)))
			if iCount>=len(result):
				break

		with open(os.path.join(rootpath,'Original.txt'),"w") as fSave:
			fSave.write(str(result))

		Extract.ExtractToDir(result,rootpath)

WORD_NOT_FOUND = -1
WORD_DICT_LOAD_SUCCEED = 1
GET_WORDLIST_SUCCEED = 1

if __name__ == "__main__":
	WORD_DICT = WordDict()
	load_err = WORD_DICT.load('HappyWordTutorial\WordDict\dict')
	if load_err != WORD_DICT_LOAD_SUCCEED:
		print(load_err)
		exit(0)
	[W, match] = WORD_DICT.matcher('afternoon', 'after')
	print(W)
	print(match)
	[likelihood, wordlist] = WORD_DICT.match_word('afternoon')
	top5index = np.argsort(likelihood)[:5]
	top5word = [wordlist[i] for i in top5index]
	print(top5word)
	pass

