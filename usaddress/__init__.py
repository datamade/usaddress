#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from builtins import zip
from builtins import str
import os
import string
import re
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import warnings

import pycrfsuite
import probableparsing

# The address components are based upon the `United States Thoroughfare,
# Landmark, and Postal Address Data Standard
# http://www.urisa.org/advocacy/united-states-thoroughfare-landmark-and-postal-address-data-standard

LABELS = [
    'AddressNumberPrefix',
    'AddressNumber',
    'AddressNumberSuffix',
    'StreetNamePreModifier',
    'StreetNamePreDirectional',
    'StreetNamePreType',
    'StreetName',
    'StreetNamePostType',
    'StreetNamePostDirectional',
    'SubaddressType',
    'SubaddressIdentifier',
    'BuildingName',
    'OccupancyType',
    'OccupancyIdentifier',
    'CornerOf',
    'LandmarkName',
    'PlaceName',
    'StateName',
    'ZipCode',
    'USPSBoxType',
    'USPSBoxID',
    'USPSBoxGroupType',
    'USPSBoxGroupID',
    'IntersectionSeparator',
    'Recipient',
    'NotAddress',
]

PARENT_LABEL = 'AddressString'
GROUP_LABEL = 'AddressCollection'

MODEL_FILE = 'usaddr.crfsuite'
MODEL_PATH = os.path.split(os.path.abspath(__file__))[0] + '/' + MODEL_FILE

DIRECTIONS = set(['n', 's', 'e', 'w',
                  'ne', 'nw', 'se', 'sw',
                  'north', 'south', 'east', 'west',
                  'northeast', 'northwest', 'southeast', 'southwest'])

