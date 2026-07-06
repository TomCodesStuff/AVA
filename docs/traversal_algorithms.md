## Traversal Algorithms:

This table below shows the traversal algorithms visualised by AVA. <br>
For each algorithm, instructional steps are provided which can be followed to produce working implementations.

---

| Algorithm                                     |
| --------------------------------------------- |
| [Breadth First Search](#bogo-sort)            |
| [Depth First Sort](#brick-sort)               | 
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

Time complexity: O(log n)<br>
Space Complexity: O(1)



<!-- Listen to Dry your eyes by The Streets  -->
