import numpy as np
from node import Node


def h1(node: Node):
    # ToDo: dont count zero-tile
    return np.count_nonzero(node.state != node.solution_node.state)


def h2(node: Node):
    manhattan_distance = 0
    for i in range(node.state.shape[0]):
        for j in range(node.state.shape[1]):
            if node.state[i, j] == 0:
                continue
            ideal_i, ideal_j = np.argwhere(node.solution_node.state == node.state[i, j])[0]
            manhattan_distance += abs(i - ideal_i) + abs(j - ideal_j)

    return manhattan_distance
