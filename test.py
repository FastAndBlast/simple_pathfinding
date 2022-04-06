from pathfinding import *


test1 = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [9, 9, 9, 9, 9],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

test2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

test3 = [
    [0, 0, 9, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 9, 0, 9, 9, 9, 9, 9, 9],
    [0, 0, 9, 0, 9, 0, 0, 0, 0, 0],
    [0, 0, 9, 0, 9, 0, 9, 9, 9, 0],
    [0, 0, 9, 0, 9, 0, 0, 0, 9, 0],
    [0, 0, 9, 0, 9, 9, 9, 0, 9, 0],
    [0, 0, 9, 0, 0, 0, 9, 0, 9, 0],
    [0, 0, 9, 0, 0, 0, 0, 0, 9, 0],
    [0, 0, 9, 9, 9, 9, 9, 9, 9, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

test4 = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

tests = [test1, test2, test3, test4]

for test in tests:
    for x in range(len(test)):
        for y in range(len(test[0])):
            if test[x][y] == 9:
                test[x][y] = None


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
                result += '1'
            elif map[height - y - 1][x] == None:
                result += '#'
            else:
                result += '0'

        result += '\n'

    return result


def main():
    i = 1
    for test in tests:
        a = astar(test)

        start = [0, 0]
        end = [len(test[0]) - 1, len(test) - 1]

        # print(a)
        print("Test #" + str(i))  # + " | " + a.name)
        print("Start: " + str(start) + " | End: " + str(end))

        path = a.get_path(start, end)

        print("Path: " + str(path))

        result = visualize_path(path, test, start, end)

        print(result)

        print("-----------")

        i += 1

    return 0


main()
