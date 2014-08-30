from usaddress import parse
import training
from training.training import parseTrainingData

class TestSynthetic(object) :
    def test_Parser(self):

        test_file = 'training/test_data/synthetic_data_osm_data_xml.xml'

        for address_text, components in parseTrainingData(test_file) :
            _, labels_true = zip(*components)
            _, labels_pred = zip(*parse(address_text))
            yield equals, address_text, labels_pred, labels_true


class TestUS50_2(object) :
    def test_Parser(self):

        test_file = 'training/test_data/us50_test_tagged.xml'

        for address_text, components in parseTrainingData(test_file) :
            _, labels_t = zip(*components)
            _, labels = zip(*parse(address_text))
            
            yield fuzzyEquals, address_text, labels_t, labels



def equals(addr, 
           labels_pred, 
           labels_true) :
    print "ADDRESS: ", addr
    assert labels_pred == labels_true

def fuzzyEquals(addr, 
           labels_true, 
           labels_pred) :
    print "ADDRESS: ", addr
    labels = []
    fuzzy_labels = []
    for label in labels_pred:
        if label == 'StreetNamePostType' or label == 'StreetNamePreDirectional':
            fuzzy_labels.append('StreetName')
        else:
            fuzzy_labels.append(label)
    for label in labels_true:
        labels.append(label)
    assert fuzzy_labels == labels
