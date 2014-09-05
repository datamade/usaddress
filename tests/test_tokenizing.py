from usaddress import tokenize
import unittest

class TestTokenizing(unittest.TestCase) :
    def test_hash(self):
        
        assert tokenize('# 1 abc st.') == ['#', '1', 'abc', 'st.']
        assert tokenize('#1 abc st') == ['#', '1', 'abc', 'st']

    def test_punc_split(self) :
        assert tokenize('1 abc st,suite 1') == ['1', 'abc', 'st,', 'suite', '1']
        

        # Turn these all into these types of tests, broken into separate
        # usefully named functions, (all test functions have to start with 
        # test, i.e. test_foo

        # test_strings = [
        # [  ],
        # [  ],
        # [ '1 abc st;suite 1', ['1', 'abc', 'st;', 'suite', '1'] ],
        # [ '1-5 abc road', ['1-5', 'abc', 'road'] ],
        # [ '222 W. Merchandise Mart Plaza, Chicago, IL 60654', ['222', 'W.', 'Merchandise', 'Mart', 'Plaza,', 'Chicago,', 'IL', '60654'] ],
        # [ '222  W.  Merchandise  Mart  Plaza,  Chicago,  IL  60654   ', ['222', 'W.', 'Merchandise', 'Mart', 'Plaza,', 'Chicago,', 'IL', '60654'] ],
        # [ 'Box #1, Chicago, IL 60654', ['Box', '#', '1,', 'Chicago,', 'IL', '60654'] ],
        # [ 'Box # 1, Chicago, IL 60654', ['Box', '#', '1,', 'Chicago,', 'IL', '60654'] ]
        # ]

if __name__ == '__main__' :
    unittest.main()    
