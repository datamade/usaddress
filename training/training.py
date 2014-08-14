import pycrfsuite
import re
import string
import parse
import random


def tokenFeatures(token) :

    features = {'token.lower' : token.lower(), 
                'token.isupper' : token.isupper(), 
                #'token.islower' : token.islower(), 
                #'token.istitle' : token.istitle(), 
                'token.isdigit' : token.isdigit(),
                'token.isstartdigit' : token[0].isdigit(),
                #'digit.length' : token.isdigit() * len(token),
                'token.ispunctuation' : (token in string.punctuation),
                'token.length' : len(token),
                #'ends_in_comma' : token[-1] == ','
                'token.isdirection' : (token.lower in ['north', 'east', 'south', 'west', 'n', 'e', 's', 'w'])
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
    #return [address[i][1] for i in range(len(address))]
    labels = []
    for i in range(len(address)):
        if address[i][1]:
            labels.append(address[i][1])
        else:
            labels.append("punc")
    return labels


def addr2tokens(address):
    return [address[i][0] for i in range(len(address))]