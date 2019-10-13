#!/usr/bin/env python3
import socket
import urllib.request
import lxml.html
import os

#Upgrade the dictionary
def Update():
	global result
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
				else:
					print("%s Error1!!\n"%(result[iLoop1][0]));

				#Find tag with specific class(chinese explainiation)
				infos=document.find_class("base-list")
				if len(infos)>0:
					#Link the content
					result[iLoop1][2]=""
					for info in infos:
						result[iLoop1][2]=result[iLoop1][2]+info.text_content()
				else:
					print("%s Error2!!\n"%(result[iLoop1][0]));

				#Find tag with specific class(extra)
				infos=document.find_class("article")
				if len(infos)>0:
					#Link the content
					result[iLoop1][3]=""
					for info in infos:
						result[iLoop1][3]=result[iLoop1][3]+info.text_content()
				else:
					print("%s Error3!!\n"%(result[iLoop1][0]));

if os.path.isfile("save.txt"):
	#Restore from local file
	with open("save.txt","r") as fSaved:
		data=fSaved.read()
		result=eval(data)
	print("Restored")
elif os.path.isfile("utf-8.txt"):
	#Initialize with only word
	with open("utf-8.txt","r") as fSource:
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
			with open("save.txt","w") as save:
				save.write(str(result))
		elif serial==-2:
			#-2 for upgrade
			Update()
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

