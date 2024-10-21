import pytest
from pagerank import transition_model, sample_pagerank, iterate_pagerank, crawl

DAMPING = 0.85


def test_transition_model():
    corpus = crawl("corpus0")
    page = "1.html"
    result = transition_model(corpus=corpus, page=page, damping_factor=DAMPING)
    assert len(result) == len(corpus)
    assert sum(result.values()) == 1


def test_sample_pagerank():
    corpus = crawl("corpus1")
    pagerank = sample_pagerank(corpus=corpus, damping_factor=DAMPING, n=10000)
    print(pagerank)
    assert len(pagerank) == len(corpus)
    assert sum(pagerank.values()) == 1


def test_iterate_pagerank():
    # Data set Corpus0
    corpus = crawl("corpus0")
    pagerank = iterate_pagerank(corpus, damping_factor=DAMPING)
    print(pagerank)
    assert len(pagerank) == len(corpus)
    assert sum(pagerank.values()) == 1

    # Data set Corpus1
    corpus = crawl("corpus1")
    pagerank = iterate_pagerank(corpus, damping_factor=DAMPING)
    print(pagerank)
    assert len(pagerank) == len(corpus)
    assert sum(pagerank.values()) == 1

    # Data set corpus2
    corpus = crawl("corpus2")
    pagerank = iterate_pagerank(corpus, damping_factor=DAMPING)
    print(pagerank)
    assert len(pagerank) == len(corpus)
    assert sum(pagerank.values()) == 1


if __name__ == "__main__":
    pytest.main()
