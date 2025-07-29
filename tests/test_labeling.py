import pytest
from parserator.training import readTrainingData

from usaddress import GROUP_LABEL, parse


# these are simple address patterns
@pytest.mark.parametrize(
    "address_text,components",
    readTrainingData(
        ["measure_performance/test_data/simple_address_patterns.xml"], GROUP_LABEL
    ),
)
def test_simple_addresses(address_text, components):

    _, labels_true = list(zip(*components))
    _, labels_pred = list(zip(*parse(address_text)))
    assert labels_pred == labels_true


# for making sure that performance isn't degrading
# from now on, labeled examples of new address formats
# should go both in training data & test data
# these are simple address patterns
@pytest.mark.parametrize(
    "address_text,components",
    readTrainingData(["measure_performance/test_data/labeled.xml"], GROUP_LABEL),
)
def test_all(address_text, components):

    _, labels_true = list(zip(*components))
    _, labels_pred = list(zip(*parse(address_text)))
    assert labels_pred == labels_true


@pytest.mark.parametrize(
    "address_text,components",
    readTrainingData(
        ["measure_performance/test_data/synthetic_osm_data.xml"], GROUP_LABEL
    ),
)
def test_synthetic_addresses(address_text, components):

    _, labels_true = list(zip(*components))
    _, labels_pred = list(zip(*parse(address_text)))
    assert labels_pred == labels_true


@pytest.mark.parametrize(
    "address_text,components",
    readTrainingData(
        ["measure_performance/test_data/us50_test_tagged.xml"], GROUP_LABEL
    ),
)
def test_us50(address_text, components):

    _, labels_true = list(zip(*components))
    _, labels_pred = list(zip(*parse(address_text)))
    fuzzyEquals(labels_pred, labels_true)


def fuzzyEquals(labels_pred, labels_true):
    labels = []
    fuzzy_labels = []
    for label in labels_pred:
        if label.startswith("StreetName"):
            fuzzy_labels.append("StreetName")
        elif label.startswith("AddressNumber"):
            fuzzy_labels.append("AddressNumber")
        elif label == ("Null"):
            fuzzy_labels.append("NotAddress")
        else:
            fuzzy_labels.append(label)
    for label in labels_true:
        labels.append(label)

    assert fuzzy_labels == labels
