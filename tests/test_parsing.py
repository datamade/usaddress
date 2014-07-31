import usaddress
import unittest

class ParseTest(unittest.TestCase) :
    def test_simple(self) :
        assert usaddress.parse('123 Main St. Chicago, IL 60647') ==\
            [('123', 'street number'), ('Main', 'street'), 
             ('St.', 'street type'), ('Chicago,', 'city'), 
             ('IL', 'state'), ('60647', 'zip')]
            
