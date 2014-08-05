import pycrfsuite
import re
import string
import parse


def tokenFeatures(token) :

    features = {'token.lower' : token.lower(), 
                #'token.isupper' : token.isupper(), 
                #'token.islower' : token.islower(), 
                #'token.istitle' : token.istitle(), 
                'token.isdigit' : token.isdigit(),
                #'digit.length' : token.isdigit() * len(token),
                #'token.ispunctuation' : (token in string.punctuation),
                #'token.length' : len(token),
                #'ends_in_comma' : token[-1] == ','
                }

    return features

def token2features(address, i):
    features = tokenFeatures(address[i][0])


    if i > 0:
        previous_features = tokenFeatures(address[i-1][0])
        for key, value in previous_features.items() :
            features['previous.' + key] = value
    else :
        features['address.start'] = True

    if i+1 < len(address) :
        next_features = tokenFeatures(address[i+1][0])
        for key, value in next_features.items() :
            features['next.' + key] = value
    else :
        features['address.end'] = True

    return [str(each) for each in features.items()]

def addr2features(address):
    return [token2features(address, i) for i in range(len(address))]

def addr2labels(address):
    return [address[i][1] for i in range(len(address))]

def addr2tokens(address):
    return [address[i][0] for i in range(len(address))]


# **** us50 data ****
# prep the training & test data
#train_data = parse.parseLines('data/us50.train.tagged')
#x_train = [addr2features(addr) for addr in train_data]
#y_train = [addr2labels(addr) for addr in train_data]

#test_data = parse.parseLines('data/us50.test.tagged')
#x_test = [addr2features(addr) for addr in test_data]
#y_test = [addr2labels(addr) for addr in test_data]

# train model
#trainer = pycrfsuite.Trainer(verbose=False)
#for xseq, yseq in zip(x_train, y_train):
#    trainer.append(xseq, yseq)
#trainer.train('../usaddress/usaddr.crfsuite')


# **** osm data ****
# prep the training data
train_data = parse.osmToTraining('data/osm_data_street.xml')
x_train = [addr2features(addr) for addr in train_data]
y_train = [addr2labels(addr) for addr in train_data]

# train model
trainer = pycrfsuite.Trainer(verbose=False)
for xseq, yseq in zip(x_train, y_train):
    trainer.append(xseq, yseq)
trainer.train('../usaddress/osm_usaddr.crfsuite')