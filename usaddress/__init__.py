import os
import string
import pycrfsuite
import re

TAGGER = pycrfsuite.Tagger()
TAGGER.open(os.path.split(os.path.abspath(__file__))[0] 
            + '/usaddr.crfsuite')

def parse(address_string) :

    re_tokens = re.compile(r"""
    \b\w[^\s]*(?=\b)\.*   # 'F-H. ' -> ['F-H.']
    |
    [^\w\s](?=\s)       # [', ']  -> [',']
    |
    (?<=\s)[^\w\s]      # ['#f ']  -> ['#']
    """,
                           re.VERBOSE | re.UNICODE)

    tokens = re_tokens.findall(address_string)

    if not tokens :
        return []

    features = addr2features(tokens)

    tags = TAGGER.tag(features)
    return zip(tokens, tags)

def tokenFeatures(token) :

    features = {'token.lower' : token.lower(), 
                'token.isupper' : token.isupper(), 
                'token.islower' : token.islower(), 
                'token.istitle' : token.istitle(), 
                'token.isalldigits' : token.isdigit(),
                'token.hasadigit' : any(char.isdigit() for char in token),
                'token.isstartdigit' : token[0].isdigit(),
                'digit.length' : token.isdigit() * len(token),
                'token.ispunctuation' : (token in string.punctuation),
                'token.length' : len(token),
                #'token.isdirection' : (token.lower in ['north', 'east', 'south', 'west', 'n', 'e', 's', 'w'])
                }

    return features

def addr2features(address):
    
    previous_feature = tokenFeatures(address[0])
    feature_sequence = [previous_feature]

    for token in address[1:] :
        next_feature = tokenFeatures(token)

        for key, value in next_feature.items() :
            feature_sequence[-1][('next', key)] = value

        feature_sequence.append(next_feature.copy())

        for key, value in previous_feature.items() :
            feature_sequence[-1][('previous', key)] = value

        previous_feature = next_feature

    feature_sequence[0]['address.start'] = True
    feature_sequence[-1]['address.end'] = True

    if len(feature_sequence) > 1 :
        feature_sequence[1][('previous', 'address.start')] = True
        feature_sequence[-2][('next', 'address.end')] = True

    feature_sequence = [[str(each) for each in feature.items()]
                         for feature in feature_sequence]

    return feature_sequence
