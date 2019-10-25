#!/usr/bin/env python3

from WordDict import WORD_DICT as wdDict


wdDict.load("dict")


'''
for a,b in wdDict.navigate():
	print(a,b)
	input()
'''


#print(wdDict.get_wordlist())

print(wdDict.get_sound("any"))
print(wdDict.get_info("any"))

