#!/usr/bin/env python3
import os
import re

def Extract(lList):
	lSentences=[]
	lSplit=re.split("[\r\n]+",lList[3])

	pSplit=re.compile("^[\\d\\.]+$")
	pEng=re.compile("^[-_+=~`!@#$%^&*()\\[\\]\\{\\}|\;:'\",./<>? A-Za-z]+$")

	sSpace=""
	lData=[None,None]
	for lLine in lSplit:
		if pSplit.fullmatch(lLine) is not None:
			if lData[0] is not None and lData[1] is not None:
				lSentences.append(lData)
			lData=[None,None]
		elif pEng.fullmatch(lLine) is not None:
			if lData[0] is None:
				lData[0]=lLine
			else:
				lData[0]+="\n"+lLine
		elif len(lLine)>0:
			if lData[1] is None:
				lData[1]=lLine
			else:
				lData[1]+="\n"+lLine

	if lData[0] is not None and lData[1] is not None:
		lSentences.append(lData)
	lData=[None,None]

	return [[lList[1],lList[0]],{"hennkou":lList[2],"reiku":lSentences}]

def ExtractToDir(lList,rootpath):
	with open(os.path.join(rootpath,"WordList.txt"),"w") as fList:
		for iLoop1 in range(len(lList)):
			fList.write("%s\n"%(lList[iLoop1][0]))
			with open(os.path.join(rootpath,lList[iLoop1][0]),"w",encoding='utf-8') as fFile:
				fFile.write(str(Extract(lList[iLoop1][1:])))

def main():
	with open("save.txt","r") as fFile:
		data=fFile.read()
		lList=eval(data)

	ExtractToDir(lList,"dict")

if __name__=="__main__":
	main()

