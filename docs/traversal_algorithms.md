## Traversal Algorithms:

This table below shows the traversal algorithms visualised by AVA. <br>
For each algorithm, instructional steps are provided which can be followed to produce working implementations.

---

| Algorithm                                     |
| --------------------------------------------- |
| [Breadth First Search](#breadth-first-search) |
| [Depth First Sort](#depth-first-search)       | 
| [Dijkstra's Shortest Path](#bubble-sort)      |


---
### Breadth First Search: 

#### Algorithm Steps:

1. Set variable `queue = [startNode]`.
2. Set variable `nodesVisited = []`
3. While queue is not empty and goal node has not been found
4. Set `currentNode = queue.removeAt(0)` (Remove first element from the queue) 
5. `nodesVisited.append(currentNode)` (Mark node as visited)
6. For each neighbour of `currentNode`
7. If neighbour is not in `nodesVisited` and neighbour is not in `queue`
8. `queue.append(neighbour)` (Add neighbour to queue)

#### Time-Space Complexities: 

Time complexity: O(V + E)<br>
Space Complexity: O(V)

V -> Number of nodes <br>
E -> Number egdes 

### Depth First Search: 

#### Algorithm Steps:

1. Set variable `stack = [startNode]`.
2. Set variable `nodesVisited = []`
3. While stack is not empty and goal node has not been found
4. Set `currentNode = stack.pop()` (Remove last element from the stack) 
5. `nodesVisited.append(currentNode)` (Mark node as visited)
6. For each neighbour of `currentNode`
7. If neighbour is not in `nodesVisited` and neighbour is not in `stack`
8. `stack.append(neighbour)` (Add neighbour to queue)

#### Time-Space Complexities: 

Time complexity: O(V + E)<br>
Space Complexity: O(V)

V -> Number of nodes <br>
E -> Number egdes 



<!-- Listen to Dry your eyes by The Streets  -->
