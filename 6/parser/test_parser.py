import pytest
from parser import preprocess, np_chunk, parser


def test_preprocess():
    sentence = "Holmes, about to, o'clock with-in sat"
    content = preprocess(sentence)
    
    assert all(isinstance(word, str) for word in content)


def test_main():
    sentence = "Holmes sat in the red armchair."
    s = preprocess(sentence)
    try:
        trees = list(parser.parse(s))
        # Print each tree with noun phrase chunks
        for tree in trees:
            tree.pretty_print()
        assert len(trees) > 0
    except ValueError as e:
        print(e)
        return

    sentence = "Holmes sat in the little red armchair."
    s = preprocess(sentence)
    try:
        trees = list(parser.parse(s))
        # Print each tree with noun phrase chunks
        for tree in trees:
            tree.pretty_print()
        assert len(trees) > 0
    except ValueError as e:
        print(e)
        return
    
    sentence = "Holmes sat in the the armchair."
    s = preprocess(sentence)
    try:
        trees = list(parser.parse(s))
        # Print each tree with noun phrase chunks
        for tree in trees:
            tree.pretty_print()
        assert len(trees) == 0
    except ValueError as e:
        print(e)
        return


def test_np_chunk():
    sentence = "Holmes sat in the little red armchair."
    s = preprocess(sentence)
    try:
        trees = list(parser.parse(s))
        # Print each tree with noun phrase chunks
        for tree in trees:
            tree.pretty_print()
            print("Noun Phrase Chunks")
            chunks = np_chunk(tree)
            for np in chunks:
                print(" ".join(np.flatten()))
            assert isinstance(chunks, list)
    except ValueError as e:
        print(e)
        return
    

if __name__ == "__main__":
    pytest.main()