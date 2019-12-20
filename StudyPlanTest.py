from StudyPlan.test_studyPlan import Test_StudyPlan
import unittest

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Test_StudyPlan))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
