import numpy as np
import random
import time


def timer(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print("{:s} function took {:.4f} s".format(f.__name__, (time2 - time1)))

        return ret

    return wrap


class N_Puzzle:
    def __init__(self, state):
        self.state = state
        self.successors = None

    def expand(self):
        if self.successors is not None:
            return self.successors

        self.successors = []

        # find position of 0
        pos = np.argwhere(self.state == 0)[0]

        # move left/right/up/down (if possible)
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = pos + offset
            if np.all(new_pos >= 0) and np.all(new_pos < SIZE):
                new_state = self.state.copy()
                # swap elements
                new_state[tuple(pos)], new_state[tuple(new_pos)] = (
                    new_state[tuple(new_pos)],
                    new_state[tuple(pos)],
                )
                self.successors.append(N_Puzzle(new_state))

        return self.successors

    def is_solved(self):
        return self == SOLVED_PUZZLE

    def __eq__(self, other):
        # only compares states not nodes!!!
        assert type(other) == N_Puzzle
        return (self.state == other.state).all()

    def __repr__(self) -> str:
        return str(self.state) + f" with h1 = {h1(self)}" + f" and h2 = {h2(self)}"


def get_random_puzzle(valid_state, random_steps=1000):
    puzzle = N_Puzzle(valid_state)
    for i in range(random_steps):
        puzzle = random.choice(puzzle.expand())
    return puzzle


########  Search Algorithmns  ########


def breadth_first_search(root):
    queue = [root]
    while len(queue) != 0:
        node = queue.pop(0)
        if node.is_solved():
            return node
        else:
            queue.extend(node.expand())

    return None


def depth_first_search(root, depth_limit=-1):
    """if depth_limit is negative => no depth_limit, so unlimited search
    if depth_limit is positive its a boundary value"""
    if root.is_solved():
        return root

    if depth_limit != 0:
        for node in root.expand():
            solution = depth_first_search(node, depth_limit - 1)
            if solution is not None:
                return solution

    return None


def iterative_deepening(root):
    depth_limit = 0
    while True:
        solution = depth_first_search(root, depth_limit)
        if solution is not None:
            return solution
        depth_limit += 1


# heuristics:
def h1(node):
    return len(np.argwhere(node.state != SOLVED_PUZZLE.state))


def h2(node):
    manhatten_distance = 0
    for i in range(node.state.shape[0]):
        for j in range(node.state.shape[1]):
            ideal_i, ideal_j = np.argwhere(SOLVED_PUZZLE.state == node.state[i, j])[0]
            manhatten_distance += abs(i - ideal_i) + abs(j - ideal_j)

    return manhatten_distance


def A_star(root, heuristic=h2):
    queue = [(heuristic(root), root)]

    def insert(node):
        h = heuristic(node)
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


@timer
def search(f, puzzle, **kwargs):
    print("\n")
    print(
        f"searching {N}-puzzle using the '{f.__name__}' algorithm"
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
    print(puzzle)
    print()

    solution = f(puzzle, **kwargs)
    if solution is not None:
        print("solved state:")
        print(solution)
    else:
        print("no solution could be found!")
    print()


if __name__ == "__main__":
    random.seed(42)

    N = 15
    SIZE = int((N + 1) ** 0.5)

    solved_state = np.append(np.arange(1, N + 1), 0).reshape((SIZE, SIZE))
    SOLVED_PUZZLE = N_Puzzle(solved_state)

    puzzle = get_random_puzzle(solved_state.copy(), random_steps=25)

    # search(depth_first_search, puzzle, depth_limit=-1)    # no depth_limit --> RecursionError
    # search(depth_first_search, puzzle, depth_limit=5)     # depth_limit too low --> no solution
    search(depth_first_search, puzzle, depth_limit=100)
    search(breadth_first_search, puzzle)
    search(iterative_deepening, puzzle)

    search(A_star, puzzle, heuristic=h1)
    search(A_star, puzzle, heuristic=h2)
