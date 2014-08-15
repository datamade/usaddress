import pycrfsuite
import usaddress
from usaddress import NULL_TAG
import random
import os
from lxml import etree

def addr2labels(address):
    labels = []
    for i in range(len(address)):
        if address[i][1]:
            labels.append(address[i][1])
        else:
            labels.append(NULL_TAG)
    return tuple(labels)

def trainModel(training_data, model_file) :

    X = []
    Y = []

    for address_text, components in training_data :
        X.append(usaddress.addr2features(components))
        Y.append(addr2labels(components))

    #train model
    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(X, Y):
        trainer.append(xseq, yseq)

    trainer.train(model_file)

def parseTrainingData(filepath):
    tree = etree.parse(filepath)
    address_collection = tree.getroot()
	
    for address in address_collection :
        address_components = []
        address_text = etree.tostring(address, method='text')
        for component in list(address) :
            address_components.append([component.text, component.tag])
            if component.tail and component.tail.strip() :
                address_components.append([component.tail.strip(), NULL_TAG])

        yield address_text, address_components 

if __name__ == '__main__' :
    root_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
    
    training_data = parseTrainingData(root_path + '/training/training_data/synthetic_data_osm_cleaned.xml')

    trainModel(training_data, root_path + '/usaddress/usaddr.crfsuite')
