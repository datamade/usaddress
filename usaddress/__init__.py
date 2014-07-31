import pycrfsuite
#predictions

TAGGER = pycrfsuite.Tagger()
TAGGER.open('usaddr.crfsuite')

def parse(address_string) :
    tokens = address_string.split()
    tags = TAGGER.tag(address_string.split())
    return zip(tokens, tags)

