import os
import re
import copy
import numpy as np
from WordDict import Grep
from WordDict import Extract

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
		likelihood = np.zeros(len(wordlist), dtype='int')		#相似度
		for num in range(len(wordlist)):
			mword = wordlist[num]
			if mword[0] != word[0]:
				#首字母不相同，相似度为正无穷
				likelihood[num] = 65535
			elif mword == word:
				#单词相同，相似度为0
				likelihood[num] = 0
			else:
				#首字母相同，求相似度
				[likelihood_0, _] = self.matcher0(mword, word)
				[likelihood_1, _] = self.matcher0(word, mword)
				likelihood[num] = min(likelihood_0, likelihood_1)

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
		tstr_len = len(template_str)
		mstr_len = len(match_str)
		if(tstr_len == 0 or mstr_len == 0):
			return 'The inputs must be strings'
		matchs = [[[template_str[0]], [match_str[0]]]]
		Wold = np.zeros(tstr_len, dtype='int')
		Wnew = np.zeros(tstr_len, dtype='int')
		error_block = np.zeros(tstr_len, dtype='int')
		minW = 0
		for i in range(1, tstr_len):
			matchs.append([[template_str[0]], [match_str[0]]])
			matchs[i][0].append(template_str[1:i+1])
			matchs[i][1].append('')
			error_block[i] = 1
			Wnew[i] = 2 + (1 << i)
		for i in range(1, mstr_len):
			for j in range(1, tstr_len + 1):
				minW = np.argmin(Wnew[:tstr_len-j+1])
				matchs[-j] = copy.deepcopy(matchs[minW])
				error_block[-j] = error_block[minW]
				if(minW == tstr_len - j):
					matchs[-j][1][-1] += match_str[i]
					matchs[-j][0][-1] = template_str[minW]
					#Wnew[-j] = Wold[minW]
					#if(matchs[-j][0][-1] != matchs[-j][1][-1]):
					Wnew[-j] = Wold[minW] + (1 << len(matchs[-j][1][-1])) + \
						(1 << (error_block[-j] + 1))
				else:
					if(matchs[-j][0][-1] != matchs[-j][1][-1]):
						error_block[-j] += 1
					if(minW < tstr_len - j - 1):
						matchs[-j][0].append(template_str[minW+1:-j])
						matchs[-j][1].append('')
						error_block[-j] += 1
						Wnew[-j] = Wnew[minW] + (1 << (tstr_len - j - minW - 1)) + \
							(1 << error_block[-j])
						Wold[-j] = Wnew[-j]
					else:
						Wnew[-j] = Wnew[minW]
						Wold[-j] = Wnew[-j]
					matchs[-j][0].append(template_str[-j])
					matchs[-j][1].append(match_str[i])
					if(template_str[-j] != match_str[i]):
						Wnew[-j] += 2 + (1 << (error_block[-j] + 1))
			#print(matchs)
		for i in range(tstr_len-1):
			matchs[i][0].append(template_str[i+1:])
			matchs[i][1].append('')
			Wnew[i] += (1 << (len(matchs[i][0][-1]) >> 1)) + \
				(1 << (error_block[i] + 1))
		#print(matchs)
		minW = np.argmin(Wnew)
		return [Wnew[minW], matchs[minW]]
		pass

	def matcher0(self, template_str, match_str):	
		'''采用DTW算法进行字符串匹配\n
		input:\n
			template_str:模板字符串\n
			match_str:需要匹配的字符串\n
		output:\n
			list[score, match]:\n
				score:匹配度，值越小匹配度越高，最小为0\n
				match:匹配情况
		'''
		tstr_len = len(template_str)
		mstr_len = len(match_str)
		if(tstr_len == 0 or mstr_len == 0):
			return 'The inputs must be strings'
		elif(tstr_len == 1 or mstr_len == 1):
			if tstr_len == 1:
				matchs = [[template_str[0], ''], [match_str[0], match_str[1:]]]
			else:
				matchs = [[template_str[0], template_str[1:]], [match_str[0], '']]
			return [(1 << abs(tstr_len - mstr_len)) + 2, matchs]
		Wold = np.zeros(tstr_len, dtype='int')
		Wnew = np.zeros(tstr_len, dtype='int')
		error_block = np.zeros(tstr_len, dtype='int')
		minW = 0
		matchs = [[[template_str[0]], [match_str[0:2]]]]
		matchs.append([[template_str[0], template_str[1]], [match_str[0], match_str[1]]])
		Wnew[0] = 6
		if(template_str[1] != match_str[1]):
			Wnew[1] = 4
			error_block[1] = 1
		for i in range(2, tstr_len):
			matchs.append([[template_str[0]], [match_str[0]]])
			matchs[i][0].append(template_str[1:i])
			matchs[i][1].append('')
			matchs[i][0].append(template_str[i])
			matchs[i][1].append(match_str[1])
			error_block[i] = 1
			Wold[i] = 2 + (1 << (i - 1))
			Wnew[i] = 2 + (1 << (i - 1))
			if(template_str[i] != match_str[1]):
				Wnew[i] += 2

		for i in range(2, mstr_len):
			for j in range(1, tstr_len + 1):
				matchs_tmp = []
				Wnew_tmp = np.zeros(tstr_len-j+1, dtype='int')
				Wold_tmp = np.zeros(tstr_len-j+1, dtype='int')
				error_block_tmp = np.zeros(tstr_len-j+1, dtype='int')
				for minW in range(0, tstr_len-j+1):
					matchs_tmp.append(copy.deepcopy(matchs[minW]))
					error_block_tmp[minW] = error_block[minW]
					if(minW == tstr_len - j):
						matchs_tmp[minW][1][-1] += match_str[i]
						matchs_tmp[minW][0][-1] = template_str[minW]
						Wnew_tmp[minW] = Wold[minW] + (1 << len(matchs_tmp[minW][1][-1])) + \
							(1 << (error_block_tmp[minW] + 1))
						Wold_tmp[minW] = Wold[-j]
					else:
						if(matchs_tmp[minW][0][-1] != matchs_tmp[minW][1][-1]):
							error_block_tmp[minW] += 1
						if(minW < tstr_len - j - 1):
							matchs_tmp[minW][0].append(template_str[minW+1:-j])
							matchs_tmp[minW][1].append('')
							error_block_tmp[minW] += 1
							Wnew_tmp[minW] = Wnew[minW] + (1 << (tstr_len - j - minW - 1)) + \
								(1 << error_block_tmp[minW])
							Wold_tmp[minW] = Wnew_tmp[minW]
						else:
							Wnew_tmp[minW] = Wnew[minW]
							Wold_tmp[minW] = Wnew_tmp[minW]
						matchs_tmp[minW][0].append(template_str[-j])
						matchs_tmp[minW][1].append(match_str[i])
						if(template_str[-j] != match_str[i]):
							Wnew_tmp[minW] += 2 + (1 << (error_block_tmp[minW] + 1))

				best = np.argmin(Wnew_tmp)
				Wnew[-j] = Wnew_tmp[best]
				Wold[-j] = Wold_tmp[best]
				matchs[-j] = copy.deepcopy(matchs_tmp[best])
			#print(matchs)
		for i in range(tstr_len-1):
			matchs[i][0].append(template_str[i+1:])
			matchs[i][1].append('')
			Wnew[i] += (1 << (len(matchs[i][0][-1]) >> 1)) + \
				(1 << (error_block[i] + 1))
		#print(matchs)
		minW = np.argmin(Wnew)
		return [Wnew[minW], matchs[minW]]
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
				lResult=Extract.Extract(lSpace)
				if len(lResult[0][0])>0 and len(lResult[0][1])>0:
					return lResult

			return WORD_NOT_FOUND
		pass
		#return [information,extra]

	def get_sound(self, word):
		'''获取发音\n
		output：\n
			Sound
		'''
		if word in self.__word_dict.keys():
			return self.__word_dict[word][0][1]
		else:
			return WORD_NOT_FOUND
		pass
		#return PathOfSound

	def get_mean(self, word):
		'''获取释义\n
		output：\n
			meaning
		'''
		if word in self.__word_dict.keys():
			return self.__word_dict[word][0][0]
		else:
			return WORD_NOT_FOUND
		pass

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

		with open(os.path.join(rootpath,'Original.txt'),"w",encoding='utf-8') as fSave:
			fSave.write(str(result))

		Extract.ExtractToDir(result,rootpath)

WORD_NOT_FOUND = -1
WORD_DICT_LOAD_SUCCEED = 1
GET_WORDLIST_SUCCEED = 1

if __name__ == "__main__":
	WORD_DICT = WordDict()
	root0 = 'HappyWordTutorial\WordDict\dict'
	root = 'WordDict\dict'
	load_err = WORD_DICT.load(root0)
	if load_err != WORD_DICT_LOAD_SUCCEED:
		print(load_err)
		exit(0)
	[W, match] = WORD_DICT.matcher0('process', 'pass')
	print(W)
	print(match)
	[likelihood, wordlist] = WORD_DICT.match_word('process')
	top5index = np.argsort(likelihood)[:5]
	top5word = [wordlist[i] for i in top5index]
	print(likelihood[top5index])
	print(top5word)
	pass

