import sys
from sklearn.metrics import f1_score
from sklearn.base import BaseEstimator
from sklearn.grid_search import GridSearchCV
from training import get_data_sklearn_format
import pycrfsuite
import usaddress

def my_f1_score(estimator, X, y):
    predicted = estimator.predict(X)
    flat_pred, flat_gold = [], []
    for a, b in zip(predicted, y):
        if len(a) == len(b):
            flat_pred.extend(a)
            flat_gold.extend(b)
    return f1_score(flat_gold, flat_pred)

class AddressEstimator(BaseEstimator):
    model_path = 'usaddress/usaddr.crfsuite'

    def __init__(self, c1=1, c2=1):
        self.c1 = c1
        self.c2 = c2

    def fit(self, X, y, **params):
        trainer = pycrfsuite.Trainer(verbose=False)
        for address, labels in zip(X, y):
            tokens = usaddress.tokenize(address)
            if len(tokens) != len(labels):
                # sometimes there are more/less gold standard labels than
                # the number of tags the system will output, This is because
                # our tokenizer works differently to how the data is tokenized.
                # Let's pretend this never happened
                continue
            trainer.append(usaddress.addr2features(tokens), labels)
        trainer.train(self.model_path)
        reload(usaddress)

    def predict(self, X):
        reload(usaddress)  # tagger object is defined at the module level, update now
        predictions = []
        for address in X:
            predictions.append([foo[1] for foo in usaddress.parse(address)])
        return predictions




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

    cv = GridSearchCV(AddressEstimator(), {'c1': [0.1, 1, 10], 'c2': [1]}, scoring=my_f1_score)
    X, y = get_data_sklearn_format()
    cv.fit(X, y)
    print(cv.best_params_)