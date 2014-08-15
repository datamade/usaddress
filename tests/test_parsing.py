import usaddress
import unittest
import training
import pycrfsuite
import random
import re

class ParseTest(unittest.TestCase) :
    def test_simple(self) :
        assert usaddress.parse('123 Main St. Chicago, IL 60647') ==\
            [('123', 'street number'), ('Main', 'street'), 
             ('St.', 'street type'), ('Chicago,', 'city'), 
             ('IL', 'state'), ('60647', 'zip')]

class TestSynthetic(object) :
    def __init__(self) :
        synthetictrainfile = 'training_data/synthetic_data_osm_cleaned.xml'
        data = training.parse.parseTrainingData(synthetictrainfile)
        random.shuffle(data)
        train_data = data[0:50]
        self.test_data = data[5000:20000]

        #prep data
        x_train = [training.training.addr2features(addr) for addr in train_data]
        y_train = [training.training.addr2labels(addr) for addr in train_data]

        #train model
        trainer = pycrfsuite.Trainer(verbose=False)
        for xseq, yseq in zip(x_train, y_train):
            trainer.append(xseq, yseq)
        self.modelfile = "training/models/"+re.sub(r'/W', '_', 'testing')+".crfsuite"
        trainer.train(self.modelfile)

    def test_Parser(self):

        tagger = pycrfsuite.Tagger()
        tagger.open(self.modelfile)
        #total_addr_count = len(test_data)
        #correct_count = 0
        assert len(self.test_data) > 0
        for addr in self.test_data:
            #address = training.addr2tokens(addr)
            labels_pred = tagger.tag(training.training.addr2features(addr))
            labels_true = training.training.addr2labels(addr)
            yield equals, labels_pred, labels_true, addr

def equals(labels_pred, labels_true, addr):
    print zip(*addr)
    assert labels_pred == labels_true
