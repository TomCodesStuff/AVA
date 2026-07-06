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
3. While queue is not empty and goal node has not been found
4. Set `currentNode = queue.removeAt(0)` (Remove first element from the queue) 
5. `nodesVisited.append(currentNode)` (Mark node as visited)
6. For each neighbour of `currentNode`
7. If neighbour is not in `nodesVisited` and neighbour is not in `queue`: <br>
    \-`queue.append(neighbour)` (Add neighbour to queue)

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
3. While stack is not empty and goal node has not been found
4. Set `currentNode = stack.pop()` (Remove last element from the stack) 
5. `nodesVisited.append(currentNode)` (Mark node as visited)
6. For each neighbour of `currentNode`
7. If neighbour is not in `nodesVisited` and neighbour is not in `stack`: <br>
    \-`stack.append(neighbour)` (Add neighbour to queue)

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
4. Set variable `currentNode` = unvisited node with smallest distance
5. Set variable `currentNodeCost` = unvisitedNodes[`currentNode`] 
6. `visitedNodes.add(currentNode)` (Mark the current node as visited).  
7. `unvisitedNodes.delete(currentNode)` (Remove current nodes from unvisisted nodes)
8. for each `neighbour` in `currentNode`
9. if not `visitedNodes.contains(neighbour)` and `currentNodeCost + neighbour.getCost(currentNode) < unvisitedNodes[neighbour]`: <br>
    \- `unvisitedNodes[neighbour] = currentNodeCost + neighbour.getCost(currentNode)`


#### Time-Space Complexities: 

Time complexity: O((V + E) log V)<br>
Space Complexity: O(V)

V -> Number of nodes <br>
E -> Number egdes 

---
### Random Walk: 

#### Algorithm Steps:

1. Set variable `visitedNodes = set()`
2. Set variable `currentNode = startNode`
2. Set variable `goalFound = False`
3. while `currentNode` and `not goalFound`
4. `visitedNodes.add(currentNode)` (Mark node as visited)
5. if `neighbours` is not empty: <br>
    \- `currentNode = randomly select neighbour that is not in visitedNodes`
6. else: <br>
    \- `currentNode = None`
7. if `currentNode == goalNode`: <br>
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
Go to [README.md](../README.md)

<!-- Listen to Dry your eyes by The Streets  -->
