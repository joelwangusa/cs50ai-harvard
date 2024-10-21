import pytest
from traffic import load_data, get_model


def test_load_data():
    data_dir = "gtsrb-small"
    images, labels = load_data(data_dir, testing=True)
    assert len(images) == len(labels)
    for image in images[:10]:
        height, width, channels = image.shape
        assert height == 30
        assert width == 30
        assert channels == 3


if __name__ == "__main__":
    pytest.main()