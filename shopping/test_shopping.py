import pytest
import random
from shopping import load_data, train_model, evaluate


def test_load_data():
    filename = "shopping.csv"
    evidence, labels = load_data(filename)

    assert len(evidence) == len(labels)
    one_evidence = random.choice(evidence)
    one_label = random.choice(labels)
    assert all(isinstance(e, int) or isinstance(e, float)
               for e in one_evidence)
    assert isinstance(one_label, int)
    assert len(one_evidence) == 17


if __name__ == "__main__":
    pytest.main()