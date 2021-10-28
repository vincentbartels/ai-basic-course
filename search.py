import numpy as np
import bisect

from decorators import timer, printer


@timer
@printer
def breadth_first_search(root, solved_puzzle):
    queue = [root]
    while len(queue) != 0:
        node = queue.pop(0)
        if node == solved_puzzle:
            return node
        else:
            queue.extend(node.expand())

    return None


# cannot use decorators for recursive function :(
def depth_first_search(root, solved_puzzle, depth_limit=-1):
    if root == solved_puzzle:
        return root

    if depth_limit != 0:
        for node in root.expand():
            solution = depth_first_search(node, solved_puzzle, depth_limit - 1)
            if solution is not None:
                return solution

    return None


@timer
@printer
def iterative_deepening(root, solved_puzzle):
    depth_limit = 0
    while True:
        solution = depth_first_search(root, solved_puzzle, depth_limit)
        if solution is not None:
            return solution
        depth_limit += 1


@timer
@printer
def A_star(root, solved_puzzle, heuristic):
    root.set_heuristic_value(heuristic(root, solved_puzzle))

    queue = [root]
    while len(queue) != 0:
        node = queue.pop(0)
        if node == solved_puzzle:
            return node
        else:
            for new_node in node.expand():
                h = heuristic(new_node, solved_puzzle)
                g = node.heuristic_value
                new_node.set_heuristic_value(h + g)
                bisect.insort_left(queue, new_node)

    return None
