from usaddress import parse, GROUP_LABEL
from parserator.training import readTrainingData
import unittest

class TestSimpleAddresses(unittest.TestCase) :
    def test_simple_addresses(self):
        test_file = 'measure_performance/test_data/simple_address_patterns.xml'
        data = list(readTrainingData([test_file], GROUP_LABEL))

        for labeled_address in data :
            address_text, components = labeled_address
            _, labels_true = zip(*components)
            _, labels_pred = zip(*parse(address_text))
            yield equals, address_text, labels_pred, labels_true

class TestSyntheticAddresses(unittest.TestCase) :
    def test_synthetic_addresses(self):

        test_file = 'measure_performance/test_data/synthetic_osm_data.xml'
        data = list(readTrainingData([test_file], GROUP_LABEL))

        for labeled_address in data :
            address_text, components = labeled_address
            _, labels_true = zip(*components)
            _, labels_pred = zip(*parse(address_text))
            yield equals, address_text, labels_pred, labels_true

class TestUS50Addresses(unittest.TestCase) :
    def test_us50(self):
        test_file = 'measure_performance/test_data/us50_test_tagged.xml'
        data = list(readTrainingData([test_file], GROUP_LABEL))

        for labeled_address in data :
            address_text, components = labeled_address
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

if __name__== "__main__":
    unittest.main()