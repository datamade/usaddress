import pycrfsuite
import re
import string
import parse


def tokenFeatures(token) :

    features = {'token.lower' : token.lower(), 
                #'token.isupper' : token.isupper(), 
                #'token.islower' : token.islower(), 
                #'token.istitle' : token.istitle(), 
                'token.isdigit' : token.isdigit(),
                #'digit.length' : token.isdigit() * len(token),
                #'token.ispunctuation' : (token in string.punctuation),
                #'token.length' : len(token),
                #'ends_in_comma' : token[-1] == ','
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


def evaluateParser(train_data, test_data, modelname):
    #prep data
    x_train = [addr2features(addr) for addr in train_data]
    y_train = [addr2labels(addr) for addr in train_data]

    #train model
    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(x_train, y_train):
        trainer.append(xseq, yseq)
    modelfile = "models/"+re.sub(r'/W', '_', modelname)+".crfsuite"
    trainer.train(modelfile)

    #predictions
    tagger = pycrfsuite.Tagger()
    tagger.open(modelfile)
    total_addr_count = len(test_data)
    correct_count = 0
    incorrect_predictions = []
    for addr in test_data:
        address = addr2tokens(addr)
        labels_pred = tagger.tag(addr2features(addr))
        labels_true = addr2labels(addr)
        if labels_pred == labels_true:
            correct_count += 1
        else:
            incorrect = { "addr": address, "pred": labels_pred, "true": labels_true}
            incorrect_predictions.append(incorrect)
    print correct_count, "out of", total_addr_count, "addresses correctly labeled"
    print float(correct_count)/float(total_addr_count)*100, "%"
    for incorrect_prediction in incorrect_predictions:
        address = incorrect_prediction["addr"]
        print "\nADDRESS:   ", ' '.join(address)
        for i in range(len(address)):
            if incorrect_prediction["pred"][i] != incorrect_prediction["true"][i]:
                print address[i], "was labeled as", incorrect_prediction["pred"][i], "instead of", incorrect_prediction["true"][i]



# **** osm synthetic data ****
#parse.osmSyntheticToTraining('data/osm_data_street.xml')
synthetictrainfile = '../training_data/synthetic_data_osm_data_street_xml.xml'
data = parse.parseTrainingData(synthetictrainfile)
train_data = data[0:20]
test_data = data[20:40]
evaluateParser(train_data, test_data, "testing")
