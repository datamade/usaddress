from usaddress import parse
import training
from training.training import parseTrainingData

class TestSynthetic(object) :
    def test_Parser(self):

        test_file = 'training/training_data/synthetic_data_osm_cleaned.xml'

        temp_counter = 0 #until we get testing sorted
        for address_text, components in parseTrainingData(test_file) :
            labels_true = training.training.addr2labels(components)
            _, labels_pred = zip(*parse(address_text))
            yield equals, address_text, labels_pred, labels_true
            temp_counter += 1
            if temp_counter > 4 :
                break


def equals(addr, 
           labels_pred, 
           labels_true) :
    assert labels_pred == labels_true

