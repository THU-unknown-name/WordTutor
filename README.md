# WordTutor

Project for Software Engineering, THU 2019 Fall 

## 运行

运行方式：在控制终端中运行以下命令

~~~python
python mymain.py
~~~

## 系统要求

Widows操作系统，python编译环境，有PyQt5包以及有Windows自带的语音识别功能，即需要能够

~~~python
import PyQt5
import win32com.client
~~~

## 程序功能

* 查词
  * 可对输入单词进行查找释义和例句
  * 不联网的情况下会自动匹配本地数据库中最佳单词
  * 有单词发音
  * 能够将单词加入背诵计划
* 背单词
  * 按照计划从生词本中按照一定规则随机选取一定数目的单词进行背诵
  * 点击单词或者例句可以进行发音
* 计划管理
  * 可以修改背诵计划
  * 能够查看已背单词的掌握情况
* 游戏测评
  * 目前只有一种游戏
  * 会根据生词本生成需要测评的单词
  * 将测评结果记录并作为下次测评的依据
* 详细请查看各个模块的README

