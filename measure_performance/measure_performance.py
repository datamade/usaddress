from __future__ import print_function
from builtins import zip
from builtins import object
from usaddress import parse
from training import parseTrainingData


class TestSynthetic(object) :
    def test_Parser(self):

        test_file = 'test_data/synthetic_osm_data_xml.xml'

        for address_text, components in parseTrainingData(test_file) :
            _, labels_true = list(zip(*components))
            _, labels_pred = list(zip(*parse(address_text)))
            yield equals, address_text, labels_pred, labels_true


class TestUS50_2(object) :
    def test_Parser(self):

        test_file = 'test_data/us50_test_tagged.xml'

        for address_text, components in parseTrainingData(test_file) :
            _, labels_true = list(zip(*components))
            _, labels_pred = list(zip(*parse(address_text)))
            
            yield fuzzyEquals, address_text, labels_pred, labels_true


class TestOpenaddress(object) :
    def test_us_ia_linn(self) :

        test_file = 'training_data/openaddress_us_ia_linn.xml'

        for address_text, components in parseTrainingData(test_file) :
            _, labels_true = list(zip(*components))
            _, labels_pred = list(zip(*parse(address_text)))
            yield equals, address_text, labels_pred, labels_true


def equals(addr, 
           labels_pred, 
           labels_true) :
    print("ADDRESS: ", addr)
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
    print("ADDRESS:    ", addr)
    print("fuzzy pred: ", fuzzy_labels)
    print("true:       ", labels)

    assert fuzzy_labels == labels
