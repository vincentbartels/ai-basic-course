import random
import numpy as np

from n_puzzle import Node, get_solution_node_state, get_random_puzzle
from search import breadth_first_search, iterative_deepening, A_star, depth_first_search
from heuristics import h1, h2

if __name__ == "__main__":
    random.seed(42)
    n = 8

    # Define search target
    solved_state = get_solution_node_state(n)
    solved_puzzle = Node(solved_state)

    # define initial puzzle state
    puzzle = get_random_puzzle(solved_state, random_steps=60)
    # puzzle = Node(np.array([[2, 0, 4], [6, 7, 1], [8, 5, 3]]))

    # do searching

    # depth-first-search is recursive, thus it needs to be wrapped manually in timer/printer functions
    depth_first_search(puzzle, solved_puzzle, depth_limit=-1)  # no depth_limit --> RecursionError
    depth_first_search(puzzle, solved_puzzle, depth_limit=5)  # depth_limit too low --> no solution
    depth_first_search(puzzle, solved_puzzle, depth_limit=100)
    breadth_first_search(puzzle, solved_puzzle)
    iterative_deepening(puzzle, solved_puzzle)

    # A_star(puzzle, solved_puzzle, heuristic=h1)
    A_star(puzzle, solved_puzzle, heuristic=h2)
