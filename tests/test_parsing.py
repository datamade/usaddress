from usaddress import parse
import training
from training.training import parseTrainingData

class TestSynthetic(object) :
    def test_Parser(self):

        test_file = 'training/training_data/synthetic_data_osm_data_xml.xml'

        for address_text, components in parseTrainingData(test_file) :
            _, labels_true = zip(*components)
            _, labels_pred = zip(*parse(address_text))
            yield equals, address_text, labels_pred, labels_true


def equals(addr, 
           labels_pred, 
           labels_true) :
    assert labels_pred == labels_true

