# 生词本及学习计划

## 生成每日背单词计划表

### 文件说明

#### Vocab.py

包括Vocab类，将WordDict转变为词汇表
Vocab为一dict，其中key为单词，value为该单词的熟悉度

#### Vocab.pkl

存储Vocab的pickle文件
由于每次背完单词后需要更新单词的熟悉度，因此需用pickle文件保存下来，下次运行时读取

#### TodayList.py

包括TodayList类，从Vocab中选取一定的数量的词汇构成每日的计划列表
todayList为一个list，为每日计划表，如：['a', 'baby', 'cat', ...]

#### testTodayList.py

测试用文件

## 背单词

### 文件说明

#### recite_action.py

* 完善由`pyuic`翻译出的recite_gui.py，定义slot和signal。
* 完成背单词操作

#### GUI/

* **recite_gui.\***：recite_gui.ui由Qt Designer设计，运行`pyuic5 -o recite_gui.py recite_gui.ui`后生成recite_gui.py
* **congrats.\***：congrats.qrc为资源文件，congrats.py定义了资源模块，用于描述图片congrats.jpg，显示于背完所有今日词汇后的祝贺界面

## Task List

- [x] 计划生成：从指定WordDict中随机选取新词，从Vocab中根据熟悉度生成复习词汇，组成今日计划TodayList (zr)
- [x] 背单词：GUI+更改Vocab中熟悉度 (lqa)
- [x] 存档：Vocab要存入文件，下次运行时读取 (zr)
- [ ] "今天"继续开始
- [ ] 数据库变化？

## Improvements

- [ ] user-defined每天背单词数，如果太多像扇贝那样循序增加？