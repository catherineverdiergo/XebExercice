import unittest
from mowerstestplayer import MowersTestPlayer


class MowerTestCase(unittest.TestCase):

    def test1(self):
        # Open and parse test file
        player = MowersTestPlayer('testmowers1.data')
        player.open()
        # play test
        results = player.apply()
        # check results
        self.assertEqual("1 3 N", results[0])
        self.assertEqual("5 1 E", results[1])

    def test2(self):
        # Open and parse test file
        player = MowersTestPlayer('testmowers2.data')
        player.open()
        # play test
        results = player.apply()
        # for r in results:
        #     print(r)
        # check results
        self.assertEqual("0 0 E", results[0])
        self.assertEqual("0 0 E", results[1])

    def test3(self):
        # Open and parse test file
        player = MowersTestPlayer('testmowers3.data')
        player.open()
        # play test
        results = player.apply()
        # for r in results:
        #     print(r)
        # check results
        self.assertEqual("3 2 E", results[0])
        # self.assertEqual("0 0 E", results[1])


if __name__ == '__main__':
    unittest.main()
