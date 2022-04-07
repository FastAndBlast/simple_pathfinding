import math
from typing import List, Tuple, Optional


class PathfindingBase:
    def __init__(self, input_map: List[List[Optional[int]]]) -> None:
        self.height = 0
        self.width = len(input_map)

        if self.width > 0:
            self.height = len(input_map[0])

        self.closed_list: List = []
        self.grid: List = []

    def valid_adjacent(self, x: int, y: int) -> bool:
        return self.grid[x][y].is_passable and not self.grid[x][y] in self.closed_list

    def get_adjacent(self, node) -> List:
        adjacent_list = []

        if node.x > 0 and self.valid_adjacent(node.x - 1, node.y):
            adjacent_list.append(self.grid[node.x - 1][node.y])
        if node.y < self.height - 1 and self.valid_adjacent(node.x, node.y + 1):
            adjacent_list.append(self.grid[node.x][node.y + 1])
        if node.y > 0 and self.valid_adjacent(node.x, node.y - 1):
            adjacent_list.append(self.grid[node.x][node.y - 1])
        if node.x < self.width - 1 and self.valid_adjacent(node.x + 1, node.y):
            adjacent_list.append(self.grid[node.x + 1][node.y])

        return adjacent_list

    def distance(self, start, end) -> float:
        return math.sqrt((end.x - start.x) ** 2 + (end.y - start.y) ** 2)

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[int]:
        raise Exception("Find path not implemented")


class AstarNode:
    def __init__(self, x: int, y: int, cost: Optional[int]) -> None:
        self.x = x
        self.y = y
        self.cost = cost
        self.is_passable = cost is not None
        self.prev = None
        self.start_dist = 0
        self.end_dist = 0

    def f(self) -> float:
        return self.start_dist + self.end_dist

    def to_coord_list(self) -> Tuple[int, int]:
        return (self.x, self.y)


class Astar(PathfindingBase):
    '''
        A class to represent the Astar pathfinder class

        Methods
            find_path(start, end):
                Finds and returns the shortest path from start to end

    '''

    def __init__(self, input_map: List[List[Optional[int]]]) -> None:
        '''
        Initializes the Astar pathfinder class

            Parameters:
                input_map (List[List[Optional[int]]]): Input map of integers, each integer represents the cost of the node
                    at location of x, y. None represents a wall

            Returns:
                None

        '''
        super().__init__(input_map)

        self.open_list: List = []

        self.grid = []
        for x in range(self.width):
            self.grid.append([])
            for y in range(self.height):
                cost = input_map[x][y]
                node = AstarNode(x, y, cost)
                self.grid[x].append(node)

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List:
        '''
        Finds and returns the shortest path from start to end

            Parameters:
                start (Tuple[int, int]): Coordinates of the start node
                end (Tuple[int, int]): Coordinates of the end node

            Returns:
                path (List[Tuple[int, int]]): List of Tuples of coordinates of the shortest path from start to end

        '''
        self.open_list = []
        self.closed_list = []

        start_node = self.grid[start[0]][start[1]]
        end_node = self.grid[end[0]][end[1]]

        start_node.end_dist = self.distance(start_node, end_node)

        self.open_list.append(start_node)

        while self.open_list:
            node = self.open_list.pop()

            if node is end_node:
                path = []
                while node:
                    path.append(node.to_coord_list())
                    node = node.prev
                path.reverse()
                return path

            self.closed_list.append(node)

            for adjacent_node in self.get_adjacent(node):
                if adjacent_node in self.open_list:
                    if node.start_dist + node.cost < adjacent_node.start_dist:
                        adjacent_node.prev = node
                        adjacent_node.start_dist = node.start_dist + node.cost
                else:
                    adjacent_node.prev = node
                    adjacent_node.start_dist = node.start_dist + node.cost
                    adjacent_node.end_dist = self.distance(
                        adjacent_node, end_node)
                    self.open_list.append(adjacent_node)

            self.open_list = sorted(
                self.open_list, key=lambda x: x.f())

        return []


class DijkstraNode:
    def __init__(self, x: int, y: int, cost: Optional[int], tentative_distance=float("inf")) -> None:
        self.x = x
        self.y = y
        self.tentative_distance = tentative_distance
        self.cost = cost
        self.is_passable = cost is not None
        self.prev = None

    def to_coord_list(self) -> Tuple[int, int]:
        return (self.x, self.y)


