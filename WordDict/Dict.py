class Dict:
	def __init__(self):
		'''
		WordDict: dict
			key:英文单词
			value: [information, extra]
				information: [释义,发音]
				extra:{'例句'：[[例句1,例句1释义,例句1发音], ...],
						'形似词': ,
						...}
		'''
		WordDict = {}

		pass

	def Open(self,DictPath):
		'''打开词库文件，录入WordDict中'''
		pass

	def ListOfWord(self):
		'''获取整个词库所有的单词'''
		pass
		#return [word1,word2,...]

	def Navigate(self):
		'''遍历词库
		output：
			yield (word,information,extra)
		
		'''
		pass
		#yield (word,information,extra)

	def MatchWord(self,word,matcher,parameter):
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

	def GetInfo(self,word):
		'''获取单词的信息
		input：
			word：单词
		output：
			list[information,extra]
		'''
		pass
		#return [information,extra]

	def GetSound(self, word):
		'''获取发音文件路径
		output：
			PathOfSound
		'''
		pass
		#return PathOfSound

	def update(self):
		'''更新词库
		'''
		pass