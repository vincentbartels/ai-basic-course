import numpy as np
import random


class N_Puzzle:
    def __init__(self, state: np.ndarray, puzzle_size: int):
        self.state = state
        self.successors = None
        self._puzzle_size = puzzle_size

    def expand(self):
        if self.successors is not None:
            return self.successors

        self.successors = []

        # find position of 0
        position = np.argwhere(self.state == 0)[0]
        self.move_tile(position)
        return self.successors

    def move_tile(self, position):
        """Move left/right/up/down (if possible)"""
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = position + offset
            if np.all(new_pos >= 0) and np.all(new_pos < self._puzzle_size):
                new_state = self.state.copy()
                # swap elements
                new_state[tuple(position)], new_state[tuple(new_pos)] = (
                    new_state[tuple(new_pos)],
                    new_state[tuple(position)],
                )
                self.successors.append(N_Puzzle(new_state, self._puzzle_size))

    def __eq__(self, other):
        """
        :raises: Assertion Error
        """
        # only compares states not nodes!!!
        assert type(other) == N_Puzzle
        return (self.state == other.state).all()



def get_random_puzzle(valid_state, random_steps=1000, puzzle_size: int = 0):
    puzzle = N_Puzzle(valid_state, puzzle_size=puzzle_size)
    for i in range(random_steps):
        puzzle = random.choice(puzzle.expand())
    return puzzle

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


