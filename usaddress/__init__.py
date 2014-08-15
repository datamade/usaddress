import os
import string
import pycrfsuite
import re

NULL_TAG = 'Null'

TAGGER = pycrfsuite.Tagger()
TAGGER.open(os.path.split(os.path.abspath(__file__))[0] 
            + '/usaddr.crfsuite')

def parse(address_string) :
    tokens = re.findall(r"\w+|[^\w\s]", address_string, re.UNICODE)
    features = addr2features(tokens)

    tags = TAGGER.tag(features)
    return zip(tokens, tags)

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

def addr2features(address):
    feature_sequence = []
    
    address = address[:]

    previous_feature = tokenFeatures(address.pop(0))
    previous_feature['address.start'] = True

    feature_sequence.append(previous_feature)

    for token in address :
        next_feature = tokenFeatures(token)
        for key, value in next_feature.items() :
            feature_sequence[-1]['next.' + key] = value
        for key, value in previous_feature.items() :
            if key[:5] != 'next.' and key[:9] != 'previous.' :
                next_feature['previous.' + key] = value

        feature_sequence.append(next_feature)
        previous_feature = next_feature



    feature_sequence[-1]['address.end'] = True

    try :
        feature_sequence[-2]['next.address.end'] = True
    except IndexError :
        pass

    feature_sequence = [[str(each) for each in feature.items()]
                         for feature in feature_sequence]

    return feature_sequence
