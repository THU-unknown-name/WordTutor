from WordDict.UnitTest import Test_WordDict
import unittest

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Test_WordDict))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)