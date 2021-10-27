import numpy as np
import random
import time

from n_puzzle import get_random_puzzle, N_Puzzle


########  Search Algorithmn Classes  ########
# Alternative to function based calculation


class SearchAlgorithm:
    _start_puzzle: N_Puzzle
    _target_puzzle: N_Puzzle

    def __init__(self, start_puzzle: N_Puzzle, target_puzzle: N_Puzzle):
        self._start_puzzle = start_puzzle
        self._target_puzzle = target_puzzle

    def find_target(self):
        pass


class BreadthFirstSearch(SearchAlgorithm):

    def __init__(self, start_puzzle: N_Puzzle, target_puzzle: N_Puzzle):
        super().__init__(start_puzzle, target_puzzle)


class DepthFirstSearch(SearchAlgorithm):

    def __init__(self, start_puzzle: N_Puzzle, target_puzzle: N_Puzzle):
        super().__init__(start_puzzle, target_puzzle)


class IterativeDeepening(SearchAlgorithm):

    def __init__(self, start_puzzle: N_Puzzle, target_puzzle: N_Puzzle):
        super().__init__(start_puzzle, target_puzzle)


class AStar(SearchAlgorithm):

    def __init__(self, start_puzzle: N_Puzzle, target_puzzle: N_Puzzle):
        super().__init__(start_puzzle, target_puzzle)


########  Search Algorithmns  ########

def breadth_first_search(root, solution: N_Puzzle):
    queue = [root]
    while len(queue) != 0:
        node = queue.pop(0)
        if node == solution:
            return node
        else:
            queue.extend(node.expand())

    return None


def depth_first_search(root, solution: N_Puzzle, depth_limit=-1):
    if root == solution:
        return root

    if depth_limit != 0:
        for node in root.expand():
            solution = depth_first_search(root=node, solution=solution, depth_limit=depth_limit - 1)
            if solution is not None:
                return solution

    return None


def iterative_deepening(root, solution: N_Puzzle):
    depth_limit = 0

    while True:
        solution = depth_first_search(root, solution, depth_limit)
        if solution is not None:
            return solution
        depth_limit += 1


def A_star(root, solution: N_Puzzle, heuristic):
    queue = [(heuristic(root, solution), root)]

    def insert(node):
        h = heuristic(node, solution)
        for i, (value, elem) in enumerate(queue):
            if h < value:
                queue.insert(i, (h, node))
                return
        queue.insert(-1, (h, node))

    while len(queue) != 0:
        _, node = queue.pop(0)
        if node.is_solved():
            return node
        else:
            for new_node in node.expand():
                insert(new_node)

    return None

# heuristics:
def h1(node, solution: N_Puzzle):
    return len(np.argwhere(node.state != solution.state))


def h2(node, solution: N_Puzzle):
    manhatten_distance = 0
    for i in range(node.state.shape[0]):
        for j in range(node.state.shape[1]):
            ideal_i, ideal_j = np.argwhere(solution.state == node.state[i, j])[0]
            manhatten_distance += abs(i - ideal_i) + abs(j - ideal_j)

    return manhatten_distance


def print_heuristics(puzzle_a: N_Puzzle, puzzle_b: N_Puzzle):
    return str(puzzle.state) + f" with h1 = {h1(puzzle_a, puzzle_b)}" + f" and h2 = {h2(puzzle_a, puzzle_b)}"


def timer(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print("{:s} function took {:.4f} s".format(f.__name__, (time2 - time1)))

        return ret

    return wrap


@timer
def search(search_algorithm, puzzle, **kwargs):
    solved_puzzle = kwargs["solution"]
    print("\n")
    print(
        f"searching {N}-puzzle using the '{search_algorithm.__name__}' algorithm"
        + (
            f" with '" + kwargs["heuristic"].__name__ + "'-heuristic"
            if "heuristic" in kwargs
            else ""
        )
        + (
            f" with depth_limit=" + str(kwargs["depth_limit"])
            if "depth_limit" in kwargs
            else ""
        )
        + "\n"
    )
    print("initial state:")
    print(print_heuristics(puzzle, solved_puzzle))
    print()

    search_solution = search_algorithm(puzzle, **kwargs)
    if search_solution is not None:
        print("solved state:")
        print(search_solution, solved_puzzle)
    else:
        print("no solution could be found!")
    print()


if __name__ == "__main__":
    random.seed(42)

    # can be 3, 8 oder 15 = n^2 -1
    N = 3
    PUZZLE_SIZE = int((N + 1) ** 0.5)

    solved_state = np.append(np.arange(1, N + 1), 0).reshape((PUZZLE_SIZE, PUZZLE_SIZE))
    solved_puzzle = N_Puzzle(solved_state, puzzle_size=PUZZLE_SIZE)

    puzzle = get_random_puzzle(solved_state.copy(), random_steps=25, puzzle_size=PUZZLE_SIZE)

    # search(depth_first_search, puzzle, depth_limit=-1)    # no depth_limit --> RecursionError
    # search(depth_first_search, puzzle, depth_limit=5)     # depth_limit too low --> no solution
    search(depth_first_search, puzzle, solution=solved_puzzle, depth_limit=100)
    search(breadth_first_search, puzzle, solution=solved_puzzle)
    search(iterative_deepening, puzzle, solution=solved_puzzle)

    search(A_star, puzzle, solution=solved_puzzle, heuristic=h1)
    search(A_star, puzzle, solution=solved_puzzle, heuristic=h2)
