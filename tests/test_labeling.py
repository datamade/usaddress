from usaddress import parse
import training
from training.training import parseTrainingData

#tests to ensure that the parser maintains performance on various simple address patterns

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
