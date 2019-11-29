#!/usr/bin/env python
import unittest
import random
import os
import shutil
import numpy as np

from . import WordDict

class Test_WordDict(unittest.TestCase):

	def setUp(self):
		if os.path.exists("./unit_test"):
			shutil.rmtree("./unit_test")

		os.mkdir("./unit_test")

	def tearDown(self):
		if os.path.exists("./unit_test"):
			shutil.rmtree("./unit_test")

	def test_load_success(self):
		WORD_DICT=WordDict.WordDict()
		self.assertEqual(WORD_DICT.load("WordDict/dict"),WordDict.WORD_DICT_LOAD_SUCCEED)

	def test_load_failed(self):
		WORD_DICT=WordDict.WordDict()
		self.assertIs(type(WORD_DICT.load("./unit_test")),str)
		self.assertIs(type(WORD_DICT.load("./unit_test/dict")),str)

	def test_get_wordlist(self):
		WORD_DICT=WordDict.WordDict()
		self.assertEqual(WORD_DICT.load("WordDict/dict"),WordDict.WORD_DICT_LOAD_SUCCEED)
		self.assertEqual(WORD_DICT.get_wordlist(),WordDict.GET_WORDLIST_SUCCEED)
		WORD_DICT.word_list

		self.assertIs(type(WORD_DICT.word_list),list)

		self.assertTrue(all([type(x) is str for x in WORD_DICT.word_list]))

	def test_navigate(self):
		dKeyWords={"hennkou","reiku"}
		WORD_DICT=WordDict.WordDict()
		self.assertEqual(WORD_DICT.load("WordDict/dict"),WordDict.WORD_DICT_LOAD_SUCCEED)
		for (word,info) in WORD_DICT.navigate():
			self.assertIs(type(word),str)

			self.assertIs(type(info),list)
			self.assertEqual(len(info),2)

			self.assertIs(type(info[0]),list)
			self.assertEqual(len(info[0]),2)
			self.assertIs(type(info[0][0]),str)
			self.assertIs(type(info[0][1]),str)

			self.assertIs(type(info[1]),dict)

			for x in info[1].keys():
				self.assertIn(x,dKeyWords)

			if "hennkou" in info[1].keys():
				self.assertIs(type(info[1]["hennkou"]),str)

			if "reiku" in info[1].keys():
				reiku=info[1]["reiku"]
				self.assertIs(type(reiku),list)
				self.assertTrue(all([len(x)==2 for x in reiku]))
				self.assertTrue(all([type(x[0]) is str and type(x[1]) is str for x in reiku]))

	def test_get_info_InDict(self):
		WORD_DICT=WordDict.WordDict()
		self.assertEqual(WORD_DICT.load("WordDict/dict"),WordDict.WORD_DICT_LOAD_SUCCEED)

		#InDict
		for (word,info) in WORD_DICT.navigate():
			self.assertEqual(WORD_DICT.get_info(word),info)

	def test_get_info_OutDict_Word(self):
		WORD_DICT=WordDict.WordDict()
		self.assertEqual(WORD_DICT.load("WordDict/dict"),WordDict.WORD_DICT_LOAD_SUCCEED)

		self.assertEqual(WORD_DICT.get_wordlist(),WordDict.GET_WORDLIST_SUCCEED)

		#OutDict
		iFound=0
		iTime=0
		iLen=[5,20]
		lFound=[]
		lNotFound=[]

		lWord=["hiking","playing","swam"]

		for sWord in lWord:
			if sWord not in WORD_DICT.word_list:
				lResult=WORD_DICT.get_info(sWord)

				if lResult==WordDict.WORD_NOT_FOUND:
					lNotFound.append(sWord)
				else:
					lFound.append(sWord)
					self.assertIs(type(lResult),list)
					self.assertEqual(len(lResult),2)

					self.assertIs(type(lResult[0]),list)
					self.assertEqual(len(lResult[0]),2)
					self.assertIs(type(lResult[0][0]),str)
					self.assertIs(type(lResult[0][1]),str)

					self.assertIs(type(lResult[1]),dict)

					self.assertGreater(len(lResult[0][0]),0)
					self.assertGreater(len(lResult[0][1]),0)
				iTime+=1

		print("Found rate %f%%\n\tFound %s\nNotFound %s"%(len(lFound)/iTime*100,lFound,lNotFound))


	def test_get_info_OutDict_Rand(self):
		WORD_DICT=WordDict.WordDict()
		self.assertEqual(WORD_DICT.load("WordDict/dict"),WordDict.WORD_DICT_LOAD_SUCCEED)

		self.assertEqual(WORD_DICT.get_wordlist(),WordDict.GET_WORDLIST_SUCCEED)

		#OutDict
		iFound=0
		iTime=5
		iLen=[5,20]
		lFound=[]
		lNotFound=[]

		src="abcdefghijilmnopqrstuvwxyzABCDEFGHIJILMNOPQRSTUVWXYZ."

		for iLoop1 in range(iTime):
			lLength=random.randint(*iLen)
			while True:
				sWord=""
				for iLoop2 in range(lLength):
					sWord=sWord+src[random.randint(0,len(src)-1)]
				if sWord not in WORD_DICT.word_list:
					lResult=WORD_DICT.get_info(sWord)

					if lResult==WordDict.WORD_NOT_FOUND:
						lNotFound.append(sWord)
					else:
						lFound.append(sWord)
						self.assertIs(type(lResult),list)
						self.assertEqual(len(lResult),2)

						self.assertIs(type(lResult[0]),list)
						self.assertEqual(len(lResult[0]),2)
						self.assertIs(type(lResult[0][0]),str)
						self.assertIs(type(lResult[0][1]),str)

						self.assertIs(type(lResult[1]),dict)

						self.assertGreater(len(lResult[0][0]),0)
						self.assertGreater(len(lResult[0][1]),0)

					break

		print("Found rate %f%%\n\tFound %s\nNotFound %s"%(len(lFound)/iTime*100,lFound,lNotFound))

	def test_get_sound(self):
		src="abcdefghijilmnopqrstuvwxyzABCDEFGHIJILMNOPQRSTUVWXYZ."

		WORD_DICT=WordDict.WordDict()
		self.assertEqual(WORD_DICT.load("WordDict/dict"),WordDict.WORD_DICT_LOAD_SUCCEED)

		#InDict
		for (word,info) in WORD_DICT.navigate():
			self.assertEqual(WORD_DICT.get_sound(word),info[0][1])

	def test_update(self):
		lWord=["shadow","escalator","swim"]
		with open("./unit_test/test.txt","w") as fFile:
			fFile.write("\n".join(lWord))

		os.mkdir("./unit_test/dict")

		WORD_DICT=WordDict.WordDict()
		WORD_DICT.update("./unit_test/test.txt","./unit_test/dict")

		self.assertTrue(os.path.isfile("./unit_test/dict/Original.txt"))
		self.assertTrue(os.path.isfile("./unit_test/dict/WordList.txt"))

		WORD_DICT=WordDict.WordDict()
		self.assertEqual(WORD_DICT.load("./unit_test/dict"),WordDict.WORD_DICT_LOAD_SUCCEED)

		for (word,info) in WORD_DICT.navigate():
			self.assertIn(word,lWord)
			self.assertGreater(len(info[0][0]),1)
			self.assertGreater(len(info[0][1]),1)

			if "hennkou" in info[1].keys():
				self.assertIs(type(info[1]["hennkou"]),str)

			if "reiku" in info[1].keys():
				reiku=info[1]["reiku"]
				self.assertIs(type(reiku),list)
				self.assertTrue(all([len(x)==2 for x in reiku]))
				self.assertTrue(all([type(x[0]) is str and type(x[1]) is str for x in reiku]))

	def test_reiku(self):
		regexp="^[-_+=~`!@#$%^&*()\\[\\]\\{\\}|\;:'\",./<>?\r\n\t A-Za-z]+$"
		WORD_DICT=WordDict.WordDict()
		self.assertEqual(WORD_DICT.load("WordDict/dict"),WordDict.WORD_DICT_LOAD_SUCCEED)

		for (word,info) in WORD_DICT.navigate():
			if "reiku" in info[1].keys():
				reiku=info[1]["reiku"]
				for sEng,sChi in reiku:
					self.assertRegex(sEng,regexp)
					self.assertNotRegex(sChi,regexp)
					self.assertGreater(ord(max(sChi)),255)

	def test_matcher(self):
		WORD_DICT=WordDict.WordDict()
		self.assertEqual(WORD_DICT.load("WordDict/dict"),WordDict.WORD_DICT_LOAD_SUCCEED)

		test = ["afternoon", "apterno", "aternoon"]
		result = [['a','f','t','e','r','n','o','on'],['a','p','t','e','r','n','o','']]
		[W, match] = WORD_DICT.matcher(test[0], test[1])
		self.assertListEqual(match, result)
		self.assertEqual(W, 10)

		result = [['a','f','t','e','r','n','o','o','n'],['a','','t','e','r','n','o','o','n']]
		[W, match] = WORD_DICT.matcher(test[0], test[2])
		self.assertListEqual(match, result)
		self.assertEqual(W, 4)

	def test_match_word(self):
		WORD_DICT=WordDict.WordDict()
		self.assertEqual(WORD_DICT.load("WordDict/dict"),WordDict.WORD_DICT_LOAD_SUCCEED)
		
		test = ['process', 'after', 'aternoon']
		result = ['progress', 'afternoon']
		[likelihood, wordlist] = WORD_DICT.match_word(test[0])
		mostlike = np.argsort(likelihood)[0]
		self.assertEqual(result[0], wordlist[mostlike])

		[likelihood, wordlist] = WORD_DICT.match_word(test[1])
		mostlike = np.argsort(likelihood)[1]
		self.assertEqual(result[1], wordlist[mostlike])

		[likelihood, wordlist] = WORD_DICT.match_word(test[2])
		mostlike = np.argsort(likelihood)[0]
		self.assertEqual(result[1], wordlist[mostlike])


		
if __name__=="__main__":
	unittest.main()

