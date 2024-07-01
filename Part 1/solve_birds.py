

# !/usr/bin/env python3
import sys
from turtle import distance
from queue import PriorityQueue

N=5

#####
# THE ABSTRACTION:
#
# Initial state:

# Goal state:
# given a state, returns True or False to indicate if it is the goal state
def is_goal(state):
    return state == list(range(1, N+1))

# Successor function:
# given a state, return a list of successor states
def successors(state):
    return [ state[0:n] + [state[n+1],] + [state[n],] + state[n+2:] for n in range(0, N-1) ]

# Heuristic function:
# using manhattan distance calculating the distance by using the index and initial state elements of that respective index
def h(state):
    distance = 0
    for i in range(0, len(state)):
        distance = distance + abs(i+1-state[i])
    return distance
#########
#
# THE ALGORITHM:

#
def solve(initial_state):
    fringe = PriorityQueue()

    fringe.put((h(initial_state), (initial_state, [])))
    while fringe.qsize() > 0:
        intermediate_state = fringe.get()
        (distance, (inter_state, final_path)) = intermediate_state
        if is_goal(inter_state):
            return final_path+[inter_state,]

        for s in successors(inter_state):
            fringe.put((h(s), (s, final_path+[inter_state,])))
    return []


#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a test case filename"))

    test_cases = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            test_cases.append([ int(i) for i in line.split() ])
    for initial_state in test_cases:
        	print('From state ' + str(initial_state) + " found goal state by taking path: " + str(solve(initial_state)))

    

