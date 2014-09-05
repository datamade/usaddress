from usaddress import parse, tokenize
import training
from training.training import parseTrainingData

class TestSynthetic(object) :
    def test_Parser(self):

        test_file = 'training/test_data/synthetic_osm_data_xml.xml'

        for address_text, components in parseTrainingData(test_file) :
            _, labels_true = zip(*components)
            _, labels_pred = zip(*parse(address_text))
            yield equals, address_text, labels_pred, labels_true


class TestUS50_2(object) :
    def test_Parser(self):

        test_file = 'training/test_data/us50_test_tagged.xml'

        for address_text, components in parseTrainingData(test_file) :
            _, labels_true = zip(*components)
            _, labels_pred = zip(*parse(address_text))
            
            yield fuzzyEquals, address_text, labels_pred, labels_true

class TestTokenizing(object) :
    def test_Tokenizer(self):

        test_strings = [
        [ '# 1 abc st.', ['#', '1', 'abc', 'st.'] ],
        [ '#1 abc st', ['#', '1', 'abc', 'st'] ],
        [ '1 abc st,suite 1', ['1', 'abc', 'st,', 'suite', '1'] ],
        [ '1 abc st;suite 1', ['1', 'abc', 'st;', 'suite', '1'] ],
        [ '1-5 abc road', ['1-5', 'abc', 'road'] ],
        [ '222 W. Merchandise Mart Plaza, Chicago, IL 60654', ['222', 'W.', 'Merchandise', 'Mart', 'Plaza,', 'Chicago,', 'IL', '60654'] ],
        [ '222  W.  Merchandise  Mart  Plaza,  Chicago,  IL  60654   ', ['222', 'W.', 'Merchandise', 'Mart', 'Plaza,', 'Chicago,', 'IL', '60654'] ],
        [ 'Box #1, Chicago, IL 60654', ['Box', '#', '1,', 'Chicago,', 'IL', '60654'] ],
        [ 'Box # 1, Chicago, IL 60654', ['Box', '#', '1,', 'Chicago,', 'IL', '60654'] ]
        ]

        for addr in test_strings:
            yield tokenEquals, addr[0], addr[1]



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
        else:
            fuzzy_labels.append(label)
    for label in labels_true:
        labels.append(label)
    print "ADDRESS:    ", addr
    print "fuzzy pred: ", fuzzy_labels
    print "true:       ", labels
    assert fuzzy_labels == labels

def tokenEquals(addr_string, correct_tokens) :
    print "ADDRESS: ", addr_string
    assert tokenize(addr_string) == correct_tokens
