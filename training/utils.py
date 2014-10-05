import random
import sys
from sklearn.cross_validation import KFold
from sklearn.metrics import f1_score, classification_report
from training import parseTrainingData, trainModel
from operator import itemgetter
import usaddress


def mean_scores_over_crossvalidation(n=5, params_to_set=dict()):
    model_path = 'usaddress/usaddr.crfsuite'
    data = list(parseTrainingData('training/training_data/labeled.xml'))
    random.shuffle(data)
    scores = []

    cv = KFold(len(data), n)
    for i, (train, test) in enumerate(cv):
        print 'Doing fold %d' % i
        trainModel(itemgetter(*train)(data), model_path)
        usaddress.load_tagger(model_path)

        y_true = []
        y_pred = []
        for address_text, components in itemgetter(*test)(data):
            tokens, labels = zip(*components)
            if len(labels) != len(usaddress.tokenize(address_text)):
                # sometimes there are more/less gold standard labels than
                # the number of tags the system will output, This is because
                # our tokenizer works differently to how the data is tokenized.
                # Let's pretend this never happened
                # print 'WARNING: data tokenized incorrectly'
                continue
            predictions = usaddress.tag(address_text)

            for pred_labels, pred_tokens in predictions.items():
                for _ in usaddress.tokenize(pred_tokens):
                    y_pred.append(pred_labels)
            y_true.extend(list(labels))
            assert len(y_pred) == len(y_true)

        # print classification_report(y_true, y_pred)
        score = f1_score(y_true, y_pred)
        print 'F1 score', score
        scores.append(score)
    return sum(scores) / len(scores)


if __name__ == '__main__':
    # refer to http://www.chokkan.org/software/crfsuite/manual.html
    # for description of parameters
    params = {'feature.minfreq': 0,
              'feature.possible_states': False,
              'feature.possible_transitions': False,
              'c1': 0,
              'c2': 1.0,
              'max_iterations': sys.maxint,
              'num_memories': 6,
              'epsilon': 1e-5,
              'period': 10,
              'delta': 1e-5,
              'linesearch': 'MoreThuente',
              'max_linesearch': 20
    }

    # todo wrap in a sklearn estimator so we can use a GridSearchCV
    mean_scores_over_crossvalidation(5, {'feature.minfreq': 1000, 'c2': .10})