class Dijkstra(PathfindingBase):
    '''
        A class to represent the Dijkstra pathfinder class

        Methods
            find_path(start, end):
                Finds and returns the shortest path from start to end

    '''

    def __init__(self, input_map: List[List[Optional[int]]]) -> None:
        '''
        Initializes the Dijkstra pathfinder class

            Parameters:
                input_map (List[List[Optional[int]]]): Input map of integers, each integer represents the cost of the node
                    at location of x, y. None represents a wall

            Returns:
                None

        '''
        super().__init__(input_map)

        self.unvisited: List = []

        self.grid = []
        for x in range(self.width):
            self.grid.append([])
            for y in range(self.height):
                cost = input_map[x][y]
                node = DijkstraNode(x, y, cost)
                self.grid[x].append(node)

    def init_unvisited(self):
        self.unvisited = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].is_passable:
                    self.unvisited.append(self.grid[x][y])

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List:
        '''
        Finds and returns the shortest path from start to end

            Parameters:
                start (Tuple[int, int]): Coordinates of the start node
                end (Tuple[int, int]): Coordinates of the end node

            Returns:
                path (List[Tuple[int, int]]): List of Tuples of coordinates of the shortest path from start to end

        '''

        self.init_unvisited()

        initial_node = self.grid[start[0]][start[1]]
        initial_node.tentative_distance = 0
        end_node = self.grid[end[0]][end[1]]

        current_node = None

        while self.unvisited:
            self.unvisited = sorted(
                self.unvisited, key=lambda x: x.tentative_distance, reverse=True)

            current_node = self.unvisited.pop()

            if current_node is end_node:
                path = []
                while current_node:
                    path.append(current_node.to_coord_list())
                    current_node = current_node.prev
                path.reverse()
                return path

            for adjacent_node in self.get_adjacent(current_node):
                distance = current_node.tentative_distance + current_node.cost
                if distance < adjacent_node.tentative_distance:
                    adjacent_node.tentative_distance = distance
                    adjacent_node.prev = current_node

        return []


class BreadthNode:
    def __init__(self, x: int, y: int, is_passable=True) -> None:
        self.x = x
        self.y = y
        self.is_passable = is_passable
        self.prev = None

    def to_coord_list(self) -> Tuple[int, int]:
        return (self.x, self.y)


class BreadthFirst(PathfindingBase):
    '''
        A class to represent the BreadthFirst pathfinder class

        Methods
            find_path(start, end):
                Finds and returns a path from start to end

    '''

    def __init__(self, input_map: List[List[Optional[int]]]) -> None:
        '''
        Initializes the BreadthFirst pathfinder class

            Parameters:
                input_map (List[List[Optional[int]]]): Input map of integers, each integer represents the cost of the node
                    at location of x, y. None represents a wall

            Returns:
                None

        '''
        super().__init__(input_map)

        self.grid = []
        for x in range(self.width):
            self.grid.append([])
            for y in range(self.height):
                cost = input_map[x][y]
                node = BreadthNode(x, y, cost is not None)
                self.grid[x].append(node)

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List:
        '''
        Finds and returns path from start to end

            Parameters:
                start (Tuple[int, int]): Coordinates of the start node
                end (Tuple[int, int]): Coordinates of the end node

            Returns:
                path (List[Tuple[int, int]]): List of Tuples of coordinates of a path from start to end

        '''
        if start == end:
            return [start]

        initial_node = self.grid[start[0]][start[1]]
        end_node = self.grid[end[0]][end[1]]

        self.closed_list = [initial_node]

        queue = [initial_node]

        while queue:
            current_node = queue.pop(0)

            adjacent_list = self.get_adjacent(current_node)

            for adjacent_node in adjacent_list:
                adjacent_node.prev = current_node
                if adjacent_node is end_node:
                    path = []
                    while adjacent_node:
                        path.append(adjacent_node.to_coord_list())
                        adjacent_node = adjacent_node.prev
                    path.reverse()
                    return path

                queue.append(adjacent_node)
                self.closed_list.append(adjacent_node)

        return []
