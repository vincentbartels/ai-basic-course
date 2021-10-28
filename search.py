import bisect

from node import Node
from decorators import timer, printer


@timer
@printer
def breadth_first_search(root):
    queue = [root]
    while len(queue) != 0:
        node = queue.pop(0)
        if node.is_solution():
            return node
        else:
            queue.extend(node.expand())

    return None


@timer
@printer
def depth_first_search(root, depth_limit=-1):
    """Depth search algorithm wrapper so that we call the decorators only once.
    The recursive depth_first_search_algorithm would call it on every recursion.
    """
    return depth_first_search_algorithm(root, depth_limit)


def depth_first_search_algorithm(node: Node, depth_limit):
    """if depth_limit is negative => no depth_limit, so unlimited search
    if depth_limit is positive its a boundary value"""
    if node.is_solution():
        return node

    if depth_limit != 0:
        for node in node.expand():
            solution = depth_first_search_algorithm(node, depth_limit - 1)
            if solution is not None:
                return solution
    return None


@timer
@printer
def iterative_deepening(root):
    depth_limit = 0
    while True:
        solution = depth_first_search_algorithm(root, depth_limit)
        if solution is not None:
            return solution
        depth_limit += 1


@timer
@printer
def A_star(root, heuristic):
    root.set_heuristic_value(heuristic(root))

    queue = [root]
    while len(queue) != 0:
        node = queue.pop(0)
        if node.is_solution():
            return node
        else:
            for new_node in node.expand():
                h = heuristic(new_node)
                g = node.heuristic_value
                new_node.set_heuristic_value(h + g)
                bisect.insort_left(queue, new_node)

    return None
