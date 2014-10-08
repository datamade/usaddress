import pycrfsuite
import usaddress
import random
import os
from lxml import etree
from imp import reload

NULL_TAG = 'Null'

def trainModel(training_data, model_file,
               params_to_set={'c1':0.1, 'c2':0.01, 'feature.minfreq':0}):

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

def parseTrainingData(filepath):
    tree = etree.parse(filepath)
    address_collection = tree.getroot()

    for address in address_collection:
        address_components = []
        address_text = etree.tostring(address, method='text')
        address_text = address_text.replace('&#38;', '&')
        for component in list(address):
            address_components.append([component.text, component.tag])
            if component.tail and component.tail.strip():
                address_components.append([component.tail.strip(), NULL_TAG])

        yield address_text, address_components


def get_data_sklearn_format(path='training/training_data/labeled.xml'):
    """
    Parses the specified data file and returns it in sklearn format.
    :param path:
    :return: tuple of:
                1) list of training addresses, each of which is a string
                2) list of gold standard labels, each of which is a tuple
                of strings, one for each token in the corresponding training
                address
    """
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
