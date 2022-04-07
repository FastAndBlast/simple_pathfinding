# simple_pathfinding

A simple pathfinding library for python, featuring astar, dijkstra and breadth-first search for 2 dimensional maps.

## How to use

### Instantiating the pathfinder

#### Dijkstra

```python
pathfinder = Dijkstra(input_map)
```

#### Astar

```python
pathfinder = Astar(input_map)
```

#### Breadth First Search

```python
pathfinder = BreadthFirst(input_map)
```

### Input map

The input map is expected to be of type `List[List[int]]` denoting the cost of each tile. `None` should be used to denote walls which cannot be passed through. The map is accessed by `map[x][y]` and the returned path is in the same coordinate structure.

### Finding path

To find path use the `pathfinder.find_path(start, end)` method. The `start` and `end` arguments are expected to be of `Tuple(Int, Int)` type, where `start` is considered the starting coordinates and `end` is considered the end coordinates.

The returned path is of type `List[Tuple(Int)]` and returns a list of coordinates which denotes the shortest path in order from `start` to `end`

#### Example

```python
path = pathfinder.find_path((0, 0), (9, 9))
```

## Algorithms

### Dijkstra

Dijkstra searches through nodes in the order of their current cost to reach them from the start node

### Astar

Astar is based on djikstra and searches through nodes in the order of their expected total distance. This is calculated through the current cost to reach the node + the eucledian distance from the node to the end node.

### Breadth First Search

Breadth First Search does not consider cost of a node but instead searches the closest tiles to the current node. This is not guranteed to return the shortest path in an input map with different node costs.
