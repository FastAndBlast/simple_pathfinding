import math
from typing import List, Optional


class pathfinding_base:
    def __init__(self, input_map: List[List[Optional[int]]]) -> None:
        self.width = 0
        self.height = len(input_map)

        if self.height > 0:
            self.width = len(input_map[0])
        else:
            return

        self.closed_list = []

    def valid_adjacent(self, x, y):
        return self.grid[x][y].passable and not self.grid[x][y] in self.closed_list

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

    def get_path(self, start, end) -> List[int]:
        pass


class astar_node:
    def __init__(self, x: int, y: int, cost: Optional[int]) -> None:
        self.x = x
        self.y = y
        self.cost = cost
        self.passable = True
        self.prev = None
        self.g = 0
        self.h = 0

    def f(self) -> float:
        return self.g + self.h

    def to_coord_list(self) -> List:
        return [self.x, self.y]

    def __repr__(self) -> str:
        return str(self.to_coord_list())


class astar(pathfinding_base):
    def __init__(self, input_map: List[List[Optional[int]]]) -> None:
        self.open_list = []

        super().__init__(input_map)

        self.grid = []
        for x in range(self.width):
            self.grid.append([])
            for y in range(self.height):
                node = astar_node(x, y, input_map[self.height - y - 1][x])
                if input_map[self.height - y - 1][x] == None:
                    node.passable = False
                self.grid[x].append(node)

    def get_path(self, start: List[int], end: List[int]) -> List:
        self.open_list = []
        self.closed_list = []

        start_node = self.grid[start[0]][start[1]]
        end_node = self.grid[end[0]][end[1]]

        start_node.h = self.distance(start_node, end_node)

        self.open_list.append(start_node)

        while self.open_list != []:
            node = self.open_list.pop(0)

            if node is end_node:
                path = []
                while node:
                    path.insert(0, node.to_coord_list())
                    node = node.prev
                return path

            self.closed_list.append(node)

            for adjacent_node in self.get_adjacent(node):
                if adjacent_node in self.open_list:
                    if node.g + node.cost < adjacent_node.g:
                        adjacent_node.prev = node
                        adjacent_node.g = node.g + node.cost
                else:
                    adjacent_node.prev = node
                    adjacent_node.g = node.g + node.cost
                    adjacent_node.h = self.distance(adjacent_node, end_node)
                    self.open_list.append(adjacent_node)

            self.open_list = sorted(
                self.open_list, key=lambda x: x.f(), reverse=True)

        return []


class dijkstra_node:
    def __init__(self, x: int, y: int, cost: Optional[int], tentative_distance=float("inf")) -> None:
        self.x = x
        self.y = y
        self.tentative_distance = tentative_distance
        self.cost = cost
        self.passable = True
        self.prev = None

    def to_coord_list(self) -> List:
        return [self.x, self.y]

    def __repr__(self) -> str:
        return str(self.to_coord_list())


class dijkstra(pathfinding_base):
    def __init__(self, input_map: List[List[Optional[int]]]) -> None:
        self.unvisited = []

        super().__init__(input_map)

        self.grid = []
        for x in range(self.width):
            self.grid.append([])
            for y in range(self.height):
                node = dijkstra_node(x, y, input_map[self.height - y - 1][x])
                if input_map[self.height - y - 1][x] == None:
                    node.passable = False
                else:
                    self.unvisited.append(node)
                self.grid[x].append(node)

    def set_unvisited(self):
        unvisited = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].passable:
                    unvisited.append(self.grid[x][y])

    def get_path(self, start: List[int], end: List[int]) -> List:
        self.set_unvisited()

        initial_node = self.grid[start[0]][start[1]]
        initial_node.tentative_distance = 0

        current_node = None

        while self.unvisited != []:
            self.unvisited = sorted(
                self.unvisited, key=lambda x: x.tentative_distance)

            current_node = self.unvisited[0]

            for adjacent_node in self.get_adjacent(current_node):
                distance = current_node.tentative_distance + current_node.cost
                if distance < adjacent_node.tentative_distance:
                    adjacent_node.tentative_distance = distance
                    adjacent_node.prev = current_node

            if current_node in self.unvisited:
                self.unvisited.remove(current_node)

            if current_node == self.grid[end[0]][end[1]]:
                path = []
                while current_node:
                    path.insert(0, current_node.to_coord_list())
                    current_node = current_node.prev
                return path

        return []


class breadth_node:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.passable = True
        self.prev = None

    def to_coord_list(self) -> List:
        return [self.x, self.y]

    def __repr__(self) -> str:
        return str(self.to_coord_list())


class breadth_first(pathfinding_base):
    def __init__(self, input_map: List[List[Optional[int]]]) -> None:
        super().__init__(input_map)

        self.grid = []
        for x in range(self.width):
            self.grid.append([])
            for y in range(self.height):
                node = breadth_node(x, y)
                if input_map[self.height - y - 1][x] == None:
                    node.passable = False
                self.grid[x].append(node)

    def get_path(self, start: List[int], end: List[int]) -> List:
        if start == end:
            return [start]

        initial_node = self.grid[start[0]][start[1]]

        self.closed_list = [initial_node]

        queue = [initial_node]

        while queue != []:
            current_node = queue.pop(0)

            adjacent_list = self.get_adjacent(current_node)

            for adjacent_node in adjacent_list:
                adjacent_node.prev = current_node
                if adjacent_node == self.grid[end[0]][end[1]]:
                    path = []
                    while adjacent_node:
                        path.insert(0, adjacent_node.to_coord_list())
                        adjacent_node = adjacent_node.prev
                    return path

                queue.append(adjacent_node)
                self.closed_list.append(adjacent_node)

        return []
