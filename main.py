import random
import numpy as np
from node import Node, SolutionNode
from search import breadth_first_search, iterative_deepening, A_star, depth_first_search
from heuristics import h1, h2


def get_random_puzzle(target_node, random_steps=100):
    new_start_node = Node(state=target_node.state)
    for i in range(random_steps):
        new_start_node = random.choice(new_start_node.expand())
    return new_start_node


def premade_start():
    very_easy = np.array([[1, 2, 3], [5, 0, 8], [4, 6, 7]])  # easy^2 -> 8
    easy = np.array([[1, 2, 3], [4, 5, 0], [6, 7, 8]])  # easy -> 11
    medium = np.array([[2, 0, 4], [6, 7, 1], [8, 5, 3]])  # medium -> 23
    hard = np.array([[8, 6, 7], [2, 5, 4], [3, 0, 1]])  # hard -> 31
    return Node(state=medium)


if __name__ == "__main__":
    random.seed(42)
    n = 8
    target_node = SolutionNode.instance(n)

    # ------ define initial puzzle state ----
    # puzzle = get_random_puzzle(target_node, random_steps=60)
    puzzle = premade_start()

    # ---- do searching ----
    # depth-first-search is recursive, thus it needs to be wrapped manually in timer/printer functions
    # depth_first_search(puzzle, depth_limit=-1)  # no depth_limit --> RecursionError
    # depth_first_search(puzzle, depth_limit=5)  # depth_limit too low --> no solution
    # depth_first_search(puzzle, depth_limit=15)
    # breadth_first_search(puzzle)
    # iterative_deepening(puzzle)
    # A_star(puzzle, heuristic=h1)
    A_star(puzzle, heuristic=h2)
