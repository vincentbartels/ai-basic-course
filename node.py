import numpy as np


class Node(object):
    def __init__(self, state=None, depth=0, predecessor=None):
        self.state: np.ndarray = state
        self.depth = depth
        self.solution_node: SolutionNode = SolutionNode.instance()
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
        """Compare both matrix element wise and check if the resulting matrix has any element that is zero
        if yes, than return false."""
        assert isinstance(other, Node)
        return (self.state == other.state).all()

    def __lt__(self, other):
        """Check is the heuristic of this node is less than the other."""
        assert type(other) == Node
        return self.heuristic_value < other.heuristic_value

    def __repr__(self) -> str:
        """Print node state (numpy array) as string"""

        return str(self.state)

    def is_solution(self):
        return self == self.solution_node


class SolutionNode(Node):
    _instance = None

    def __init__(self, n: int = 3):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, n=3):
        if cls._instance is None:
            print(f'Creating new instance in {n}-puzzle')
            cls._instance = super(SolutionNode, cls).__new__(cls)
            size = int((n + 1) ** 0.5)
            solution_state = np.append(np.arange(1, n + 1), 0).reshape((size, size))
            super(SolutionNode, cls._instance).__init__(solution_state)
        return cls._instance
