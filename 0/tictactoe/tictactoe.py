"""
Tic Tac Toe Player
"""

import math
import copy

MAX = float('inf')
MIN = float('-inf')
X = "X"
O = "O"
EMPTY = None
N = 3


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x, o = 0, 0
    for r in range(N):
        for c in range(N):
            if board[r][c] == X:
                x += 1
            elif board[r][c] == O:
                o += 1
    
    return X if x <= o else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for r in range(N):
        for c in range(N):
            if board[r][c] == EMPTY:
                possible_moves.add((r, c))
    
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    curren_player = player(board)

    r, c = action[0], action[1]

    # Detect invalid moves
    if board[r][c] != EMPTY or r < 0 or c < 0 or r >= N or c >= N:
        print(board, action)
        raise NameError("Invalid action, chess already exist!")
    
    new_board[r][c] = curren_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner_player = None
    row_check = [set() for i in range(N)]
    col_check = [set() for i in range(N)]
    cross_check = [set(), set()]

    for r in range(N):
        for c in range(N):
            row_check[r].add(board[r][c])
            col_check[c].add(board[r][c])
            if r == c:
                cross_check[0].add(board[r][c])
            if r + c == N - 1:
                cross_check[1].add(board[r][c])
    
    # Check row and col
    for i in range(N):
        if len(row_check[i]) == 1:
            winner_player = next(iter(row_check[i]))
            if winner_player != EMPTY:
                return winner_player
        
        if len(col_check[i]) == 1:
            winner_player = next(iter(col_check[i]))
            if winner_player != EMPTY:
                return winner_player

    # Check cross
    for i in range(len(cross_check)):
        if len(cross_check[i]) == 1: 
            winner_player = next(iter(cross_check[i]))
            if winner_player != EMPTY:
                return winner_player

    return winner_player


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    winner_player = winner(board)
    if winner_player != None:
        return True

    for r in range(N):
        for c in range(N):
            if board[r][c] == EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    max_player = True if player(board) == X else False
    if max_player:
        _, action = maxvalue(board, MIN, MAX)
    else:
        _, action = minvalue(board, MIN, MAX)

    return action


def maxvalue(board, alpha, beta):
    """
    Returns the max value of all the possible move that the opponet can achieve
    """
    best_move = None
    if terminal(board):
        return utility(board), best_move
    
    score = MIN
    for action in list(actions(board)):
        min_value, _ = minvalue(result(board, action), alpha, beta)
        if score < min_value:
            score = min_value
            best_move = action
        
        alpha = max(alpha, score)
        if beta <= alpha:
            break
    
    return score, best_move


def minvalue(board, alpha, beta):
    """
    Returns the min value of all the possible move that the opponet can achieve
    """
    best_move = None
    if terminal(board):
        return utility(board), best_move
    
    score = MAX
    for action in list(actions(board)):
        max_value, _ = maxvalue(result(board, action), alpha, beta)
        if score > max_value:
            score = max_value
            best_move = action

        beta = min(beta, score)
        if beta <= alpha:
            break
    
    return score, best_move

