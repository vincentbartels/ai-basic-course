import time

from node import Node
from heuristics import h1, h2

# from search import h1, h2

########  Decorator Functions  ########
#                                     #
#   for generating a pretty output    #
#   and timing each search function   #
#                                     #


def timer(f):
    def time_wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print("This search took {:.4f} s to complete\n\n".format((time2 - time1)))

        return ret

    return time_wrap


def printer(f):
    def print_wrap(node: Node, **kwargs):
        n = node.state.shape[0] ** 2 - 1

        print(f"Searching {n}-node using the '{f.__name__}' algorithm")

        # print name of heuristic function / depth limit value
        for kw in kwargs:
            kw_value = kwargs[kw] if not callable(kwargs[kw]) else kwargs[kw].__name__
            print(f"with {kw} = {kw_value}")

        print("\ninitial state:")
        print(node)
        print(f"h1 = {h1(node)}; h2 = {h2(node)}")


        search_result: Node = f(node, **kwargs)
        if search_result is None:
            print("no solution could be found!")

        else:
            print("\nsolved state:")
            print(search_result)
            print(f"h1 = {h1(search_result)}; h2 = {h2(search_result)}")
            print(f"solution depth: {search_result.depth}")
        print()

        return search_result

    return print_wrap
