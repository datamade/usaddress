from usaddress import parse
import training
from training.training import parseTrainingData
import unittest

#tests to ensure that the parser maintains accuracy on various simple address patterns
class TestSimple(unittest.TestCase) :

    def test_simple_addresses(self):
        test_file = 'training/test_data/simple_address_patterns.xml'

        for address_text, components in parseTrainingData(test_file) :
            _, labels_true = zip(*components)
            _, labels_pred = zip(*parse(address_text))
            yield equals, address_text, labels_pred, labels_true

class TestSynthetic(unittest.TestCase) :
    def test_Parser(self):

        test_file = 'test_data/synthetic_osm_data_xml.xml'

        for address_text, components in parseTrainingData(test_file) :
            _, labels_true = zip(*components)
            _, labels_pred = zip(*parse(address_text))
            yield equals, address_text, labels_pred, labels_true


class TestUS50_2(unittest.TestCase) :
    def test_Parser(self):

        test_file = 'test_data/us50_test_tagged.xml'

        for address_text, components in parseTrainingData(test_file) :
            _, labels_true = zip(*components)
            _, labels_pred = zip(*parse(address_text))
            
            yield fuzzyEquals, address_text, labels_pred, labels_true


def equals(addr, 
           labels_pred, 
           labels_true) :
    print "ADDRESS: ", addr
    assert labels_pred == labels_true

def fuzzyEquals(addr, 
                labels_pred,
                labels_true) : 
    labels = []
    fuzzy_labels = []
    for label in labels_pred:
        if label.startswith('StreetName') :
            fuzzy_labels.append('StreetName')
        elif label.startswith('AddressNumber') :
            fuzzy_labels.append('AddressNumber')
        else:
            fuzzy_labels.append(label)
    for label in labels_true:
        labels.append(label)
    print "ADDRESS:    ", addr
    print "fuzzy pred: ", fuzzy_labels
    print "true:       ", labels

    assert fuzzy_labels == labels