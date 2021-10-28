import time

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
    def print_wrap(puzzle, solved_puzzle, **kwargs):
        n = puzzle.state.shape[0] ** 2 - 1

        print(f"Searching {n}-puzzle using the '{f.__name__}' algorithm")

        # print name of heuristic function / depth limit value
        for kw in kwargs:
            kw_value = kwargs[kw] if not callable(kwargs[kw]) else kwargs[kw].__name__
            print(f"with {kw} = {kw_value}")

        print("\ninitial state:")
        print(puzzle)
        print(f"h1 = {h1(puzzle, solved_puzzle)}; h2 = {h2(puzzle, solved_puzzle)}")

        solution = f(puzzle, solved_puzzle, **kwargs)
        if solution is None:
            print("no solution could be found!")

        else:
            print("\nsolved state:")
            print(solution)
            print(f"h1 = {h1(solution, solved_puzzle)}; h2 = {h2(solution, solved_puzzle)}")
        print()

        return solution

    return print_wrap
