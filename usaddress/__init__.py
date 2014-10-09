import os
import string
import pycrfsuite
import re
from collections import OrderedDict
import warnings

DIRECTIONS = set(['n', 's', 'e', 'w',
                  'ne', 'nw', 'se', 'sw',
                  'north', 'south', 'east', 'west', 
                  'northeast', 'northwest', 'southeast', 'southwest'])

try :
    TAGGER = pycrfsuite.Tagger()
    path = os.path.split(os.path.abspath(__file__))[0] + '/usaddr.crfsuite'
    TAGGER.open(path)
except IOError :
    warnings.warn("You must train the model (run training/training.py) and create the usaddr.crfsuite file before you can use the parse and tag methods")

def parse(address_string) :

    tokens = tokenize(address_string)

    if not tokens :
        return []

    features = addr2features(tokens)

    tags = TAGGER.tag(features)
    return zip(tokens, tags)

def tag(address_string) :
    tagged_address = OrderedDict()
    for token, label in parse(address_string) :
        tagged_address.setdefault(label, []).append(token)

    for token in tagged_address :
        component = ' '.join(tagged_address[token])
        component = component.strip(" ,;")
        tagged_address[token] = component

    return tagged_address 


def tokenize(address_string) :
    re_tokens = re.compile(r"""
    \(*\b[^\s,;#()]+[.,;)]*   # ['ab. cd,ef '] -> ['ab.', 'cd,', 'ef']
    |
    [#&]                # [^'#abc'] -> ['#']
    """,
                           re.VERBOSE | re.UNICODE)

    tokens = re_tokens.findall(address_string)

    if not tokens :
        return []

    return tokens


def tokenFeatures(token) :

    if token in (u'&', u'#') :
        token_clean = token
    else :
        token_clean = re.sub(r'(^[\W]*)|([^.\w]*$)', u'', token)
    token_abbrev = re.sub(r'[.]', u'', token_clean.lower())
    features = {'nopunc' : token_abbrev,
                'abbrev' : token_clean[-1] == u'.',
                'case' : casing(token_clean),
                'digits' : digits(token_clean),
                'length' : (u'd:' + unicode(len(token_abbrev))
                            if token_abbrev.isdigit()
                            else u'w:' + unicode(len(token_abbrev))),
                'endsinpunc' : (token[-1]
                                if bool(re.match('.+[^.\w]', token))
                                else False),
                'directional' : token_abbrev in DIRECTIONS,
                'has.vowels'  : bool(set(token_abbrev[1:]) & set('aeiou')),
                }

    return features

def addr2features(address):
    
    feature_sequence = [tokenFeatures(address[0])]
    previous_features = feature_sequence[-1].copy()

    for token in address[1:] :
        token_features = tokenFeatures(token) 
        current_features = token_features.copy()

        feature_sequence[-1]['next'] = current_features
        token_features['previous'] = previous_features
            
        feature_sequence.append(token_features)

        previous_features = current_features

    feature_sequence[0]['address.start'] = True
    feature_sequence[-1]['address.end'] = True

    if len(feature_sequence) > 1 :
        feature_sequence[1]['previous']['address.start'] = True
        feature_sequence[-2]['next']['address.end'] = True

    return feature_sequence

def casing(token) :
    if token.isupper() :
        return 'upper'
    elif token.islower() :
        return 'lower' 
    elif token.istitle() :
        return 'title'
    else :
        return 'other'

def digits(token) :
    if token.isdigit() :
        return 'all_digits' 
    elif set(token) & set(string.digits) :
        return 'some_digits' 
    else :
        return 'no_digits'
                                    

