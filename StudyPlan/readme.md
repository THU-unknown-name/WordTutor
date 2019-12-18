# 生词本及学习计划

## 生成每日背单词计划表

### 文件说明

#### Vocab.py

包括Vocab类，将WordDict转变为词汇表
Vocab为一dict，其中key为单词，value为该单词的熟悉度

添加了一些接口：

* `add_word_to_vocab(word)`:向词库表中添加一个单词

* `remove_word_from_vocab(word)`：从词库表中移除一个单词

* `get_n_word_from_familiarVocab(n)`：从熟悉的单词中选取n个单词（用于游戏）


#### Vocab.pkl

存储Vocab的pickle文件
由于每次背完单词后需要更新单词的熟悉度，因此需用pickle文件保存下来，下次运行时读取

#### TodayList.py

包括TodayList类，从Vocab中选取一定的数量的词汇构成每日的计划列表
todayList为一个list，为每日计划表，如：['a', 'baby', 'cat', ...]

添加了一些接口：

* `set_stated_todaylist_length(length)`：设置每日计划表的长度（此设定从第二天开始实行，不改变当天单词列表中的单词数目）

* `get_stated_todaylist_length()`：返回每日计划表的设定值

* `update_current_word(index)`：更新当前背到了哪个单词。每背完一个单词对其进行更新

* `get_current_word()`：返回当前背到了哪个单词。每次打开软件时从今日计划表中该位置开始继续往下背

* `add_word_to_todaylist(word, vocab)`：添加单词到每日计划中 **此时默认添加到了词库中**

* `get_n_word_from_todaylist(n)`：从TodayList中返回n个单词用于游戏

* `record_finished(self, num, today_list_dict)`：把今日已经背的单词数、背诵单词情况记录下来，以便之后存进pkl

* `save_todaylist()`：将`__today_list`, `__vocab_num`, `__stated_vocab_num`, `__date`， `__current_word_index`等变量存到pickle文件中，运行时读取 # 注意：一定要在结束背单词的动作后执行该函数，保存数据！

#### TodayList.pkl
存储Todaylist的pickle文件

一定要在退出背单词时完成保存，否则今日计划表的数据会丢失！

#### test_studyPlan.py

测试用文件,里面针对Vocab.py和TodayList.py的各个接口和功能进行了测试。通过调用WordTutor中的StudyPlanTest.py运行

运行方式：在WordTutor目录下 运行 python StudyPlanTest.py


## 背单词

### 文件说明

#### recite_action.py

* 完善由`pyuic`翻译出的recite_gui.py，定义slot和signal。
* 完成背单词操作
* 第一次进入时会有弹出框，询问需要每天背多少个单词
* 每次退出时会记录下当前所背的词的数量，保存vocab.pkl, todaylist.pkl（保存之前要先把今日已经背过几个词、今日背词状态先更新到TodayList对象中）
* 当某天已经完成了背诵，再次点击背单词会弹出提示"今日已背完"，不再背诵，这边建议亲移步游戏区呢。

#### GUI/

* **recite_gui.\***：recite_gui.ui由Qt Designer设计，运行`pyuic5 -o recite_gui.py recite_gui.ui`后生成recite_gui.py
* **congrats.\***：congrats.qrc为资源文件，congrats.py定义了资源模块，用于描述图片congrats.jpg，显示于背完所有今日词汇后的祝贺界面

## 生词本管理

由GUI/setting_gui.py及setting_action.py实现。

### 学习计划设置

* 显示当前计划：x个每天
* 修改当前计划：点击"修改"按钮即可修改，弹出对话框，调用`Todaylist.set_stated_todaylist_length`会同步存入pkl中，第二日生效。输入数据不合法时会有警告。

### 生词展示

* 生词依次被展示在QListWidget中，包括已掌握（熟悉度=2）和未掌握（熟悉度=1）的。已掌握的词背景为深绿色，未掌握为浅绿色。

## Chang Log

* 2019.12.6 增加了“今天”的概念，同一天的计划表不发生变化，不同天的计划表不同。因此还需要一个TodayList.pickle文件来存储相关信息
* 2019.12.14 由于用户很可能不连续地记不住单词，`update_current_word(index)`, `get_current_word()`很可能是没有意义的，这里我直接跳过了熟悉度最高的词作为暂时的处理方式，认为它们已经背完，为了保持一致，对TodayList.py里面生成计划的方式进行了修改(去掉了将最熟悉的词列入计划部分，这里可能需要进一步测试)。把词表生成方式改为40%新词+60%不熟悉词。
* 2019.12.17 将today_list改为dict，value为word，key为今日背诵情况（0为没背过，1为背过没记住还需要复习，2为记住了不再出现）。

## Task List

- [x] 计划生成：从指定WordDict中随机选取新词，从Vocab中根据熟悉度生成复习词汇，组成今日计划TodayList (zr)
- [x] 背单词：GUI+更改Vocab中熟悉度 (lqa)
- [x] 存档：Vocab要存入文件，下次运行时读取 (zr)
- [x] "今天"继续开始
- [x] 数据库变化？

## Improvements

- [ ] 第一次之后还能更改每天背单词数，主界面上可能需要添加"设置"的入口
- [ ] 熟悉度改为6级，取词方式也要相应变化
- [x] 按照背诵规则，如果一个单词在某天第一次出现时"没记住/撤销"了，第二次出现时如果记住了还是不会更新熟悉度的。但是退出重新进入背单词之后就丢失了这个信息，就有潜在的bug，而且现在是第一轮背完之后再去复习之前没记住的，这里应该加一个信息用于记录某词在今天是否被背诵过。

