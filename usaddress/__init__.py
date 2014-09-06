import os
import string
import pycrfsuite
import re

TAGGER = pycrfsuite.Tagger()
TAGGER.open(os.path.split(os.path.abspath(__file__))[0] 
            + '/usaddr.crfsuite')

def tokenize(address_string) :
    re_tokens = re.compile(r"""
    \b[^\s,;#]+[.,;]*   # ['ab. cd,ef '] -> ['ab.', 'cd,', 'ef']
    |
    [#&]                # [^'#abc'] -> ['#']
    """,
                           re.VERBOSE | re.UNICODE)

    tokens = re_tokens.findall(address_string)

    if not tokens :
        return []

    return tokens

def parse(address_string) :

    tokens = tokenize(address_string)

    if not tokens :
        return []

    features = addr2features(tokens)

    tags = TAGGER.tag(features)
    return zip(tokens, tags)

def tokenFeatures(token) :

    token_clean = re.sub(r'(^[\W]*)|([\s,;]$)', u'', token)
    token_abbrev = re.sub(r'[.]', u'', token_clean.lower())
    features = {'lower' : token_clean.lower(), 
                'nopunc' : token_abbrev,
                'isupper' : token_clean.isupper(),
                'islower' : token_clean.islower(), 
                'istitle' : token_clean.istitle(), 
                'isalldigits' : token_clean.isdigit(),
                'split_digit' :  bool(re.match(r'\d+[\W\S]+\d+', 
                                               token_clean)),
                'digit.length' : unicode(len(token_clean)
                                         if token_clean.isdigit() 
                                         else False),
                'endsinpunc' : token[-1] in string.punctuation,
                'end.delim' : token[-1] in (u',', u';'),
                'wordl.length' : unicode(len(token_clean)
                                         if not token_clean.isdigit()
                                         else False),
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