STREET_NAMES = {
    'allee', 'alley', 'ally', 'aly', 'anex', 'annex', 'annx', 'anx', 'arc',
    'arcade', 'av', 'ave', 'aven', 'avenu', 'avenue', 'avn', 'avnue', 'bayoo',
    'bayou', 'bch', 'beach', 'bend', 'bg', 'bgs', 'blf', 'blfs', 'bluf',
    'bluff', 'bluffs', 'blvd', 'bnd', 'bot', 'bottm', 'bottom', 'boul',
    'boulevard', 'boulv', 'br', 'branch', 'brdge', 'brg', 'bridge', 'brk',
    'brks', 'brnch', 'brook', 'brooks', 'btm', 'burg', 'burgs', 'byp', 'bypa',
    'bypas', 'bypass', 'byps', 'byu', 'camp', 'canyn', 'canyon', 'cape',
    'causeway', 'causwa', 'cen', 'cent', 'center', 'centers', 'centr',
    'centre', 'cir', 'circ', 'circl', 'circle', 'circles', 'cirs', 'clb',
    'clf', 'clfs', 'cliff', 'cliffs', 'club', 'cmn', 'cmns', 'cmp', 'cnter',
    'cntr', 'cnyn', 'common', 'commons', 'cor', 'corner', 'corners', 'cors',
    'course', 'court', 'courts', 'cove', 'coves', 'cp', 'cpe', 'crcl', 'crcle',
    'creek', 'cres', 'crescent', 'crest', 'crk', 'crossing', 'crossroad',
    'crossroads', 'crse', 'crsent', 'crsnt', 'crssng', 'crst', 'cswy', 'ct',
    'ctr', 'ctrs', 'cts', 'curv', 'curve', 'cv', 'cvs', 'cyn', 'dale', 'dam',
    'div', 'divide', 'dl', 'dm', 'dr', 'driv', 'drive', 'drives', 'drs', 'drv',
    'dv', 'dvd', 'est', 'estate', 'estates', 'ests', 'exp', 'expr', 'express',
    'expressway', 'expw', 'expy', 'ext', 'extension', 'extensions', 'extn',
    'extnsn', 'exts', 'fall', 'falls', 'ferry', 'field', 'fields', 'flat',
    'flats', 'fld', 'flds', 'fls', 'flt', 'flts', 'ford', 'fords', 'forest',
    'forests', 'forg', 'forge', 'forges', 'fork', 'forks', 'fort', 'frd',
    'frds', 'freeway', 'freewy', 'frg', 'frgs', 'frk', 'frks', 'frry', 'frst',
    'frt', 'frway', 'frwy', 'fry', 'ft', 'fwy', 'garden', 'gardens', 'gardn',
    'gateway', 'gatewy', 'gatway', 'gdn', 'gdns', 'glen', 'glens', 'gln',
    'glns', 'grden', 'grdn', 'grdns', 'green', 'greens', 'grn', 'grns', 'grov',
    'grove', 'groves', 'grv', 'grvs', 'gtway', 'gtwy', 'harb', 'harbor',
    'harbors', 'harbr', 'haven', 'hbr', 'hbrs', 'heights', 'highway', 'highwy',
    'hill', 'hills', 'hiway', 'hiwy', 'hl', 'hllw', 'hls', 'hollow', 'hollows',
    'holw', 'holws', 'hrbor', 'ht', 'hts', 'hvn', 'hway', 'hwy', 'inlet',
    'inlt', 'is', 'island', 'islands', 'isle', 'isles', 'islnd', 'islnds',
    'iss', 'jct', 'jction', 'jctn', 'jctns', 'jcts', 'junction', 'junctions',
    'junctn', 'juncton', 'key', 'keys', 'knl', 'knls', 'knol', 'knoll',
    'knolls', 'ky', 'kys', 'lake', 'lakes', 'land', 'landing', 'lane', 'lck',
    'lcks', 'ldg', 'ldge', 'lf', 'lgt', 'lgts', 'light', 'lights', 'lk', 'lks',
    'ln', 'lndg', 'lndng', 'loaf', 'lock', 'locks', 'lodg', 'lodge', 'loop',
    'loops', 'mall', 'manor', 'manors', 'mdw', 'mdws', 'meadow', 'meadows',
    'medows', 'mews', 'mill', 'mills', 'mission', 'missn', 'ml', 'mls', 'mnr',
    'mnrs', 'mnt', 'mntain', 'mntn', 'mntns', 'motorway', 'mount', 'mountain',
    'mountains', 'mountin', 'msn', 'mssn', 'mt', 'mtin', 'mtn', 'mtns', 'mtwy',
    'nck', 'neck', 'opas', 'orch', 'orchard', 'orchrd', 'oval', 'overpass',
    'ovl', 'park', 'parks', 'parkway', 'parkways', 'parkwy', 'pass', 'passage',
    'path', 'paths', 'pike', 'pikes', 'pine', 'pines', 'pkway', 'pkwy',
    'pkwys', 'pky', 'pl', 'place', 'plain', 'plains', 'plaza', 'pln', 'plns',
    'plz', 'plza', 'pne', 'pnes', 'point', 'points', 'port', 'ports', 'pr',
    'prairie', 'prk', 'prr', 'prt', 'prts', 'psge', 'pt', 'pts', 'rad',
    'radial', 'radiel', 'radl', 'ramp', 'ranch', 'ranches', 'rapid', 'rapids',
    'rd', 'rdg', 'rdge', 'rdgs', 'rds', 'rest', 'ridge', 'ridges', 'riv',
    'river', 'rivr', 'rnch', 'rnchs', 'road', 'roads', 'route', 'row', 'rpd',
    'rpds', 'rst', 'rte', 'rue', 'run', 'rvr', 'shl', 'shls', 'shoal',
    'shoals', 'shoar', 'shoars', 'shore', 'shores', 'shr', 'shrs', 'skwy',
    'skyway', 'smt', 'spg', 'spgs', 'spng', 'spngs', 'spring', 'springs',
    'sprng', 'sprngs', 'spur', 'spurs', 'sq', 'sqr', 'sqre', 'sqrs', 'sqs',
    'squ', 'square', 'squares', 'st', 'sta', 'station', 'statn', 'stn', 'str',
    'stra', 'strav', 'straven', 'stravenue', 'stravn', 'stream', 'street',
    'streets', 'streme', 'strm', 'strt', 'strvn', 'strvnue', 'sts', 'sumit',
    'sumitt', 'summit', 'ter', 'terr', 'terrace', 'throughway', 'tpke',
    'trace', 'traces', 'track', 'tracks', 'trafficway', 'trail', 'trailer',
    'trails', 'trak', 'trce', 'trfy', 'trk', 'trks', 'trl', 'trlr', 'trlrs',
    'trls', 'trnpk', 'trwy', 'tunel', 'tunl', 'tunls', 'tunnel', 'tunnels',
    'tunnl', 'turnpike', 'turnpk', 'un', 'underpass', 'union', 'unions', 'uns',
    'upas', 'valley', 'valleys', 'vally', 'vdct', 'via', 'viadct', 'viaduct',
    'view', 'views', 'vill', 'villag', 'village', 'villages', 'ville', 'villg',
    'villiage', 'vis', 'vist', 'vista', 'vl', 'vlg', 'vlgs', 'vlly', 'vly',
    'vlys', 'vst', 'vsta', 'vw', 'vws', 'walk', 'walks', 'wall', 'way', 'ways',
    'well', 'wells', 'wl', 'wls', 'wy', 'xing', 'xrd', 'xrds',
}
try:
    TAGGER = pycrfsuite.Tagger()
    TAGGER.open(MODEL_PATH)
