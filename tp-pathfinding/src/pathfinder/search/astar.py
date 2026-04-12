from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution|NoSolution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)
        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = root.cost

        # Initialize frontier with the root node
        frontier: PriorityQueueFrontier = PriorityQueueFrontier()
        frontier.add(root, root.cost + grid.manhattan(root.state))
        
        while not frontier.is_empty():
            node: Node = frontier.pop()
            possible_actions: list[str] = grid.actions(node.state)

            if grid.objective_test(node.state):
                return Solution(node, reached)

            if not possible_actions:
                return NoSolution(reached)

            for action in possible_actions:
                successor: tuple[int, int] = grid.result(node.state, action)
    
                successor_cost = node.cost + grid.individual_cost(node.state, action)

                if successor not in reached or successor_cost < reached[successor]:                              
                    son: Node = Node(
                        "",
                        state = successor,
                        cost = successor_cost,
                        parent = node,
                        action = action
                    )
                    reached[successor] = successor_cost
                    frontier.add(son, son.cost + grid.manhattan(son.state)) 
        return NoSolution(reached)