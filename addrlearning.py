import pycrfsuite
import re
import string

def parseLines(lines):
    parsed = [[]]
    addr_index = 0
    token_index = 0
    tag_list = [None, 'street number', 'pobox', 'street', None,
                'city', 'state', 'zip']
    
    for line in lines:
        if line == '\n':
            addr_index += 1
            token_index = 0
            parsed.append([])
        else:
            split = line.split(' |')
            token_string = split[0]
            token_num = split[1].rstrip()
            token_num = int(token_num)
            token_tag = tag_list[token_num]
            words = re.findall(r"[\w]+|[^\s\w]", token_string)
            for word in words:
                parsed[addr_index].append((word, token_tag))

    return parsed

def word2features(address, i):
    word = address[i][0]
    if i == 0:
        wordprevious = ''
    else:
        wordprevious = address[i-1][0]
    if i +1 == len(address):
        wordnext= ''
    else:
        wordnext = address[i+1][0]
    features = ['word.lower=' + word.lower(), 
                'word.isdigit=%s' % word.isdigit(),
                'word.ispunctuation=%s' % (word in string.punctuation),
                'word.previous=' + wordprevious,
                'word.next=' + wordnext
                ]
    return features

def addr2features(address):
    return [word2features(address, i) for i in range(len(address))]

def addr2labels(address):
    return [address[i][1] for i in range(len(address))]

def addr2tokens(address):
    return [address[i][0] for i in range(len(address))]


# prep the training & test data
with open('./training_data/us50.train.tagged', 'r') as train_file :
    train_data = parseLines(train_file)

x_train = [addr2features(addr) for addr in train_data]
y_train = [addr2labels(addr) for addr in train_data]

with open('./training_data/us50.test.tagged', 'r') as test_file :
    test_data = parseLines(test_file)

x_test = [addr2features(addr) for addr in test_data]
y_test = [addr2labels(addr) for addr in test_data]


#train model
trainer = pycrfsuite.Trainer(verbose=False)

for xseq, yseq in zip(x_train, y_train):
    trainer.append(xseq, yseq)

trainer.train('usaddr.crfsuite')

#predictions
tagger = pycrfsuite.Tagger()
tagger.open('usaddr.crfsuite')

#see predictions of example addresses against correct labels
example_addrs = test_data[0:10]
for example in example_addrs:
    print "ADDRESS:   ", ' '.join(addr2tokens(example))
    print "PREDICTED: ", ' '.join(tagger.tag(addr2features(example)))
    print "CORRECT:   ", ' '.join(addr2labels(example)), '\n'


print train_data[0]
print "***"
print x_train[0]



