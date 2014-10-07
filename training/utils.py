from __future__ import print_function
from sklearn.metrics import f1_score
from sklearn.base import BaseEstimator
from sklearn.grid_search import GridSearchCV
from training import get_data_sklearn_format
import pycrfsuite
import usaddress


def f1_with_flattening(estimator, X, y):
    """
    Calculate F1 score by flattening the predictions of the
    estimator across all addresses. For example, given the following
    addresses as input
        ['1 My str', '2 Your blvd'],
    the predictions of the model will be flattened like so:
        ['AddressNumber', 'StreetName', 'StreetNamePostType', 'AddressNumber', 'StreetName', 'StreetNamePostType']
    and compared to a similarly flattened gold standard labels. This calculates the overall
    quality of the model across all addresses as opposed to how well it does
    at any particular address.
    :param X: list of addresses to tag
    :param y: list of gold standard tuples
    """
    predicted = estimator.predict(X)
    flat_pred, flat_gold = [], []
    for a, b in zip(predicted, y):
        if len(a) == len(b):
            flat_pred.extend(a)
            flat_gold.extend(b)
    return f1_score(flat_gold, flat_pred)


class AddressEstimator(BaseEstimator):
    """
    A sklearn-compatible wrapper for a usaddress trainer
    """
    model_path = 'usaddress/usaddr.crfsuite'

    def __init__(self, c1=1, c2=1, feature_minfreq=0):
        """
        :param c1: L1 regularisation coefficient
        :param c2: L2 regularisation coefficient
        :param feature_minfreq: minimum feature frequency
        :return:
        """
        self.c1 = c1
        self.c2 = c2
        self.feature_minfreq = feature_minfreq

    def fit(self, X, y, **params):
        # sklearn requires parameters to be declared as fields of the estimator,
        # an we can't have a full stop there. Replace with an underscore
        params = {k.replace('_', '.'): v for k, v in self.__dict__.items()}
        trainer = pycrfsuite.Trainer(verbose=False, params=params)
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
    cv = GridSearchCV(AddressEstimator(), {'c1': [10 ** x for x in range(-2, 2)],
                                           'c2': [10 ** x for x in range(-2, 4)],
                                           'feature_minfreq': [0, 3, 5]},
                      scoring=f1_with_flattening, verbose=5)
    X, y = get_data_sklearn_format()
    cv.fit(X, y)
    print(cv.best_params_)
    for foo in cv.grid_scores_:
        print(foo)