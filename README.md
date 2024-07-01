# Problem 1 - Birds, heuristics, and A*

Here our problem is sort the given 5 integers in 10 seconds. The given code works only if some of the numbers are misplaced. But when the list is in reverse order the exisiting code takes 20 seconds to run the code. So here to make this code efficient, we have make our fringe a priority queue and update our heuristic function.

In this problem, we can obtain the solution in mayy ways. But my heuristic function is based on Manhattan distance. So here, we calculate the absolute difference for current state and our goal state. Our goal state can be obtained by adding 1 to the index where the number is placed.

I make the fringe to be priority queue so that, instead of popping the intermediate states in order we can get the states which have more priority. So here distance would be our priority factor. Which ever distance comes out to be less, it would be popped out of the firnge first and next states are calculated based on that state and push all the next states to fringe.

We will continue the same procedure until the fringe is empty an we reach the goal state. Once we reach the goal state, we return all the intermidate states that we came across to attain the goal state.

# Problem 2 - The  2022  Puzzle

The goal of the problem is to find the less number of board moves that will give us a board that is ordered.

Search Algorithm

This problem's search algorithm is an A* search, which starts by exploring the most promising state in the fringe. The states in the fringe are stored using a data structure called a min-heap.

Initial State - 25 tiles board with initial board condition

State-Space - All board after valid moves (move entire row left/right, entire column up/down and outer and inner circle in clockwise and counter clockwise)

Successor Function - A function that after the change returns all legitimate board states.

Goal State - Ordered 2d board

For this search problem-

Cost function - cost of one board move. It accumulates cost of board move through the search.

Heuristic Function - Count of number of misplaced tiles in the board is considered as this is admissible. Preferred option for heuristic function was the sum of the number of moves of each tile to bring it to its correct place.

Total cost which is the sum of these cost functions is used as priority for the states in the fringe.

Question-1: The search tree's branching factor is 24. 5 possibilities for row right, 5 options for row left, 5 options for column up, 5 options for column down, 2 moves around the outside ring (clockwise and counterclockwise), and 2 moves around the inner ring (clockwise and counter clockwise).

Question-2: If the answer can be achieved in 7 moves, then if we use breadth-first search (BFS) instead of A* search, then a total of $7 + 7^2 + 7^3 + 7^4 + 7^5 + 7^6 + 7^7$, approx $7^7$ states.
Jotting down the thought process -

This search algorithm uses best cost function g(s) to keep track of cost from the start state to current intermediate state and heuristic cost function h(s) that calculates cost of reaching goal state from current intermediate step.

I tried to write the manhattan distance in the heuristic to find the optimal distance and used the same priority queue class in the solve function which i used in problem 1

* [Reference](https://docs.python.org/3/library/queue.html)

