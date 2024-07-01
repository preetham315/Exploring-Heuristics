

import sys
from copy import deepcopy
from pyparsing import col
import numpy as np
from queue import PriorityQueue
############ Tests ############
cstate = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
board= deepcopy(cstate)
ROWS = 5
COLS = 5

def move_right(board, row):
  """Move the given row to one position right"""
  board[row] = board[row][-1:] + board[row][:-1]
  return board

def move_left(board, row):
  """Move the given row to one position left"""
  board[row] = board[row][1:] + board[row][:1]
  return board

def rotate_right(board,row,residual):
    board[row] = [board[row][0]] +[residual] + board[row][1:]
    residual=board[row].pop()
    return residual

def rotate_left(board,row,residual):
    board[row] = board[row][:-1] + [residual] + [board[row][-1]]
    residual=board[row].pop(0)
    return residual

def move_clockwise(board):
    """Move the outer ring clockwise"""
    board[0]=[board[1][0]]+board[0]
    residual=board[0].pop()
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,0,residual)
    board=transpose_board(board)
    return board

def move_cclockwise(board):
    """Move the outer ring counter-clockwise"""
    board[0]=board[0]+[board[1][-1]]
    residual=board[0].pop(0)
    board=transpose_board(board)
    residual=rotate_right(board,0,residual)
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    return board

def transpose_board(board):
  """Transpose the board --> change row to column"""
  return [list(col) for col in zip(*board)]

def path_finder(board, path_):
  board = np.array(board).reshape(ROWS, COLS).tolist()
  """Uses the output of student's path to reach canonical state"""
  for direction in path_:
    if set(direction).intersection(set(['U','D','R','L'])):
        direction,index=direction
        index=int(index)-1
    if direction == "R":
        board = move_right(board, index)
    elif direction == "L":
        board = move_left(board, index)
    elif direction == "U":
        board = transpose_board(move_left(transpose_board(board), index))
    elif direction == "D":
        board = transpose_board(move_right(transpose_board(board), index))
    elif direction == 'Oc':
        board = move_clockwise(board)
    elif direction == 'Occ':
        board = move_cclockwise(board)
    elif direction == 'Ic':
        board=np.array(board)
        inner_board=board[1:-1,1:-1].tolist()
        inner_board = move_clockwise(inner_board)
        board[1:-1,1:-1]=np.array(inner_board)
        board=board.tolist()
    elif direction == 'Icc':
        board=np.array(board)
        inner_board=board[1:-1,1:-1].tolist()
        inner_board = move_cclockwise(inner_board)
        board[1:-1,1:-1]=np.array(inner_board)
        board=board.tolist()
  return board


# heuristic function : Manhattan dsitance. Calculated the difference in absolute values of row_man and row, respectively for column
def h(board):
    distance = 0
    row_manhattan = 0
    column_manhattan= 0
    
    for row in range(len(board)):
        for column in range(len(board[0])):
            for actual_row in range(len(cstate)):
                for actual_column in range(len(cstate[0])):
                    if cstate[actual_row][actual_column] == board[row][column]:
                        row_manhattan = actual_row
                        column_manhattan = actual_column
            distance += abs(row_manhattan - row) + abs(column_manhattan - column)
        
    return distance

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]


# return a list of possible successor states
def successors(state):
    next_states = []
    for i in range(len(state)):
        next_states.append(move_right(deepcopy(state), i))
        next_states.append(move_left(deepcopy(state), i))
        next_states.append(rotate_left(deepcopy(state), i))
        next_states.append(rotate_right(deepcopy(state), i))
    
    next_states.append(move_cclockwise(state))
    next_states.append(move_clockwise(state))
    return True

# check if we've reached the goal
def is_goal(state):
    for row in range(len(state)):
        for  column in range(len(state[0])):
            if state[row][column] != (row * 5) + (column + 1):
                return False
    
    return True
# implemented the priority queue same as question 1
def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    # return ["Oc","L2","Icc", "R4"]
    
    fringe = PriorityQueue()
    fringe.put((h((initial_board)), ((initial_board), h(initial_board), [])))
    node_visited = []
    
    while fringe.qsize() > 0:
        next_state = fringe.get()
        (state, heuristic_value, path) = next_state
        
        node_visited.append(state)

        if is_goal(state):
            return path

        successor_states = successors((state))

        for s in successor_states:
            if s[0] not in node_visited:
                heuristic_value = h(s[0])
                fringe.put((s[0], heuristic_value, path+[s[2],]))
                node_visited.append(s[0])

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
