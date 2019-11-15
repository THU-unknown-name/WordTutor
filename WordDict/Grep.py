#!/usr/bin/env python3
import socket
import urllib.request
import lxml.html
import os
import re
import urllib.parse

#Info=[["base-speak",None],["base-list",None],["change",None],["article",{"product","hotwords"}]]
Info=[["base-speak",None,None,None],["base-list",None,None,None],["change",None,None,None],["collins-section",None,{"ms-if"},{"suggest"}]]

def Get(sWord,lInfo):
	newline=re.compile("[ \r\n]*[\r\n][ \r\n]*")
	space=re.compile(" +")
	result=[None]*len(Info)

	data=None

	try:
		#Grep Html
		request=urllib.request.urlopen("http://www.iciba.com/%s"%(urllib.parse.quote(sWord)),timeout=2)
		data=request.read().decode()
	except urllib.request.URLError:
		#What error?
		print("Failed to request")
		return None
	except socket.timeout:
		#Time out(2s)
		print("Timeout")
		return None

	document=lxml.html.document_fromstring(data)
	document=document.find_class("container")
	if len(document)!=1:
		print("Error")
		return
	document=document[0]
	for iLoop1 in range(len(lInfo)):
		infos=document.find_class(lInfo[iLoop1][0])

		result[iLoop1]=""
		for info in infos:
			bSkip=False

			if lInfo[iLoop1][1] is not None:
				for cSkip in lInfo[iLoop1][1]:
					if cSkip in info.classes:
						bSkip=True
						break

			if not bSkip and lInfo[iLoop1][2] is not None:
				for iKey,_ in info.items():
					if iKey in lInfo[iLoop1][2]:
						bSkip=True
						break

			if not bSkip and lInfo[iLoop1][3] is not None:
				for eData in info.iter():
					for cSkip in lInfo[iLoop1][3]:
						if cSkip in eData.classes:
							bSkip=True
							break
					if bSkip:
						break


			if not bSkip:
				result[iLoop1]=result[iLoop1]+info.text_content()

		result[iLoop1]=space.sub(" ",newline.sub("\n",result[iLoop1])).strip()

	return result


#Upgrade the dictionary
def Update(result,CallBack=None):
	global Info
	#Navigate throuhout the dictinary
	for iLoop1 in range(len(result)):
		#Fillin Entries not complete
		if len(result[iLoop1])<=1:
			data=Get(result[iLoop1][0],Info)
			if data is not None:
				result[iLoop1]=result[iLoop1][0:1]+data
			if CallBack is not None:
				CallBack(iLoop1)


def main():
	inputfile="utf-8.txt"
	savefile="save.txt"
	if os.path.isfile(savefile):
		#Restore from local file
		with open(savefile,"r") as fSaved:
			data=fSaved.read()
			result=eval(data)
		print("Restored")
	elif os.path.isfile(inputfile):
		#Initialize with only word
		with open(inputfile,"r") as fSource:
			result=[]
			for sLine in fSource:
				space=sLine.split()
				if len(space)>2:
					result.append([space[1]])
		print("Initialized")

	while True:
		#Enter a integer
		serial=int(input())
		if serial<0:
			if serial==-1:
				#-1 for save
				with open(savefile,"w") as save:
					save.write(str(result))
			elif serial==-2:
				#-2 for upgrade
				Update(result)
			else:
				#others for quit
				break
		else:
			#Print out the entry if num is nonnegative
			for iLoop1 in range(len(result[serial])):
				print(result[serial][iLoop1])
				print("************************************")

if __name__=="__main__":
	main()

