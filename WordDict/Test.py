#!/usr/bin/env python3
from . import WordDict

def main():
	wdDict=WordDict.WordDict()


	wdDict.load("dict")

	#print(wdDict.get_wordlist())

	print(wdDict.get_info("any"))
	print(wdDict.get_info("ancestor"))

	'''
	for a,b in wdDict.navigate():
		print(a,b)
		input()
	'''


if __name__=="__main__":
	main()

