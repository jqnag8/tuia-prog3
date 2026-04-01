from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution | NoSolution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None) # root

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = True

        # Applying objective_test on root
        if grid.objective_test(root.state):
            return Solution(root, reached)
        

        # Initialize frontier with the root node
        frontier: QueueFrontier = QueueFrontier()
        frontier.add(root)


        while True:
            if frontier.is_empty():
                return NoSolution(reached)

            node: Node = frontier.remove()
            possible_actions: list[str] = grid.actions(node.state)

            if not possible_actions:
                return NoSolution(reached)

            for action in possible_actions:
                successor: tuple[int, int] = grid.result(node.state, action)

                if successor in reached:
                    continue # Successor is already in reached            
                    
                son: Node = Node(
                    "",
                    state = successor,
                    cost = node.cost + grid.individual_cost(node.state, action),
                    parent = node,
                    action = action)

                if grid.objective_test(successor):
                    return Solution(son, reached)

                reached[successor] = True
                frontier.add(son)

    
