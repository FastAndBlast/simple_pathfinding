import simple_pathfinding


def main():
    '''
    Simple example of how to use the simple_pathfinding module

    Creates a small map with a wall and prints the cost and length of the shortest path using astar pathfinding
    '''
    input_map = []

    width = 10
    height = 10

    # Making an empty map
    for x in range(width):
        input_map.append([])
        for y in range(height):
            input_map[x].append(1)

    # Making a wall
    for x in range(2, 8):
        input_map[x][3] = None

    # Initialise the pathfinder
    astar = simple_pathfinding.Astar(input_map)

    # Find path from bottom left corner of the map to the top right corner
    path = astar.find_path((0, 0), (width - 1, height - 1))

    # Find the total cost of the path
    cost_sum = 0
    for node in path:
        cost_sum += input_map[node[0]][node[1]]

    # Find the total length of the path in nodes
    length = len(path)

    print("Shortest path: Cost " + str(cost_sum) + " | Length " + str(length))

    return 0


if __name__ == "__main__":
    main()
