import pytest
from heredity import joint_probability, update, normalize, load_data


def test_joint_probability():
    people = load_data("data/family0.csv")
    one_gene = {"Harry"}
    two_genes = {"James"}
    have_trait = {"James"}
    probability = joint_probability(people, one_gene=one_gene,
                                    two_genes=two_genes, have_trait=have_trait)
    assert probability == 0.0026643247488

    people = load_data("data/family0.csv")
    one_gene = {}
    two_genes = {}
    have_trait = {}
    probability = joint_probability(people, one_gene=one_gene,
                                    two_genes=two_genes, have_trait=have_trait)
    assert 0.8664 <= round(probability, 4) <= 0.8864


def test_update():
    people = load_data("data/family0.csv")
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    one_gene = {"Harry"}
    two_genes = {"James"}
    have_trait = {"James"}
    p = joint_probability(people, one_gene=one_gene, two_genes=two_genes, have_trait=have_trait)
    update(probabilities, one_gene, two_genes, have_trait, p)

    assert probabilities["Harry"]['gene'][1] == p
    assert probabilities["Harry"]['gene'][2] == 0
    assert probabilities["Harry"]['gene'][0] == 0
    assert probabilities["Harry"]['trait'][True] == 0
    assert probabilities["Harry"]['trait'][False] == p
    assert probabilities["James"]['gene'][1] == 0
    assert probabilities["James"]['gene'][2] == p
    assert probabilities["James"]['gene'][0] == 0
    assert probabilities["James"]['trait'][True] == p
    assert probabilities["James"]['trait'][False] == 0
    assert probabilities["Lily"]['gene'][1] == 0
    assert probabilities["Lily"]['gene'][2] == 0
    assert probabilities["Lily"]['gene'][0] == p
    assert probabilities["Lily"]['trait'][True] == 0
    assert probabilities["Lily"]['trait'][False] == p


def test_normalize():
    people = load_data("data/family0.csv")
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # case1
    one_gene = {"Harry"}
    two_genes = {"James"}
    have_trait = {"James"}
    p = joint_probability(people, one_gene=one_gene, two_genes=two_genes, have_trait=have_trait)
    update(probabilities, one_gene=one_gene, two_genes=two_genes, have_trait=have_trait, p=p)
    
    # case2
    one_gene = {"Harry"}
    two_genes = {"James"}
    have_trait = {"James, Harry"}
    p = joint_probability(people, one_gene=one_gene, two_genes=two_genes, have_trait=have_trait)
    update(probabilities, one_gene=one_gene, two_genes=two_genes, have_trait=have_trait, p=p)

    normalize(probabilities)

    print("\n", probabilities)

    assert sum(probabilities["Harry"]["gene"].values()) == pytest.approx(1.0)
    assert sum(probabilities["Harry"]["trait"].values()) == pytest.approx(1.0)
    assert sum(probabilities["James"]["gene"].values()) == pytest.approx(1.0)
    assert sum(probabilities["James"]["trait"].values()) == pytest.approx(1.0)
    assert sum(probabilities["Lily"]["gene"].values()) == pytest.approx(1.0)
    assert sum(probabilities["Lily"]["trait"].values()) == pytest.approx(1.0)


if __name__ == "__main__":
    pytest.main()