except IOError:
    warnings.warn('You must train the model (parserator train --trainfile '
                  'FILES) to create the %s file before you can use the parse '
                  'and tag methods' % MODEL_FILE)


def parse(address_string):
    tokens = tokenize(address_string)

    if not tokens:
        return []

    features = tokens2features(tokens)

    tags = TAGGER.tag(features)
    return list(zip(tokens, tags))


def tag(address_string, tag_mapping=None):
    tagged_address = OrderedDict()

    last_label = None
    is_intersection = False
    og_labels = []

    for token, label in parse(address_string):
        if label == 'IntersectionSeparator':
            is_intersection = True
        if 'StreetName' in label and is_intersection:
            label = 'Second' + label

        # saving old label
        og_labels.append(label)
        # map tag to a new tag if tag mapping is provided
        if tag_mapping and tag_mapping.get(label):
            label = tag_mapping.get(label)
        else:
            label = label

        if label == last_label:
            tagged_address[label].append(token)
        elif label not in tagged_address:
            tagged_address[label] = [token]
        else:
            raise RepeatedLabelError(address_string, parse(address_string),
                                     label)

        last_label = label

    for token in tagged_address:
        component = ' '.join(tagged_address[token])
        component = component.strip(" ,;")
        tagged_address[token] = component

    if 'AddressNumber' in og_labels and not is_intersection:
        address_type = 'Street Address'
    elif is_intersection and 'AddressNumber' not in og_labels:
        address_type = 'Intersection'
    elif 'USPSBoxID' in og_labels:
        address_type = 'PO Box'
    else:
        address_type = 'Ambiguous'

    return tagged_address, address_type


def tokenize(address_string):
    if isinstance(address_string, bytes):
        address_string = str(address_string, encoding='utf-8')
    address_string = re.sub('(&#38;)|(&amp;)', '&', address_string)
    re_tokens = re.compile(r"""
    \(*\b[^\s,;#&()]+[.,;)\n]*   # ['ab. cd,ef '] -> ['ab.', 'cd,', 'ef']
    |
    [#&]                       # [^'#abc'] -> ['#']
    """,
                           re.VERBOSE | re.UNICODE)

    tokens = re_tokens.findall(address_string)

    if not tokens:
        return []

    return tokens


def tokenFeatures(token):
    if token in (u'&', u'#', u'½'):
        token_clean = token
    else:
        token_clean = re.sub(r'(^[\W]*)|([^.\w]*$)', u'', token,
                             flags=re.UNICODE)

    token_abbrev = re.sub(r'[.]', u'', token_clean.lower())
    features = {
        'abbrev': token_clean[-1] == u'.',
        'digits': digits(token_clean),
        'word': (token_abbrev
                 if not token_abbrev.isdigit()
                 else False),
        'trailing.zeros': (trailingZeros(token_abbrev)
                           if token_abbrev.isdigit()
                           else False),
        'length': (u'd:' + str(len(token_abbrev))
                   if token_abbrev.isdigit()
                   else u'w:' + str(len(token_abbrev))),
        'endsinpunc': (token[-1]
                       if bool(re.match('.+[^.\w]', token, flags=re.UNICODE))
                       else False),
        'directional': token_abbrev in DIRECTIONS,
        'street_name': token_abbrev in STREET_NAMES,
        'has.vowels': bool(set(token_abbrev[1:]) & set('aeiou')),
    }

    return features


def tokens2features(address):
    feature_sequence = [tokenFeatures(address[0])]
    previous_features = feature_sequence[-1].copy()

    for token in address[1:]:
        token_features = tokenFeatures(token)
        current_features = token_features.copy()

        feature_sequence[-1]['next'] = current_features
        token_features['previous'] = previous_features

        feature_sequence.append(token_features)

        previous_features = current_features

    feature_sequence[0]['address.start'] = True
    feature_sequence[-1]['address.end'] = True

    if len(feature_sequence) > 1:
        feature_sequence[1]['previous']['address.start'] = True
        feature_sequence[-2]['next']['address.end'] = True

    return feature_sequence


def digits(token):
    if token.isdigit():
        return 'all_digits'
    elif set(token) & set(string.digits):
        return 'some_digits'
    else:
        return 'no_digits'


def trailingZeros(token):
    results = re.findall(r'(0+)$', token)
    if results:
        return results[0]
    else:
        return ''


class RepeatedLabelError(probableparsing.RepeatedLabelError):
    REPO_URL = 'https://github.com/datamade/usaddress/issues/new'
    DOCS_URL = 'https://usaddress.readthedocs.io/'
