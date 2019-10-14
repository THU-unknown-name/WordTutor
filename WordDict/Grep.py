#!/usr/bin/env python3
import socket
import urllib.request
import lxml.html
import os
import re

#Upgrade the dictionary
def Update(result):
	newline=re.compile("[ \r\n]*[\r\n][ \r\n]*")
	space=re.compile(" +")
	#Navigate throuhout the dictinary
	for iLoop1 in range(len(result)):
		#Fillin Entries not complete
		if result[iLoop1][1] is None or result[iLoop1][2] is None or result[iLoop1][3] is None:
			#Printout progress
			print("%d/%d"%(iLoop1,len(result)))
			data=None
			try:
				#Grep Html
				request=urllib.request.urlopen("http://www.iciba.com/%s"%(result[iLoop1][0]),timeout=2)
				data=request.read().decode()
			except urllib.request.URLError:
				#What error?
				data=None
				print("Failed to request")
			except socket.timeout:
				#Time out(2s)
				data=None
				print("Timeout")

			if data is not None:
				document=lxml.html.document_fromstring(data)
				#Find tag with specific class(baic info)
				infos=document.find_class("in-base-top")
				if len(infos)==1:
					result[iLoop1][1]=infos[0].text_content()
					result[iLoop1][1]=space.sub(" ",newline.sub("\n",result[iLoop1][1]))
				else:
					print("%s Error1!!\n"%(result[iLoop1][0]));

				#Find tag with specific class(chinese explainiation)
				infos=document.find_class("base-list")
				if len(infos)>0:
					#Link the content
					result[iLoop1][2]=""
					for info in infos:
						result[iLoop1][2]=result[iLoop1][2]+info.text_content()
					result[iLoop1][2]=space.sub(" ",newline.sub("\n",result[iLoop1][2]))
				else:
					print("%s Error2!!\n"%(result[iLoop1][0]));

				#Find tag with specific class(extra)
				infos=document.find_class("article")
				if len(infos)>0:
					#Link the content
					result[iLoop1][3]=""
					for info in infos:
						result[iLoop1][3]=result[iLoop1][3]+info.text_content()
					result[iLoop1][3]=space.sub(" ",newline.sub("\n",result[iLoop1][3]))
				else:
					print("%s Error3!!\n"%(result[iLoop1][0]));

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
					result.append([space[1],None,None,None])
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
			print(result[serial][0])
			print("************************************")
			print(result[serial][1])
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
			print(result[serial][2])
			print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
			print(result[serial][3])
			print("------------------------------------")

if __name__=="__main__":
	main()

