#!/usr/bin/env python3
import socket
import urllib.request
import lxml.html
import os
import re

Info=["base-speak","base-list","change","article"]
#Info=["base-list","article"]


def Get(sWord,lInfo):
	newline=re.compile("[ \r\n]*[\r\n][ \r\n]*")
	space=re.compile(" +")
	result=[None]*len(Info)

	data=None

	try:
		#Grep Html
		request=urllib.request.urlopen("http://www.iciba.com/%s"%(sWord),timeout=2)
		data=request.read().decode()
		#print(data)
	except urllib.request.URLError:
		#What error?
		print("Failed to request")
		return None
	except socket.timeout:
		#Time out(2s)
		print("Timeout")
		return None

	document=lxml.html.document_fromstring(data)
	for iLoop1 in range(len(lInfo)):
		infos=document.find_class(lInfo[iLoop1])

		result[iLoop1]=""
		for info in infos:
			result[iLoop1]=result[iLoop1]+info.text_content()
		result[iLoop1]=space.sub(" ",newline.sub("\n",result[iLoop1]))

	return result


#Upgrade the dictionary
def Update(result):
	global Info
	#Navigate throuhout the dictinary
	for iLoop1 in range(len(result)):
		#Fillin Entries not complete
		if len(result[iLoop1])<=1:
			#Printout progress
			print("%d/%d"%(iLoop1,len(result)))
			data=Get(result[iLoop1][0],Info)
			if data is not None:
				result[iLoop1]=result[iLoop1][0:1]+data
			else:
				print("Failed to request")


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

