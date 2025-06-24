"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


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
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.add((i,j))
    return possible_moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    
    if board[i][j] != EMPTY:
        raise Exception("Invalid move")
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win==X:
        return 1
    elif win==0:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    current = player(board)
    def max_value(board):
        if terminal(board):
            return utility(board), None
        v = -math.inf
        move = None
        for action in actions(board):
            min_v, _ = min_value(result(board, action))
            if min_v > v:
                v = min_v
                move = action
        return v, move
    def min_value(board):
        if terminal(board):
            return utility(board), None
        v = math.inf
        move = None
        for action in actions(board):
            max_v, _ = max_value(result(board, action))
            if max_v < v:
                v = max_v
                move = action
        return v, move
    return max_value(board)[1] if current == X else min_value(board)[1]