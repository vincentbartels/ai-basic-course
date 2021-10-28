import numpy as np


def h1(self, solved_puzzle):
    # ToDo: dont count zero-tile
    return np.count_nonzero(self.state != solved_puzzle.state)


def h2(self, solved_puzzle):
    manhattan_distance = 0
    for i in range(self.state.shape[0]):
        for j in range(self.state.shape[1]):
            if self.state[i, j] == 0:
                continue
            ideal_i, ideal_j = np.argwhere(solved_puzzle.state == self.state[i, j])[0]
            manhattan_distance += abs(i - ideal_i) + abs(j - ideal_j)

    return manhattan_distance
