import pycrfsuite
import usaddress
import random
import os
from lxml import etree
from imp import reload

NULL_TAG = 'Null'

def trainModel(training_data, model_file, params_to_set=dict()) :

    X = []
    Y = []

    for address_text, components in training_data:
        tokens, labels = zip(*components)
        X.append(usaddress.addr2features(tokens))
        Y.append(labels)

    # train model
    trainer = pycrfsuite.Trainer(verbose=False, params=params_to_set)
    for xseq, yseq in zip(X, Y):
        trainer.append(xseq, yseq)

    trainer.train(model_file)
    reload(usaddress)
    print(list(usaddress.parse('12 Awesome blvd'))) # todo remove

def parseTrainingData(filepath):
    tree = etree.parse(filepath)
    address_collection = tree.getroot()

    for address in address_collection:
        address_components = []
        address_text = etree.tounicode(address, method='text')
        # address_text = address_text.replace('&#38;', '&')
        for component in list(address):
            address_components.append([component.text, component.tag])
            if component.tail and component.tail.strip():
                address_components.append([component.tail.strip(), NULL_TAG])

        yield address_text, address_components


def get_data_sklearn_format(path='training/training_data/labeled.xml'):
    data = list(parseTrainingData(path))
    random.shuffle(data)

    x, y = [], []
    for address_text, components in data:
        tokens, labels = zip(*components)
        x.append(address_text)
        y.append(labels)
    return x, y


if __name__ == '__main__':
    root_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

    # training_data = list(parseTrainingData(root_path + '/training/training_data/synthetic_data_osm_data_xml.xml'))
    training_data = list(parseTrainingData(root_path + '/training/training_data/labeled.xml'))

    trainModel(training_data, root_path + '/usaddress/usaddr.crfsuite')