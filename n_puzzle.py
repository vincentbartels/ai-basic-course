import numpy as np
import random


class Node:
    def __init__(self, state, depth=0, predecessor=None):
        self.state = state
        self.depth = depth

        self.predecessor = predecessor

    def expand(self):
        successors = []

        # find position of 0
        pos = np.argwhere(self.state == 0)[0]

        # move left/right/up/down (if possible)
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = pos + offset
            if np.all(new_pos >= 0) and np.all(new_pos < self.state.shape[0]):
                new_state = self.state.copy()
                # swap elements
                new_state[tuple(pos)], new_state[tuple(new_pos)] = (
                    new_state[tuple(new_pos)],
                    new_state[tuple(pos)],
                )
                successors.append(Node(new_state, depth=self.depth + 1, predecessor=self))

        return successors

    def set_heuristic_value(self, value):
        self.heuristic_value = value

    def __eq__(self, other):
        assert type(other) == Node
        # only compares states not nodes!!!
        return (self.state == other.state).all()

    def __lt__(self, other):
        assert type(other) == Node
        return self.heuristic_value < other.heuristic_value

    def __repr__(self) -> str:
        return str(self.state)


def get_solved_state(n):
    size = int((n + 1) ** 0.5)

    return np.append(np.arange(1, n + 1), 0).reshape((size, size))


def get_random_puzzle(valid_state, random_steps=100):
    puzzle = Node(valid_state)
    for i in range(random_steps):
        puzzle = random.choice(puzzle.expand())
    return puzzle
