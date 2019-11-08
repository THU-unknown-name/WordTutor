#!/usr/bin/env python3
import os

def Extract(lList):
	return [[lList[1],lList[0]],[lList[2]]]

def ExtractToDir(lList,rootpath):
	with open(os.path.join(rootpath,"WordList.txt"),"w") as fList:
		for iLoop1 in range(len(lList)):
			fList.write("%s\n"%(lList[iLoop1][0]))
			with open(os.path.join(rootpath,lList[iLoop1][0]),"w") as fFile:
				fFile.write(str(Extract(lList[iLoop1][1:])))

def main():
	with open("save.txt","r") as fFile:
		data=fFile.read()
		lList=eval(data)

	ExtractToDir(lList,"dict")

if __name__=="__main__":
	main()

