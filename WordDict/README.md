# 词库
## 基本功能接口介绍
数据：

+ __word_dict: dict private，词库数据

  + key: 英文单词

  + value: list[information, extra]

    + information(基本信息): list[释义，发音]

    + extra(扩展信息): dict{'例句'：[[例句1,例句1释义,例句1发音], ...],

      ​									'形似词': (暂无),

      ​									...}

+ __rootpath: str private，词库根目录

+ word_list: list，单词目录

函数：
+ load(self, rootpath):打开词库文件，录入WordDict中

  + input:

    + rootpath:词库根目录

  + output:

    + if succeed: return WORD_DICT_LOAD_SUCCEED
    + else: return error_massage

  + example:

    ~~~python
    WORD_DICT = Word_Dict()
    load_err = WORD_DICT.load('WordDict\dict')
    if load_err != WORD_DICT_LOAD_SUCCEED:
        print(load_err)
        exit(0)
    ~~~

    

+ get_wordlist(self):获取整个词库所有的单词(由load()函数调用)

  + output:

    + if succeed: return GET_WORDLIST_SUCCEED
    + else: return error_message

  + example:

    ~~~python
    WORD_DICT = Word_Dict()
    get_wordlist_err = WORD_DICT.get_wordlist()
    if get_wordlist_err != GET_WORDLIST_SUCCEED:
        print(get_wordlist_err)
    ~~~

    

+ navigate(self):遍历词库

  + output:

    + yield (word,[information,extra])

  + example:

    ~~~python
    WORD_DICT = Word_Dict()
    load_err = WORD_DICT.load('WordDict\dict')
    if load_err != WORD_DICT_LOAD_SUCCEED:
        print(load_err)
        exit(0)
    for word, info in WORD_DICT.navigate():
        print(word) #打印单词
        print(info[0][0]) #打印释义
        print(info[1]['hennkou']) #打印例句
        print(info[1]['reiku']) #打印变形
    ~~~
  ~~~
    
    
  ~~~

+ match_word(self,word):匹配单词

  + input:

    + word: 需要匹配的单词

  + output:

    + list[likelihood, wordlist]:
      + likelihood:与wordlist中的单词的匹配度，值越小匹配度越高
      + wordlist:单词列表，word与wordlist中的单词分别进行匹配

  + example:

    ~~~python
    WORD_DICT = Word_Dict()
    load_err = WORD_DICT.load('WordDict\dict')
    if load_err != WORD_DICT_LOAD_SUCCEED:
        print(load_err)
        exit(0)
    [likelihood, wordlist] = WORD_DICT.match_word('afternoon')
    top5index = np.argsort(likelihood)[:5]
    top5word = [wordlist[i] for i in top5index]
    print(top5word)
    ############################################################
    #打印结果(还需要改进)
    ['afternoon', 'attention', 'autumn', 'action', 'another']
    ~~~

+ matcher(self, template_str, match_str):采用DTW算法进行字符串匹配

  + input:

    + template_str:模板字符串
    + match_str:需要匹配的字符串

  + output:

    + list[score, match]:
      + score:匹配度，值越小匹配度越高，最小为0
      + match:匹配情况

  + example:

    ~~~python
    WORD_DICT = Word_Dict()
    load_err = WORD_DICT.load('WordDict\dict')
    if load_err != WORD_DICT_LOAD_SUCCEED:
        print(load_err)
        exit(0)
    [W, match] = WORD_DICT.matcher('afternoon', 'apterno')
    print(W)
    print(match)
    ~~~
    
    
  
+ get_info(self,word):获取单词的信息

  + input:

    + word: 单词

  + output: 

    + if succeed: return list[information,extra]:

      + information(基本信息): list[释义，发音]

      + extra(扩展信息): dict{'例句'：[[例句1,例句1释义,例句1发音], ...],

        ​									'形似词': (暂无),

        ​									...}

    + else: return WORD_NOT_FOUND

  + example:

    ~~~python 
    WORD_DICT = Word_Dict()
    load_err = WORD_DICT.load('WordDict\dict')
    if load_err != WORD_DICT_LOAD_SUCCEED:
        print(load_err)
        exit(0)
    info = WORD_DICT.get_info('afternoon')
    if info != WORD_NOT_FOUND:   
    	print(info[0][0]) #打印释义
    	print(info[1]['hennkou']) #打印例句
    else:
        pass
    ~~~

    

+ get_sound(self, word):获取发音

+ get_mean(self, word):获取释义

+ update(wordlist,rootpath):更新词库
	+ input:

		wordlist list[str...]: list words to grep information
		rootpath str: path to store result data

	+ example:

		import WordDict
		WordDict.WordDict.update("wordlist.txt","dict")

## 词库爬取方式
Run Grep.py to grep information of words stored in utf-8.txt and store the result into save.txt
The current format used to store in save.txt is a list printed as string.
+ The first dimension of the list defines diffrent records for words
+ The second dimension of the lis defines the different aspects of information for the word.
	+ 0 -> Word: The word
	+ 1 -> Pronounciation: The pronounciation of the word
	+ 2 -> Explanation: Chinese meaning
	+ 3 -> Change: Type changing
	+ 4 -> Example: Example sentenses
Usage:
+ Run Grep.py.
	+ Input -2 to grep Inforamtion of words stored in utf-8.txt or upgrade the current List.
		+ Failure may occur during this procedure, just input and run again to fill in the missing entries.
	+ Input -1 to save the current greped information(word list included).
	+ Input a non-negative number to see the details of a specific entry(in the order of storage in List).
		+ Attention, if the ubound exceed the count of entries, the program would crash.
	+ Input a negative number less than -2 to exit.

Run Extract.py to Extract the save.txt to dict dir, which writes the details of each word into separate file and writes a total list into WordList.txt

Run Process.sh to convert utf-8.txt to wordlist.txt for a raw word list
Then Run Process.py to Grep the word information and store them into Directory dict
Or for a manual version, Run Grep.py and use relevant inputs to get save.txt relevant to wordlist.txt. Then Run Extract.py to extract save.txt into dict directory for the main program to use.

Grep.py:
+ Info: Default classes to collect information

+ Get(sWord,lInfo): Grep information of word
	+ input:

		+ sWord str:Word to grep info
		+ lInfo list[str classes...]:list of strings which describes the classes of tags to grep specific parts of information

	+ output:

		+ list[str data...]:contexts greped from iciba with respect to lInfo

	+ example:

		import Grep
		word="cluster"
		lSpace=Grep.Get(word,Grep.Info)
		print(lSpace)

Extract.py:
+ Extract(lList): Extract the raw information greped by Get into Info format used by WordDict
	+ input:

		+ lList list: Original Information greped by Get

	+ output:

		+ list: format used by WordDict(returned by get_info)

	+ example:

		import Grep
		import Extract
		word="cluster"
		lSpace=Grep.Get(word,Grep.Info)
		lSpace=Extract.Extract(lSpace)
		print(lSpace)

+ ExtractToDir(lList,rootpath): Extract the raw information and write to rootpath
	+ input:

		+ lList list: Original Information
		+ rootpath str: root path to store extracted information

	+ example:

		import Extract
		with open("save.txt","r") as fFile:
			data=fFile.read()
			lList=eval(data)
		ExtractToDir(lList,"dict")

