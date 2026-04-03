from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)
        
        # Initialize expanded with the empty dictionary
        expanded : dict[tuple[int, int], bool] = dict()
        expanded[root.state] = True

        if grid.objective_test(root.state):
            return Solution(root, expanded)
        
        frontier: StackFrontier = StackFrontier()
        frontier.add(root)
        
        while not frontier.is_empty():
            node : Node = frontier.remove()
            possible_actions : list[str] = grid.actions(node.state)

            if not possible_actions:            # Consultar redundancia
                return NoSolution(expanded)

            for action in possible_actions:
                successor: tuple[int, int] = grid.result(node.state, action)

                if successor in expanded:
                    continue # Successor is already in expanded            
                    
                son: Node = Node(
                    "",
                    state = successor,
                    cost = node.cost + grid.individual_cost(node.state, action),
                    parent = node,
                    action = action)

                if grid.objective_test(successor):
                    return Solution(son, expanded)

                expanded[successor] = True
                frontier.add(son)

        return NoSolution(expanded)
