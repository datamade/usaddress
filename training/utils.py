import random
import sys
from sklearn.cross_validation import KFold
from sklearn.metrics import f1_score, classification_report
from sklearn.base import BaseEstimator
from sklearn.grid_search import GridSearchCV
from training import trainModel, get_data_sklearn_format
import pycrfsuite
from operator import itemgetter
import usaddress


class AddressEstimator(BaseEstimator):
    model_path = 'usaddress/usaddr.crfsuite'

    def __init__(self, c1=1, c2=1):
        self.c1 = c1
        self.c2 = c2

    def fit(self, X, y, **params):
        trainer = pycrfsuite.Trainer(verbose=False)
        for address, labels in zip(X, y):
            tokens = usaddress.tokenize(address)
            if len(tokens) != labels:
                # sometimes there are more/less gold standard labels than
                # the number of tags the system will output, This is because
                # our tokenizer works differently to how the data is tokenized.
                # Let's pretend this never happened
                # print 'WARNING: data tokenized incorrectly'
                continue
            trainer.append(usaddress.addr2features(tokens), labels)
        trainer.train(self.model_path)
        reload(usaddress)
        print(usaddress.parse('12 Awesome blvd'))

    def predict(self, X):
        reload(usaddress)
        print(usaddress.parse('12 Awesome blvd'))
        # reload(usaddress)  # tagger object is defined at the module level, update now
        return [usaddress.parse(x) for x in X]

# def mean_scores_over_crossvalidation(n=5, params_to_set=dict()):
# data = get_all_data()
#     scores = []
#
#     cv = KFold(len(data), n)
#     for i, (train, test) in enumerate(cv):
#         print 'Doing fold %d' % i
#         trainModel(itemgetter(*train)(data), model_path)
#         reload(usaddress)  # tagger object is defined at the module level, update now
#
#         y_true = []
#         y_pred = []
#         for address_text, components in itemgetter(*test)(data):
#             tokens, labels = zip(*components)
#             if len(labels) != len(usaddress.tokenize(address_text)):
#                 # sometimes there are more/less gold standard labels than
#                 # the number of tags the system will output, This is because
#                 # our tokenizer works differently to how the data is tokenized.
#                 # Let's pretend this never happened
#                 # print 'WARNING: data tokenized incorrectly'
#                 continue
#             predictions = usaddress.parse(address_text)
#             y_pred.extend(x[1] for x in predictions)
#             y_true.extend(labels)
#             assert len(y_pred) == len(y_true)
#
#         # print classification_report(y_true, y_pred)
#         score = f1_score(y_true, y_pred)
#         print 'F1 score', score
#         scores.append(score)
#     return sum(scores) / len(scores)


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
    # mean_scores_over_crossvalidation(5, {'feature.minfreq': 1000, 'c2': .10})

    cv = GridSearchCV(AddressEstimator(), {'c1': [0.1, 1, 10], 'c2': [1]}, scoring='f1')
    X, y = get_data_sklearn_format()
    cv.fit(X, y)
    print(cv.best_params_)