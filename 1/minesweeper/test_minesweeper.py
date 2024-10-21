import pytest
from minesweeper import Minesweeper, Sentence, MinesweeperAI


def test_minesweeper_initialization():
    game = Minesweeper(height=8, width=8, mines=10)
    assert game.height == 8
    assert game.width == 8
    assert len(game.mines) == 10


def test_nearby_mines():
    game = Minesweeper(height=3, width=3, mines=1)
    game.mines = {(0, 0)}
    game.board[0][0] = True
    assert game.nearby_mines((1, 1)) == 1
    assert game.nearby_mines((2, 2)) == 0


def test_sentence():
    sentence = Sentence({(0, 0), (0, 1), (1, 0)}, 2)
    assert sentence.known_mines() == set()
    assert sentence.known_safes() == set()

    sentence = Sentence({(0, 0)}, 1)
    assert sentence.known_mines() == {(0, 0)}

    sentence = Sentence({(0, 0), (0, 1)}, 0)
    assert sentence.known_safes() == {(0, 0), (0, 1)}


def test_minesweeper_ai():
    ai = MinesweeperAI(height=8, width=8)
    assert ai.height == 8
    assert ai.width == 8
    assert len(ai.moves_made) == 0
    assert len(ai.mines) == 0
    assert len(ai.safes) == 0
    assert len(ai.knowledge) == 0


def test_ai_add_knowledge():
    ai = MinesweeperAI(height=3, width=3)
    ai.add_knowledge((1, 1), 0)
    assert (1, 1) in ai.moves_made
    assert (1, 1) in ai.safes
    assert len(ai.knowledge) == 1


def test_ai_make_safe_move():
    ai = MinesweeperAI(height=3, width=3)
    ai.safes.add((0, 0))
    assert ai.make_safe_move() == (0, 0)
    ai.moves_made.add((0, 0))
    assert ai.make_safe_move() is None


def test_ai_make_random_move():
    ai = MinesweeperAI(height=1, width=1)
    assert ai.make_random_move() == (0, 0)
    ai.moves_made.add((0, 0))
    assert ai.make_random_move() is None


def print_ai_status(move, nearby_count, ai):
    print(f'\nAfter move:{move} with nearby_count:{nearby_count}')
    if ai.knowledge:
        print('Sentences in Knowledge Base:')
        for cnt, s in enumerate(ai.knowledge):
            print(f'{cnt}: {s}')
    else:
        print('NO Sentences in Knowledge Base.')       
    print(f'Safe Cells: {sorted(list(ai.safes))}')
    print(f'Mine Cells: {sorted(list(ai.mines))}')   


def test_add_knowledge_basic():
    # Create AI agent
    HEIGHT, WIDTH, MINES = 8, 8, 8
    ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

    # Test new sentence logic (3rd requirement)
    move, nearby_count = (1, 1), 0
    ai.add_knowledge(move, nearby_count)
    print_ai_status(move, nearby_count, ai)

    move, nearby_count = (2, 2), 2
    ai.add_knowledge(move, nearby_count)
    print_ai_status(move, nearby_count, ai)

    # Test inference logic for new safes or mines (4th requirement)
    move, nearby_count = (3, 3), 0
    ai.add_knowledge(move, nearby_count)
    print_ai_status(move, nearby_count, ai)


def test_subset():
    # Create AI agent
    HEIGHT, WIDTH, MINES = 8, 8, 8
    ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

    # Test new sentence logic (3rd requirement)
    move, nearby_count = (1, 1), 0
    ai.add_knowledge(move, nearby_count)
    print_ai_status(move, nearby_count, ai)

    move, nearby_count = (2, 2), 2
    ai.add_knowledge(move, nearby_count)
    print_ai_status(move, nearby_count, ai)

    # Test inference logic for new safes or mines (4th requirement)
    move, nearby_count = (3, 3), 0
    ai.add_knowledge(move, nearby_count)
    print_ai_status(move, nearby_count, ai)

    # Setup for new sentence inference logic test
    move, nearby_count = (4, 2), 1
    ai.add_knowledge(move, nearby_count)
    print_ai_status(move, nearby_count, ai)

    # Tests subset inference logic for new sentences (5th requirement)
    move, nearby_count = (7, 2), 2
    ai.add_knowledge(move, nearby_count)
    print_ai_status(move, nearby_count, ai)

    move, nearby_count = (5, 2), 1
    ai.add_knowledge(move, nearby_count)
    print_ai_status(move, nearby_count, ai)


if __name__ == "__main__":
    pytest.main()
