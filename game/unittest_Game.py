import unittest
from random import choice
from game.gameSystem import *
from WordDict.WordDict import *
import os

pklpath = 'game/Game.pkl'
init_Game = [0, 0, 0]
print(os.getcwd())

class Test_Game(unittest.TestCase):

    def test_01_saveGame(self):
        if os.path.exists(pklpath):
            os.remove(pklpath)

        WORD_DICT = WordDict()
        WORD_DICT.load('WordDict/dict')
        myGame = gameSystem(WORD_DICT)

        self.assertTrue(os.path.exists(pklpath))

    def test_02_initGame(self):
        if os.path.exists(pklpath):
            os.remove(pklpath)

        WORD_DICT = WordDict()
        WORD_DICT.load('WordDict/dict')
        myGame = gameSystem(WORD_DICT)
        self.assertEqual(len(myGame.allWords), len(WORD_DICT.word_list))
        word = choice(WORD_DICT.word_list)
        self.assertEqual(myGame.vocab_dict[word], init_Game)
        self.assertEqual(len(myGame.allWords), len(WORD_DICT.word_list))
        # print('words!')

    def test_03_updateGameHist(self):

        WORD_DICT = WordDict()
        WORD_DICT.load(os.path.dirname(os.getcwd()) + '/WordDict/dict')
        myGame = gameSystem(WORD_DICT)

        word = choice(WORD_DICT.word_list)
        wordACC = {word: True}
        oldHist = myGame.vocab_dict[word]
        newHist = [(oldHist[1] + 1)/(oldHist[2] + 1), oldHist[1] + 1, oldHist[2] + 1]
        self.assertEqual(myGame.vocab_dict[word], oldHist)
        myGame.updateGameHist(wordACC)
        self.assertEqual(myGame.vocab_dict[word], newHist)

        word = choice(WORD_DICT.word_list)
        wordACC = {word: False}
        oldHist = myGame.vocab_dict[word]
        newHist = [(oldHist[1]) / (oldHist[2] + 1), oldHist[1], oldHist[2] + 1]
        self.assertEqual(myGame.vocab_dict[word], oldHist)
        myGame.updateGameHist(wordACC)
        self.assertEqual(myGame.vocab_dict[word], newHist)
