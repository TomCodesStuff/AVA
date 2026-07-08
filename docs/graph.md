# Graph Class Documentation 

The `Graph` class depends on the [`Node`](#node-class-documentation) and [`Edge`](#edge-class-documentation) classes to fucntion. <br> 
Documentation for these classes can be found within this markdown document also. <br>. 
Below are the helper functions provided by the `Graph` class. <br>

| Function:      | Parameters: | Return Values:           | Description:                                                                                                        | 
| -------------- | ----------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------- | 
| addNode        | node : Node |                          | Adds a Node object to the graph.                                                                                    |
| removeNode     | node : Node |                          | Remove a Node object from the graph.                                                                                |
| get            |             | An array of Node objects | Returns all Node objects currently in the graph.                                                                    |
| size           |             | An Integer               | Returns the number of nodes in the graph.                                                                           |
| getStartNode   |             | A Node object or None    | Returns the Node object designated as the start node. <br> If no start node has been assigned, None is returned.    |
| setStartNode   | node : Node |                          | Assigns the passed Node object to be the goal node.                                                                 |
| getGoaltNode   |             | A Node object or None    | Returns the Node object designated as the goal node. <br> If no goal node has been assigned, None is returned       |
| setGoaltNode   | node : Node |                          | Assigns the passed Node object to be the goal node.                                                                 |
| resetColours   |             |                          | Sets each Node and Edge objects colour to the default.                                                              |
| reconstuctPath |             | An array of Node objects | Returns the path found after an algorithm is run. <br> If no route was found an empty list is returned.             |
| printRoute     |             |                          | Prints the route found after an algorithm is run to the terminal. <br> If no route was found "No route" is printed. |
                                     

---

# Node Class Documentation 

Below are the helper functions provided by the `Node` class. <br>

| Function:         | Parameters:                              | Return Values:            | Description:                                                                                         | 
| ----------------- | ---------------------------------------- | ------------------------- | ---------------------------------------------------------------------------------------------------- | 
| getColour         |                                          | A string                  | Returns the colour which will be displayed on screen.                                                |
| setColour         | colour : str                             |                           | Set the colour that will be displayed on screen to the passed value.                                 |
| resetColour       |                                          |                           | Reset the nodes colour back to the default.                                                          |
| getBaseColour     |                                          |                           | Get the colour used when `resetColour` is called.                                                    |
| setBaseColour     | colour : str                             |                           | Set the colour used when `resetColour` is called to the specified value.                             |
| getEdgeColour     | neighbourNode : Node                     |                           | Gets the colour of the edge connecting the passed neighobur node.                                    |
| setEdgeColour     | neighbourNode : Node <br> colour : str   |                           | Sets the colour of the edge connecting the passed neighobur node to the specified colour.            |
| resetEdgeColour   | neighbourNode : Node                     |                           | Reset the colour of the edge connecting the passed neighbour node to the default.                    |
| getNeighbours     |                                          | An array of tuples.       | Each tuple contains a Node object and the weight/cost to get to the node.                            |
| addEdge           | edge : Edge                              |                           | Adds the passed Edge object to the Node.                                                             |
| removeEdge        | edge : Edge                              |                           | Removes the passed Edge object from the Node.                                                        |
| getPrevNode       |                                          | A Node object or None     | Returns the predecessor Node in the current path. <br> If there is no predecessor, None is returned. |
| setPrevNode       | node : Node                              |                           | Sets the predecessor Node in the current path.                                                       |
| getHeuristicValue |                                          | An Integer                | Returns the euclidian distance from the goal node.                                                   |
| setHeuristicValue | value : int                              |                           | Sets the heuristic to the passed value.                                                              |


---

# Edge Class Documentation 

Below are the helper functions provided by the `Edge` class. <br>


| Function:         | Parameters:                              | Return Values:            | Description:                                                          | 
| ----------------- | ---------------------------------------- | ------------------------- | --------------------------------------------------------------------- |
| getWeight         |                                          | An Integer                | Returns the weight/cost assigned to the Edge object.                  |
| setWeight         | weight : int                             |                           | Assigns the weight/cost of the Edge object to the passed value.       |
| getColour         |                                          | A String                  | Returns the colour which will be displayed on screen.                 |
| setColour         | colour : str                             |                           | Sets the colour that will be displayed on screen to the passed value. |
| getDirection      |                                          | An Enum                   | Returns the Enum asscoiated with the direction.                       |
| setDirection      | direction : Enum                         |                           | Sets the Edge objects direction to the passed Enum.                   |
| getNeighbourNode  | node : Node                              |                           | Return the node that is connected by the edge to the passed node.     |
| setFirstNode      | node : Node                              |                           | Assign the firt node the edge connects to the passed Node object.     |
| setSecondNode     | node : Node                              |                           | Assign the second node the edge connects to the passed Node object.   |
| resetColour       |                                          |                           | Resets the Edge objects colour to thedefault.                         |



---
Go to [README.md](../README.md)

<!-- Listen to Zombie by The Cranberries  -->
