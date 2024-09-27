import unittest

from usaddress import tokenize


class TestTokenizing(unittest.TestCase):
    def test_hash(self):
        self.assertEqual(tokenize("# 1 abc st"), ["#", "1", "abc", "st"])
        self.assertEqual(tokenize("#1 abc st"), ["#", "1", "abc", "st"])
        self.assertEqual(tokenize("box # 1 abc st"), ["box", "#", "1", "abc", "st"])
        self.assertEqual(tokenize("box #1 abc st"), ["box", "#", "1", "abc", "st"])
        self.assertEqual(
            tokenize("box# 1 abc st"),
            ["box", "#", "1", "abc", "st"],
        )
        self.assertEqual(tokenize("box#1 abc st"), ["box", "#", "1", "abc", "st"])

    def test_split_on_punc(self):
        self.assertEqual(
            tokenize("1 abc st,suite 1"), ["1", "abc", "st,", "suite", "1"]
        )
        self.assertEqual(
            tokenize("1 abc st;suite 1"), ["1", "abc", "st;", "suite", "1"]
        )
        self.assertEqual(
            tokenize("1-5 abc road"),
            ["1-5", "abc", "road"],
        )

    def test_spaces(self):
        self.assertEqual(tokenize("1 abc st"), ["1", "abc", "st"])
        self.assertEqual(
            tokenize("1  abc st"),
            ["1", "abc", "st"],
        )
        self.assertEqual(tokenize("1 abc st "), ["1", "abc", "st"])
        self.assertEqual(
            tokenize(" 1 abc st"),
            ["1", "abc", "st"],
        )

    def test_capture_punc(self):
        self.assertEqual(
            tokenize("222 W. Merchandise Mart Plaza"),
            ["222", "W.", "Merchandise", "Mart", "Plaza"],
        )
        self.assertEqual(
            tokenize("222 W Merchandise Mart Plaza, Chicago, IL"),
            ["222", "W", "Merchandise", "Mart", "Plaza,", "Chicago,", "IL"],
        )
        self.assertEqual(tokenize("123 Monroe- St"), ["123", "Monroe-", "St"])

    def test_nums(self):
        self.assertEqual(
            tokenize("222 W Merchandise Mart Plaza Chicago IL 60654"),
            ["222", "W", "Merchandise", "Mart", "Plaza", "Chicago", "IL", "60654"],
        )

    def test_ampersand(self):
        self.assertEqual(tokenize("123 & 456"), ["123", "&", "456"])
        self.assertEqual(tokenize("123&456"), ["123", "&", "456"])
        self.assertEqual(tokenize("123& 456"), ["123", "&", "456"])
        self.assertEqual(tokenize("123 &456"), ["123", "&", "456"])
        self.assertEqual(tokenize("123 &#38; 456"), ["123", "&", "456"])
        self.assertEqual(tokenize("123&#38;456"), ["123", "&", "456"])
        self.assertEqual(tokenize("123&#38; 456"), ["123", "&", "456"])
        self.assertEqual(tokenize("123 &#38;456"), ["123", "&", "456"])
        self.assertEqual(tokenize("123 &amp; 456"), ["123", "&", "456"])
        self.assertEqual(tokenize("123&amp;456"), ["123", "&", "456"])
        self.assertEqual(tokenize("123&amp; 456"), ["123", "&", "456"])
        self.assertEqual(tokenize("123 &amp;456"), ["123", "&", "456"])

    def test_paren(self):
        self.assertEqual(
            tokenize("222 W Merchandise Mart Plaza (1871) Chicago IL 60654"),
            [
                "222",
                "W",
                "Merchandise",
                "Mart",
                "Plaza",
                "(1871)",
                "Chicago",
                "IL",
                "60654",
            ],
        )
        self.assertEqual(
            tokenize("222 W Merchandise Mart Plaza (1871), Chicago IL 60654"),
            [
                "222",
                "W",
                "Merchandise",
                "Mart",
                "Plaza",
                "(1871),",
                "Chicago",
                "IL",
                "60654",
            ],
        )
        self.assertEqual(
            tokenize("222 W Merchandise Mart Plaza(1871) Chicago IL 60654"),
            [
                "222",
                "W",
                "Merchandise",
                "Mart",
                "Plaza",
                "(1871)",
                "Chicago",
                "IL",
                "60654",
            ],
        )


if __name__ == "__main__":
    unittest.main()
