#!/usr/bin/env python
import datetime
import unittest
import random
import os
import shutil

from StudyPlan import TodayList
from StudyPlan import Vocab

from WordDict import WordDict

word_dict = WordDict.WordDict()
load_err = word_dict.load('WordDict\\dict')


class Test_StudyPlan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.exists('StudyPlan/Vocab.pkl'):
            shutil.copyfile('StudyPlan/Vocab.pkl', 'StudyPlan/Vocab_copy_during_test.pkl')
        if os.path.exists('StudyPlan/TodayList.pkl'):
            shutil.copyfile('StudyPlan/TodayList.pkl', 'StudyPlan/TodayList_copy_during_test.pkl')

    @classmethod
    def tearDownClass(cls):
        if os.path.exists('StudyPlan/Vocab_copy_during_test.pkl'):
            shutil.copyfile('StudyPlan/Vocab_copy_during_test.pkl', 'StudyPlan/Vocab.pkl')
            os.remove('StudyPlan/Vocab_copy_during_test.pkl')
        if os.path.exists('StudyPlan/TodayList_copy_during_test.pkl'):
            shutil.copyfile('StudyPlan/TodayList_copy_during_test.pkl', 'StudyPlan/TodayList.pkl')
            os.remove('StudyPlan/TodayList_copy_during_test.pkl')

    def setUp(self):
        word_dict.get_wordlist()

    def test_01_saveVocab(self):
        if os.path.exists('StudyPlan/Vocab.pkl'):
            os.remove('StudyPlan/Vocab.pkl')
        vocab = Vocab.Vocab(word_dict)
        vocab.saveVocab()
        self.assertTrue(os.path.exists('StudyPlan/Vocab.pkl'))

    def test_02_init_vocab(self):
        if os.path.exists('StudyPlan/Vocab.pkl'):
            os.remove('StudyPlan/Vocab.pkl')

        # 如果是第一次使用软件，则初始化词汇表的方式应该是CREATE_NEW_VOCAB，且词库表中单词数目与本地词库文件中存储的单词数目相等
        vocab = Vocab.Vocab(word_dict)
        self.assertEqual(vocab.init_method, Vocab.CREATE_NEW_VOCAB)
        self.assertEqual(len(vocab.getVocabDict()), len(word_dict.word_list))
        vocab.saveVocab()

        # 如果不是第一次使用软件，则则初始化词汇表的方式应该是LOAD_EXISTING_VOCAB，直接加载已有的pickle文件
        vocab = Vocab.Vocab(word_dict)
        self.assertEqual(vocab.init_method, Vocab.LOAD_EXISTING_VOCAB)
        self.assertEqual(len(vocab.getVocabDict()), len(word_dict.word_list))

    def test_03_getInfo(self):
        vocab = Vocab.Vocab(word_dict)

        # 测试用例：已经在Vocab中的单词
        word = random.choice(list(vocab.getVocabDict().keys()))
        self.assertEqual(vocab.getInfo(word), word_dict.get_info(word))

        # 测试用例：不在Vocab中但确实存在的单词
        word = 'electromechanical'
        self.assertFalse(word in vocab.getVocabDict().keys())
        self.assertFalse(word in word_dict.word_list)
        self.assertEqual(vocab.getInfo(word), word_dict.get_info(word))

        # 测试用例：不正确的单词
        word = 'asdfgh'
        self.assertEqual(vocab.getInfo(word), WordDict.WORD_NOT_FOUND)

    def test_04_updateFamiliarity(self):
        vocab = Vocab.Vocab(word_dict)

        # 不在词库中的单词，无法更新
        word = 'electromechanical'
        self.assertEqual(vocab.updateFamiliarity(word, 1), -1)

        # 在词库中的单词，可以进行更新。熟悉度只能是0,1,2三种，如果小于0则应更新为0，如果大于2则更新为2
        word = random.choice(list(vocab.getVocabDict().keys()))
        self.assertEqual(vocab.updateFamiliarity(word, -1), 0)
        self.assertEqual(vocab.updateFamiliarity(word, 0), 0)
        self.assertEqual(vocab.updateFamiliarity(word, 1), 1)
        self.assertEqual(vocab.updateFamiliarity(word, 2), 2)
        self.assertEqual(vocab.updateFamiliarity(word, 3), 2)

    def test_05_getFamiliarity(self):
        vocab = Vocab.Vocab(word_dict)

        # 不在词库中的单词，无法获得
        word = 'electromechanical'
        self.assertEqual(vocab.getFamiliarity(word), -1)

        # 在词库中的单词，可以正确返回
        word = random.choice(list(vocab.getVocabDict().keys()))
        self.assertEqual(vocab.getFamiliarity(word), 0)
        # 熟悉度更新的单词，也可正确返回更新后的熟悉度
        vocab.updateFamiliarity(word, 1)
        self.assertEqual(vocab.getFamiliarity(word), 1)

    def test_06_getNewVocabList(self):
        vocab = Vocab.Vocab(word_dict)

        # 随机选取Vocab中的10个单词作为生词，相当于测试用例
        familiarity = [1, 2]
        for key in vocab.getVocabDict().keys():
            vocab.updateFamiliarity(key, random.choice(familiarity))
        new_word_list = random.sample(list(vocab.getVocabDict().keys()), 10)
        for word in new_word_list:
            vocab.updateFamiliarity(word, 0)

        # 确认测试用例与输出结果是否相符
        self.assertTrue(set(new_word_list).issuperset(set(vocab.getNewVocabList())) and set(
            vocab.getNewVocabList()).issuperset(set(new_word_list)))

    def test_07_word_is_valid(self):
        vocab = Vocab.Vocab(word_dict)
        # 词库表中的单词
        self.assertTrue(vocab.word_is_valid('afternoon'))
        # 不在词库表中但正确的单词
        self.assertTrue(vocab.word_is_valid('tribology'))
        # 不正确的单词
        self.assertFalse(vocab.word_is_valid('asdfg'))

    def test_08_add_word_to_vocab(self):
        vocab = Vocab.Vocab(word_dict)
        # 如果添加词库中已有的单词，则其熟悉度应变为0
        word = random.choice(list(vocab.getVocabDict().keys()))
        vocab.updateFamiliarity(word, 1)
        vocab.add_word_to_vocab(word)
        self.assertEqual(vocab.getFamiliarity(word), 0)

        # 添加不正确的单词，添加失败
        self.assertFalse(vocab.add_word_to_vocab('asdfg'))

        # 添加不在词库中的正确单词，添加成功
        self.assertFalse('electromechanical' in vocab.getVocabDict().keys())
        vocab.add_word_to_vocab('electromechanical')
        self.assertTrue(
            'electromechanical' in vocab.getVocabDict().keys() and vocab.getVocabDict()['electromechanical'] == 0)
        # 重启程序后还是能获取新添加的单词
        vocab = Vocab.Vocab(word_dict)
        self.assertTrue(
            'electromechanical' in vocab.getVocabDict().keys() and vocab.getVocabDict()['electromechanical'] == 0)

    def test_09_remove_word_from_vocab(self):
        vocab = Vocab.Vocab(word_dict)
        # 删除词库中已有的单词
        self.assertTrue('electromechanical' in vocab.getVocabDict().keys())
        self.assertTrue(vocab.remove_word_from_vocab('electromechanical'))
        self.assertFalse('electromechanical' in vocab.getVocabDict().keys())

        # 不正确的单词，无法删除
        self.assertFalse(vocab.remove_word_from_vocab('asfg'))
        self.assertTrue(vocab.remove_word_from_vocab('afternoon'))
        self.assertFalse('afternoon' in vocab.getVocabDict().keys())

        vocab.add_word_to_vocab('afternoon')

        # 测试词库不能被完全删除，至少保留1个单词
        shutil.copyfile('StudyPlan/Vocab.pkl', 'StudyPlan/Vocab_copy.pkl')
        self.assertTrue(os.path.exists('StudyPlan/Vocab_copy.pkl'))
        vocab_copy = Vocab.Vocab(word_dict)
        self.assertEqual(vocab_copy.init_method, Vocab.LOAD_EXISTING_VOCAB)
        word = random.choice(list(vocab.getVocabDict().keys()))
        for key in vocab.getVocabDict().keys():
            if key != word:
                self.assertTrue(vocab_copy.remove_word_from_vocab(key))
        self.assertFalse(vocab_copy.remove_word_from_vocab(word))
        self.assertEqual(len(vocab_copy.getVocabDict()), 1)

        shutil.copyfile('StudyPlan/Vocab_copy.pkl', 'StudyPlan/Vocab.pkl')
        os.remove('StudyPlan/Vocab_copy.pkl')
        self.assertFalse(os.path.exists('StudyPlan/Vocab_copy.pkl'))

    def test_10_get_n_word_from_familiarVocab(self):
        vocab = Vocab.Vocab(word_dict)
        # 设置50个单词为熟悉单词
        set_familiar_word_list = random.sample(list(vocab.getVocabDict().keys()), 50)
        for word in set_familiar_word_list:
            vocab.updateFamiliarity(word, 2)

        # 输入数据有效：从中选取10个单词组成返回列表
        get_list = vocab.get_n_word_from_familiarVocab(10)
        self.assertIsInstance(get_list, list)
        self.assertEqual(len(get_list), 10)
        self.assertTrue(set(get_list).issubset(set(set_familiar_word_list)))

        # 输入数据无效：n值过大，返回空列表
        get_list = vocab.get_n_word_from_familiarVocab(60)
        self.assertEqual(len(get_list), 0)

        # 输入数据无效：n值非正数，返回空列表
        get_list = vocab.get_n_word_from_familiarVocab(-1)
        self.assertEqual(len(get_list), 0)

    def test_11_init_todaylist(self):
        if os.path.exists('StudyPlan/TodayList.pkl'):
            os.remove('StudyPlan/TodayList.pkl')

        # 新用户第一次使用软件
        vocab = Vocab.Vocab(word_dict)
        todaylist_obj = TodayList.TodayList(vocab)
        self.assertTrue(todaylist_obj.new_user)
        todaylist_obj.plan_for_new_user(20, vocab)
        todaylist_dict = todaylist_obj.getTodayList()
        self.assertEqual(len(todaylist_dict), 20)

        # 确认所有单词都没有背过
        all_value_0_in_todaylist = True
        for k in todaylist_dict:
            if not (todaylist_dict[k] == 0):
                all_value_0_in_todaylist = False
                break
        self.assertTrue(all_value_0_in_todaylist)

        # 确认是否能按照正确的词数分配方法，从不同熟悉度的单词中挑选组成每日计划
        # 情况1：生词数量多，不熟悉的单词不够
        all_familiarity_0_in_todaylist = True
        for k in todaylist_dict:
            if not (vocab.getFamiliarity(k) == 0):
                all_familiarity_0_in_todaylist = False
                break
        self.assertTrue(all_familiarity_0_in_todaylist)

        # 情况2：不熟悉的单词多，生词数量不够
        for k in vocab.getVocabDict().keys():
            vocab.updateFamiliarity(k, 1)
        todaylist_obj.plan_for_new_user(20, vocab)
        todaylist_dict = todaylist_obj.getTodayList()
        all_familiarity_1_in_todaylist = True
        for k in todaylist_dict:
            if not (vocab.getFamiliarity(k) == 1):
                all_familiarity_1_in_todaylist = False
                break
        self.assertTrue(all_familiarity_1_in_todaylist)

        # 情况3：熟悉的单词多，生词和不熟悉单词数量不够
        for k in vocab.getVocabDict().keys():
            vocab.updateFamiliarity(k, 2)
        todaylist_obj.plan_for_new_user(20, vocab)
        todaylist_dict = todaylist_obj.getTodayList()
        all_familiarity_2_in_todaylist = True
        for k in todaylist_dict:
            if not (vocab.getFamiliarity(k) == 2):
                all_familiarity_2_in_todaylist = False
                break
        self.assertTrue(all_familiarity_2_in_todaylist)

        # 情况4：各种单词数量都足够生成计划
        new_num = unfamiliar_num = 0
        for k in list(vocab.getVocabDict().keys())[:100]:
            vocab.updateFamiliarity(k, 0)
        for k in list(vocab.getVocabDict().keys())[200:400]:
            vocab.updateFamiliarity(k, 1)
        todaylist_obj.plan_for_new_user(20, vocab)
        todaylist_dict = todaylist_obj.getTodayList()
        for k in todaylist_dict:
            if vocab.getFamiliarity(k) == 0:
                new_num += 1
            if vocab.getFamiliarity(k) == 1:
                unfamiliar_num += 1
        self.assertEqual(new_num, 12)
        self.assertEqual(unfamiliar_num, 8)

    def test_12_add_word_to_todaylist(self):
        vocab = Vocab.Vocab(word_dict)
        todaylist_obj = TodayList.TodayList(vocab)
        todaylist_obj.plan_for_new_user(10, vocab)
        todaylist_dict = todaylist_obj.getTodayList()

        # 添加已经在计划中的单词
        word = random.choice(list(todaylist_dict.keys()))
        self.assertFalse(todaylist_obj.add_word_to_todaylist(word, vocab))

        # 添加不在计划中的单词
        while True:
            word = random.choice(list(vocab.getVocabDict().keys()))
            if word not in todaylist_dict.keys():
                break
        self.assertTrue(todaylist_obj.add_word_to_todaylist(word, vocab))
        self.assertEqual(len(todaylist_obj.getTodayList()), 11)
        # 重新打开程序仍然存在
        todaylist_obj = TodayList.TodayList(vocab)
        self.assertEqual(len(todaylist_obj.getTodayList()), 11)

        # 添加不正确的单词（无法添加）
        self.assertFalse(todaylist_obj.add_word_to_todaylist('dsddsds', vocab))

    def test_13_get_n_word_from_todaylist(self):
        vocab = Vocab.Vocab(word_dict)
        todaylist_obj = TodayList.TodayList(vocab)
        todaylist_dict = todaylist_obj.getTodayList()

        # 合法的n
        get_list = todaylist_obj.get_n_word_from_todaylist(5)
        self.assertTrue(set(get_list).issubset(set(list(todaylist_dict.keys()))))

        # 不合法的n，n比今日计划中的单词数要多
        get_list = todaylist_obj.get_n_word_from_todaylist(20)
        self.assertEqual(len(get_list), 0)

    def test_14_time_concept(self):
        vocab = Vocab.Vocab(word_dict)
        todaylist_obj = TodayList.TodayList(vocab)
        todaylist_obj.plan_for_new_user(50, vocab)
        todaylist_obj.save_todaylist()
        pre_todaylist = list(todaylist_obj.getTodayList().keys())

        # 同一天打开
        todaylist_obj = TodayList.TodayList(vocab)
        curr_todaylist = list(todaylist_obj.getTodayList().keys())
        self.assertTrue(pre_todaylist == curr_todaylist)

        # 不同天打开
        pre_todaylist = curr_todaylist
        todaylist_obj.change_date(datetime.date.today() + datetime.timedelta(days=1))
        todaylist_obj.save_todaylist()
        todaylist_obj = TodayList.TodayList(vocab)
        curr_todaylist = list(todaylist_obj.getTodayList().keys())
        self.assertFalse(pre_todaylist == curr_todaylist)


if __name__ == "__main__":
    unittest.main()
