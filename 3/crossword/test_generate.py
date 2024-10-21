import pytest
import random
from collections import defaultdict

from generate import CrosswordCreator, Crossword
from crossword import Variable, Crossword


def test_enforce_node_consistency():
    """
    Update `self.domains` such that each variable is node-consistent.
    (Remove any values that are inconsistent with a variable's unary
        constraints; in this case, the length of the word.)
    """
    structure = "data/structure0.txt"
    words = "data/words0.txt"
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()

    for var, words in creator.domains.items():
        assert all(len(word) == var.length for word in words) == True


def test_revise():
    """
    Make variable `x` arc consistent with variable `y`.
    To do so, remove values from `self.domains[x]` for which there is no
    possible corresponding value for `y` in `self.domains[y]`.

    Return True if a revision was made to the domain of `x`; return
    False if no revision was made.
    """
    structure = "data/structure0.txt"
    words = "data/words0.txt"
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    
    x = Variable(4, 1, "across", 4)
    y = Variable(0, 1, "across", 3)
    revised = creator.revise(x, y)
    assert revised == False

    x = Variable(0, 1, "across", 3)
    y = Variable(0, 1, "down", 5)
    revised = creator.revise(x, y)
    assert revised == True


def test_ac3():
    """
    Update `self.domains` such that each variable is arc consistent.
    If `arcs` is None, begin with initial list of all arcs in the problem.
    Otherwise, use `arcs` as the initial list of arcs to make consistent.

    Return True if arc consistency is enforced and no domains are empty;
    return False if one or more domains end up empty.
    """
    structure = "data/structure0.txt"
    words = "data/words0.txt"
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    result = creator.ac3()
    assert result == True

    result = creator.ac3([])
    assert result == True


def test_assignment_complete():
    """
    Return True if `assignment` is complete (i.e., assigns a value to each
    crossword variable); return False otherwise.
    """
    structure = "data/structure0.txt"
    words = "data/words0.txt"
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    creator.ac3()

    # Complete assignment
    assignment = defaultdict(str)
    for var, words in creator.domains.items():
        assignment[var] = random.choice(list(words))
    result = creator.assignment_complete(assignment)
    assert result == True

    # Incomplete assignment
    result = creator.assignment_complete(dict())
    assert result == False


def test_consistent():
    """
    Return True if `assignment` is consistent (i.e., words fit in crossword
    puzzle without conflicting characters); return False otherwise.
    """
    structure = "data/structure0.txt"
    words = "data/words0.txt"
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    creator.ac3()

    special_var = Variable(1, 4, "down", 4)
    # Complete assignment
    assignment = defaultdict(str)
    for var, words in creator.domains.items():
        assignment[var] = random.choice(list(words))
        if var == special_var:
            assignment[var] = "FIVE"
    result = creator.consistent(assignment)
    assert result == True

    # Incomplete assignment
    assignment = defaultdict(str)
    for var, words in creator.domains.items():
        assignment[var] = random.choice(list(words))
        if var == special_var:
            assignment[var] = "NINE"
    result = creator.consistent(assignment)
    assert result == False


def test_order_domain_values():
    """
    Return a list of values in the domain of `var`, in order by
    the number of values they rule out for neighboring variables.
    The first value in the list, for example, should be the one
    that rules out the fewest values among the neighbors of `var`.
    """
    # CrosswordCreator.order_domain_values(var, assignment)
    structure = "data/structure0.txt"
    words = "data/words0.txt"
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    creator.ac3()
    # Complete assignment
    assignment = defaultdict(str)
    for var, words in creator.domains.items():
        assignment[var] = random.choice(list(words))
    special_var = Variable(1, 4, "down", 4)
    ordered_values = creator.order_domain_values(special_var, assignment)
    
    assert isinstance(ordered_values, list)


def test_select_unassigned_variable():
    """
    Return an unassigned variable not already part of `assignment`.
    Choose the variable with the minimum number of remaining values
    in its domain. If there is a tie, choose the variable with the highest
    degree. If there is a tie, any of the tied variables are acceptable
    return values.
    """
    structure = "data/structure0.txt"
    words = "data/words0.txt"
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    
    # setup an assignment (incomplete)
    assignment = defaultdict(str)
    total = len(creator.domains)
    slice = random.choice(range(total - 1))
    partial_vars = list(creator.domains.keys())[:slice]
    for var in creator.domains:
        if var in partial_vars:
            words = creator.domains[var]
            assignment[var] = random.choice(list(words))
    selected_var = creator.select_unassigned_variable(assignment)
    
    assert selected_var in creator.crossword.variables


def test_backtrack():
    """
    Using Backtracking Search, take as input a partial assignment for the
    crossword and return a complete assignment if possible to do so.

    `assignment` is a mapping from variables (keys) to words (values).

    If no assignment is possible, return None.
    """
    structure = "data/structure2.txt"
    words = "data/words2.txt"
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)   
    creator.enforce_node_consistency()
    creator.ac3()
    result = creator.backtrack(dict())
    print("\n", result)
    if result:
        creator.print(result)
        output = "output.png"
        if output:
            creator.save(result, output)

    assert result is not None


if __name__ == "__main__":
    pytest.main()