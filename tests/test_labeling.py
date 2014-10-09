from usaddress import parse
import training
from training.training import parseTrainingData
import unittest

#tests to ensure that the parser maintains performance on various simple address patterns
class TestManualAddr2XML(unittest.TestCase) :

    def test_simple_addresses(self):
        test_file = 'training/test_data/simple_address_patterns.xml'

        for address_text, components in parseTrainingData(test_file) :
            _, labels_true = zip(*components)
            _, labels_pred = zip(*parse(address_text))
            yield equals, address_text, labels_pred, labels_true


def equals(addr, 
           labels_pred, 
           labels_true) :
    print "ADDRESS: ", addr
    assert labels_pred == labels_true
