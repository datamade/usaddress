#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from builtins import zip
from builtins import str
import os
import string
import pycrfsuite
import re
try :
    from collections import OrderedDict
except ImportError :
    from ordereddict import OrderedDict
import warnings

# The address components are based upon the `United States Thoroughfare, Landmark, and Postal Address Data Standard
# http://www.urisa.org/advocacy/united-states-thoroughfare-landmark-and-postal-address-data-standard

LABELS = [
'AddressNumber',
'StreetName',
'PlaceName',
'StateName',
'ZipCode',
'AddressNumberPrefix',
'AddressNumberSuffix',
'StreetNamePreDirectional',
'StreetNamePostDirectional',
'StreetNamePreModifier',
'StreetNamePostType',
'StreetNamePreType',
'USPSBoxType',
'USPSBoxID',
'USPSBoxGroupType',
'USPSBoxGroupID',
'LandmarkName',
'CornerOf',
'IntersectionSeparator',
'OccupancyType',
'OccupancyIdentifier',
'SubaddressIdentifier',
'SubaddressType',
'Recipient',
'BuildingName',
'NotAddress'
]

PARENT_LABEL = 'AddressString'
GROUP_LABEL = 'AddressCollection'

MODEL_FILE = 'usaddr.crfsuite'
MODEL_PATH = os.path.split(os.path.abspath(__file__))[0] + '/' + MODEL_FILE

DIRECTIONS = set(['n', 's', 'e', 'w',
                  'ne', 'nw', 'se', 'sw',
                  'north', 'south', 'east', 'west', 
                  'northeast', 'northwest', 'southeast', 'southwest'])

try :
    TAGGER = pycrfsuite.Tagger()
    TAGGER.open(MODEL_PATH)
except IOError :
    warnings.warn('You must train the model (parserator train --trainfile FILES) to create the %s file before you can use the parse and tag methods' %MODEL_FILE)

def parse(address_string) :

    tokens = tokenize(address_string)

    if not tokens :
        return []

    features = tokens2features(tokens)

    tags = TAGGER.tag(features)
    return list(zip(tokens, tags))

def tag(address_string) :
    tagged_address = OrderedDict()

    last_label = None
    intersection = False

    for token, label in parse(address_string) :
        if label == 'IntersectionSeparator' :
            intersection = True
        if 'StreetName' in label and intersection :
            label = 'Second' + label 
        if label == last_label :
            tagged_address[label].append(token)
        elif label not in tagged_address :
            tagged_address[label] = [token]
        else :
            raise RepeatedLabelError(address_string, parse(address_string), label)
            
        last_label = label

    for token in tagged_address :
        component = ' '.join(tagged_address[token])
        component = component.strip(" ,;")
        tagged_address[token] = component


    if 'AddressNumber' in tagged_address and not intersection :
        address_type = 'Street Address'
    elif intersection and 'AddressNumber' not in tagged_address :
        address_type = 'Intersection'
    elif 'USPSBoxID' in tagged_address :
        address_type = 'PO Box'
    else :
        address_type = 'Ambiguous'

    return (tagged_address, address_type)

def tokenize(address_string) :
    if isinstance(address_string, bytes):
        address_string = str(address_string, encoding='utf-8')
    address_string = re.sub('(&#38;)|(&amp;)', '&', address_string)
    re_tokens = re.compile(r"""
    \(*\b[^\s,;#&()]+[.,;)]*   # ['ab. cd,ef '] -> ['ab.', 'cd,', 'ef']
    |
    [#&]                       # [^'#abc'] -> ['#']
    """,
                           re.VERBOSE | re.UNICODE)

    tokens = re_tokens.findall(address_string)

    if not tokens :
        return []

    return tokens

def tokenFeatures(token) :

    if token in (u'&', u'#', u'½') :
        token_clean = token
    else :
        token_clean = re.sub(r'(^[\W]*)|([^.\w]*$)', u'', token)
    token_abbrev = re.sub(r'[.]', u'', token_clean.lower())
    features = {'nopunc' : token_abbrev,
                'abbrev' : token_clean[-1] == u'.',
                'digits' : digits(token_clean),
                'length' : (u'd:' + str(len(token_abbrev))
                            if token_abbrev.isdigit()
                            else u'w:' + str(len(token_abbrev))),
                'endsinpunc' : (token[-1]
                                if bool(re.match('.+[^.\w]', token))
                                else False),
                'directional' : token_abbrev in DIRECTIONS,
                'has.vowels'  : bool(set(token_abbrev[1:]) & set('aeiou')),
                }

    return features

def tokens2features(address):
    
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

def digits(token) :
    if token.isdigit() :
        return 'all_digits' 
    elif set(token) & set(string.digits) :
        return 'some_digits' 
    else :
        return 'no_digits'
                                    

class RepeatedLabelError(Exception) :
    def __init__(self, original_string, parsed_string, repeated_label) :

        message ='''

ERROR: Unable to tag this string because more than one area of the string has the same label

ORIGINAL STRING:  %s
PARSED TOKENS:    %s
UNCERTAIN LABEL:  %s

When this error is raised, it's likely that either (1) the string is not a valid address or (2) some tokens were labeled incorrectly

To report an error in labeling a valid address, open an issue at https://github.com/datamade/usaddress/issues/new - it'll help us continue to improve usaddress!

For more information, see the documentation at http://usaddress.readthedocs.org/
        '''%(original_string, parsed_string, repeated_label)

        super(RepeatedLabelError, self).__init__(message)

        self.original_string = original_string
        self.parsed_string = parsed_string


