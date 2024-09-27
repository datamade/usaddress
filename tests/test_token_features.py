import unittest

from usaddress import tokenFeatures


class TestTokenFeatures(unittest.TestCase):
    def test_unicode(self):
        features = tokenFeatures("å")
        assert features["endsinpunc"] is False


if __name__ == "__main__":
    unittest.main()
