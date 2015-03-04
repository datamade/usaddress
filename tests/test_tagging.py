import unittest
import usaddress

class TestTagging(unittest.TestCase) :

    def test_broadway(self) :
        s1 = '1775 Broadway And 57th, Newyork NY'
        print usaddress.tag(s1)
        assert 1 == 0


