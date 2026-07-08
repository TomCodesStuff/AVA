## Traversal Algorithms:

This table below shows the traversal algorithms visualised by AVA. <br>
For each algorithm, instructional steps are provided which can be followed to produce working implementations.

---

| Algorithm                                                 |
| --------------------------------------------------------- |
| [Breadth First Search](#breadth-first-search)             |
| [Depth First Sort](#depth-first-search)                   | 
| [Dijkstra's Shortest Path](#dijkstras-shortest-path)      |
| [Random Walk](#random-walk)                               |

---
### Breadth First Search: 

#### Algorithm Steps:

1. Set variable `queue = [startNode]`.
2. Set variable `nodesVisited = []`
3. Set variable `goalFound = False`
4. While `queue.isNotEmpty()` and `not goalFound`
5. Set `currentNode = queue.removeAt(0)` (Remove first element from the queue) 
6. `nodesVisited.append(currentNode)` (Mark node as visited)
7. For each `neighbour` of `currentNode`
8. If `neighbour not in nodesVisited` and `neighbour not in queue`: <br>
    \- `queue.append(neighbour)` (Add neighbour to queue)
9. If `currentNode` = `goalNode` <br>
    \- Set `goalFound = True`

#### Time-Space Complexities: 

Time complexity: O(V + E)<br>
Space Complexity: O(V)

V -> Number of nodes <br>
E -> Number egdes 

---
### Depth First Search: 

#### Algorithm Steps:

1. Set variable `stack = [startNode]`.
2. Set variable `nodesVisited = []`
3. Set variable `goalFound = False`
4. While `stack.isNotEmpty()` and `not goalFound`
5. Set `currentNode = stack.pop()` (Remove last element from the stack) 
6. `nodesVisited.append(currentNode)` (Mark node as visited)
7. For each `neighbour` of `currentNode`
8. If `neighbour not in nodesVisited` and `neighbour not in stack`: <br>
    \- `stack.append(neighbour)` (Add neighbour to queue)
9. If `currentNode` = `goalNode` <br>
    \- Set `goalFound = True`

#### Time-Space Complexities: 

Time complexity: O(V + E)<br>
Space Complexity: O(V)

V -> Number of nodes <br>
E -> Number egdes 

--- 
### Dijkstra's Shortest Path: 

#### Algorithm Steps:

1. Set variable `unvisitedNodes = {node : 0 if node = startNode else infinity for each node}`.
2. Set variable `visitedNodes = set()`.
3. while `unvisitedNodes` is not empty and there is an unvisited node with a distance less than infinity. 
4. Set variable `currentNode = unvisited node with smallest distance`
5. Set variable `currentNodeCost = unvisitedNodes[currentNode]` 
6. `visitedNodes.add(currentNode)` (Mark the current node as visited).  
7. `unvisitedNodes.delete(currentNode)` (Remove current nodes from unvisisted nodes)
8. for each `neighbour` in `currentNode`
9. if not `visitedNodes.contains(neighbour)` and `currentNodeCost + neighbour.getCost(currentNode) < unvisitedNodes[neighbour]`: <br>
    \- `unvisitedNodes[neighbour] = currentNodeCost + neighbour.getCost(currentNode)`


#### Time-Space Complexities: 

Time complexity: O(V<sup>2</sup> + E)<br>
Space Complexity: O(V)

V -> Number of nodes <br>
E -> Number egdes 

#### A Note On Time Complexity

A time complexity of O((V + E) log V) can be achieved if a heap is used to store unvisisted nodes as the root will contain the node with the shortest distance 

---
### Random Walk: 

#### Algorithm Steps:

1. Set variable `visitedNodes = set()`
2. Set variable `currentNode = startNode`
3. Set variable `goalFound = False`
4. while `currentNode` and `not goalFound`
5. `visitedNodes.add(currentNode)` (Mark node as visited)
6. if `neighbours` is not empty: <br>
    \- `currentNode = randomly select neighbour that is not in visitedNodes`
7. else: <br>
    \- `currentNode = None`
8. if `currentNode == goalNode`: <br>
    \- Set variable `goalFound = True`

#### Time-Space Complexities: 

Time complexity: O(V + E)<br>
Space Complexity: O(V)

V -> Number of nodes <br>
E -> Number egdes 

#### Note:

This algorithm is an avoidant random walk to prevent the algorithm from executing indefinitely in cases <br> 
where the goal node is unreachable. A true random walk would not have a visited nodes set and would continue <br> 
randomly selecting nodes until finding the goal node is found.  

---
### Uniform Cost Search: 

#### Algorithm Steps:

1. Set variable `visitedNodes = set()`
2. Set variable `frontier = {startNode : 0}`
3. Set variable `goalFound = False`   
4. While `frontier.isNotEmpty()` and `not goalFound`
5. Set variable `currentNode = frontier.getLowestCostNode()`
6. `visitedNodes.add(currentNode)` (Mark the current node as visited).  
7. for each `neighbour` of `currentNode`
8. Set Variable `totalCost = frontier[currentNode] + neighbour.getWeight()`
9. if `neighbour not in visitedNodes` and `totalCost < frontier.get(neighbour, infinity)`: <br>
    \- Set `frontier[neighbour] = totalCost`
10. `frontier.delete(currentNode)` (Remove current nodes from frontier)
11. if `currentNode = goalNode`: <br> 
    \- Set `goalFound = True`


#### Time-Space Complexities: 

Time complexity: O(V<sup>2</sup> + E)<br>
Space Complexity: O(V)

V -> Number of nodes <br>
E -> Number egdes 

#### A Note On Time Complexity

A time complexity of O((V + E) log V) can be achieved if a heap is used to store unvisisted nodes, <br> 
as the root will contain the node with the smallest cost.

---
Go to [README.md](../README.md)

<!-- Listen to Dry your eyes by The Streets  -->
