#!/usr/bin/env python3

with open("save.txt","r") as fFile:
	data=fFile.read()
	lList=eval(data)

for iLoop1 in range(len(lList)):
	with open("dict/%s"%(lList[iLoop1][0]),"w") as fFile:
		fFile.write(str([[lList[iLoop1][2].strip(),lList[iLoop1][1].strip()],[lList[iLoop1][3].strip()]]))

