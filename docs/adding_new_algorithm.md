# Adding A New Algorithm. 

| Table Of Contents                                         |
| --------------------------------------------------------- |
| [1. File Formatting](#1-file-formatting)                  |
| [2. Class Formatting](#2-class-formatting)                |
| [3. Algorithm Parent Class](#3-algorithm-parent-class)    |
| [4. Method Implementation](#4-method-implementation)      |
| [5. Data Structure Class](#5-data-structure-class)        | 

## 1. File Formatting

When creating a new algorithm file, it must be found in the correct directory and follow the specified naming convention to be recognised.  

### 1.1 File Location 

The directory the new algorithm must be found will differ per algorithm type and are listed below:

- Searching Algorithms -> <b> /algorithms/searching/ </b> <br>
- Sorting Algorithms -> <b> /algorithms/sorting/ </b> <br>
- Tarversal Algorithms -> <b> /algorithms/traversal/ </b> 

### 1.2 File Name 

New algorithm files must follow the naming convention as defined by algorithm type:

- Searching Algorithms -> <b> algorithm_name_search.py. </b> <br>
    \- (e.g. linear_search.py, binary_search.py, etc.) 
- Sorting Algorithms -> <b> algorithm_name_sort.py. </b> <br> 
    \- (e.g. bubble_sort.py, insertion_sort.py, etc.) 
- Traversal Algorithms -> <b> algorithm_name_traverse.py. </b> <br> 
    \- (e.g. dijkstra_traverse.py, depth_first_search.py, etc.) 


## 2. Class Formatting 

This project follows the Object Oriented Programming Paradigm. <br>
As such new algorithms must be implemented as a class. 

### 2.1 Class Naming 

New algorithm classes must follow the class naming convention as defined by algorithm type:

- Searching Algorithms -> <b> AlgorithmNameSearch. </b> <br>
    \- (e.g. LinearSearch, BinarySearch, etc.) 
- Sorting Algorithms -> <b> AlgorithmNameSort. </b> <br> 
    \- (e.g. BubbleSort, InsertionSort, etc.)   
- Traversal Algorithms -> <b> AlgorithmNameTraverse. </b> <br> 
    \- (e.g. DijkstraTraverse, DepthFirstTraverse, etc.)   


## 3. Algorithm Parent Class. 

Each new algorithm class must inherit from the `Algorithm` parent class. <br>
The `Algorithm` class provides several helper methods required for each algorithm 
to interface correctly with the project. <br>
Documentation for the `Algorithm` class can be found [here](./algorithm.md).  

Once the `Algorithm` class has correctly been imported and inherited, it's constructor must be called. 
The steps for importing, inheriting and calling the constructor are outlined below via code snippet.


### 3.1 Importing The Algorithm Class 

```python 
from algorithms import Algorithm 
```
<i> Import statement needed to use the Algorithm parent class </i>

### 3.2 Inheriting The Algorithm Class

```python 
class BogoSort(Algorithm):
```
<i> Inheriting the Algorithm parent class correctly. <br> 
BogoSort is used as an example here. </i>

### 3.3 Constructor 

```python 
def __init__(self):
    super().__init__()
```
<i> Correct implementation of the constructor. </i>

## 4. Method Implementation 

The project executes algorithms by calling the `run()` method. <br>
Therefore, new algorithms must implement the `run()` method in order to be recognised by the project. <br>
If a new algorithm succesfully inherits from the `Algorithm` base class, this method is defined as abstract. <br> 
As such the algorithm class can not be instantiated until the `run()` method is implemented. <br>


Another abstract method is defined in the `Algorithm` class which is `getName()`. <br>
The string returned by the `getName()` method is what AVA displays to the user during algorithm selection. <br>
As with the `run()` method if `getName*()` is not defined the algorithm class can not be instantiated.   

The Code Snippets to create the `run()` and `getName()` methods are provided below.

### 4.1 Creating The run() Method 
```python 
def run(self) -> int:
    return 0
```

<i> Correctly creating the `run()` method. </i>

### 4.2 Creating The getName() Method 
```python 
def getName(self) -> str:
    return "Bogo Sort"
```

<i> Correctly creating the `getName()` method. Bogo Sort is once again used as an example </i>

## 5. Delaying Execution. 

Delays need to invoked frequently during the execution of an algorithm as it allows for users to see each step of an algorithm. <br> 
Without these delays the algorithms would finish too quickly and any updates to the GUI will be too fast to see.

There are two dedicated methods to invoke a delay which are outlined below:

```python 
    self.tick()
    self.briefTick()
```

<i> Provided tick methods used to delay algorithm execution. </i> 

The amount of time algorithms are delayed for when calling `self.tick()` is defined by the users during runtime. <br>
The delay caused by calling `self.briefTick()` is half a second (500 ms). 


## 6. Data Structure Class. 

Algorithms interact with the project through a data structure class. <br> 
The data structure class and its helper methods differ depending on the algorithm type. <br>
The specific data structure for each algorithm type are outlined below:

- Searching Algorithms -> <b> [Search Array.](./search_array.md) </b> <br> 
- Sorting Algorithms -> <b> [Sort Array.](./sort_array.md) </b> 
- Traversal Algorithms -> <b> [Graph.](./graph.md) </b> 

---

Go to [README.md](../README.md)

<!-- Listen to Linger by The Cranberries -->
