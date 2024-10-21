import pytest
from nim import NimAI, Nim


def test_get_q_value():
    ai = NimAI()
    game = Nim()
    state = game.piles.copy()
    action = (2, 3)
    result = ai.get_q_value(state, action)

    assert result == 0


def test_update_q_value():
    ai = NimAI()
    game = Nim()
    state = game.piles.copy()
    action = (2, 3)
    # Arbitary assign a reward & best future reward
    old_q, reward, best_future = 0, 0, 2
    ai.update_q_value(state, action, old_q, reward, best_future)

    # Evaluate the new Q-value
    result = ai.get_q_value(state, action)
    assert result == 1.0


def test_best_future_reward():
    ai = NimAI()
    game = Nim()
    state = game.piles.copy()
    action = (2, 3)
    # Arbitary assign a reward & best future reward
    old_q, reward, best_future = 0, 0, 2
    ai.update_q_value(state, action, old_q, reward, best_future)

    # Make the move, update pile state
    game.move(action)
    result = ai.best_future_reward(state)
    assert result == 1.0


def test_choose_action():
    ai = NimAI()
    game = Nim()
    state = game.piles.copy()
    action = (2, 3)
    # Arbitary assign a reward & best future reward
    old_q, reward, best_future = 0, 0, 2
    ai.update_q_value(state, action, old_q, reward, best_future)

    # Make the move, update pile state
    game.move(action)
    # Use pure greedy algorithm
    result = ai.choose_action(state, False)
    assert result == (2, 3)

    # Use epsilon-greedy algorithm
    result = ai.choose_action(state)
    assert isinstance(result, tuple)


if __name__ == "__main__":
    pytest.main()