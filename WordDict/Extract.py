#!/usr/bin/env python3

def Extract(lList):
	return [[lList[1].strip(),lList[0].strip()],[lList[2].strip()]]

def main():
	with open("save.txt","r") as fFile:
		data=fFile.read()
		lList=eval(data)

	with open("dict/WordList.txt","w") as fList:
		for iLoop1 in range(len(lList)):
			fList.write("%s\n"%(lList[iLoop1][0]))
			with open("dict/%s"%(lList[iLoop1][0]),"w") as fFile:
				fFile.write(str(Extract(lList[iLoop1][1:])))

if __name__=="__main__":
	main()

