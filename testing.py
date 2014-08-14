from training import parse, training
import random
import pycrfsuite
import re


def evaluateParser(train_data, test_data, modelname):
    #prep data
    x_train = [training.addr2features(addr) for addr in train_data]
    y_train = [training.addr2labels(addr) for addr in train_data]

    #train model
    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(x_train, y_train):
        trainer.append(xseq, yseq)
    modelfile = "training/models/"+re.sub(r'/W', '_', modelname)+".crfsuite"
    trainer.train(modelfile)

    #predictions
    tagger = pycrfsuite.Tagger()
    tagger.open(modelfile)
    total_addr_count = len(test_data)
    correct_count = 0
    incorrect_predictions = []
    for addr in test_data:
        address = training.addr2tokens(addr)
        labels_pred = tagger.tag(training.addr2features(addr))
        labels_true = training.addr2labels(addr)
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
#parse.osmSyntheticToTraining('data/osm_data.xml')
synthetictrainfile = 'training_data/synthetic_data_osm_cleaned.xml'
data = parse.parseTrainingData(synthetictrainfile)
random.shuffle(data)
train_data = data[0:5000]
test_data = data[5000:20000]
evaluateParser(train_data, test_data, "testing")
