from WordDict.UnitTest import Test_WordDict
from StudyPlan.test_studyPlan import Test_StudyPlan
from game.test import Test_Game as Test_Game0
from game.unittest_Game import *
import unittest

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Test_WordDict))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Test_StudyPlan))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Test_Game))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    Test_Game0()
