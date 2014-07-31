import os
import pycrfsuite

TAGGER = pycrfsuite.Tagger()
TAGGER.open(os.path.split(os.path.abspath(__file__))[0] 
            + '/usaddr.crfsuite')

def parse(address_string) :
    tokens = address_string.split()
    tags = TAGGER.tag(address_string.split())
    return zip(tokens, tags)

