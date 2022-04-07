import simple_pathfinding
from typing import List

E = 0
X = None

DUMP_VISUAL_PATHS = True

TEST_MAP1 = [
    [E, E, E, E, E],
    [E, E, E, E, E],
    [X, X, X, X, X],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
]

TEST_MAP2 = [
    [E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E],
    [E, E, E, E, E, E, E, E, E, E],
]

TEST_MAP3 = [
    [E, E, X, E, E, E, E, E, E, E],
    [E, E, X, E, X, X, X, X, X, X],
    [E, E, X, E, X, E, E, E, E, E],
    [E, E, X, E, X, E, X, X, X, E],
    [E, E, X, E, X, E, E, E, X, E],
    [E, E, X, E, X, X, X, E, X, E],
    [E, E, X, E, E, E, X, E, X, E],
    [E, E, X, E, E, E, E, E, X, E],
    [E, E, X, X, X, X, X, X, X, E],
    [E, E, E, E, E, E, E, E, E, E],
]

TEST_MAP4 = [
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
    [E, E, E, E, E],
]

TEST_MAPS = [TEST_MAP1, TEST_MAP2, TEST_MAP3, TEST_MAP4]


def visualize_path(path, map, start, end) -> str:
    result = ""

    width = 0
    height = len(map)
    if height > 0:
        width = len(map[0])

    for y in range(height - 1, -1, -1):
        for x in range(width):
            if [x, y] == start:
                result += 'S'
            elif [x, y] == end:
                result += 'E'
            elif [x, y] in path:
                result += '■'
            elif map[height - y - 1][x] == None:
                result += 'X'
            else:
                result += '0'

        result += '\n'

    return result


def transpose(map: List[List[int]]) -> List[List[int]]:
    height = len(map)
    width = len(map[0])

    new_map: List[List[int]] = []

    for x in range(width):
        new_map.append([])
        for y in range(height):
            new_map[x].append(map[height - y - 1][x])

    return new_map


def get_path_cost(path, map) -> int:
    cost_sum = 0
    for coord in path:
        if map[coord[0]][coord[1]] != None:
            cost_sum += map[coord[0]][coord[1]]

    return cost_sum


def test_function(func):
    for i, test_map in enumerate(TEST_MAPS):
        transposed_map = transpose(test_map)
        a = func(transposed_map)

        start = [0, 0]
        end = [len(transposed_map) - 1, len(transposed_map[0]) - 1]

        print("|-----Test #" + str(i + 1) + "-----")
        print("Start: " + str(start) + " | End: " + str(end))

        path = a.find_path(start, end)

        print("Length: " + str(len(path) - 1) +
              " | Cost: " + str(get_path_cost(path, transposed_map)))

        if DUMP_VISUAL_PATHS:
            if path:
                print("Path: " + str(path))
                result = visualize_path(path, test_map, start, end)
                print(result)
            else:
                print("Path: Does not exist\n")


def main():
    print("|----------ASTAR----------|")
    test_function(simple_pathfinding.Astar)

    print("|----------DIJKSTRA----------|")
    test_function(simple_pathfinding.Dijkstra)

    print("|----------BREADTH FIRST----------|")
    test_function(simple_pathfinding.BreadthFirst)

    return 0


if __name__ == "__main__":
    main()
