## Sorting Algorithms:

This table below shows the searching algorithms visualised by AVA. <br>
For each algorithm, instructional steps are provided which can be followed to produce working implementations.

Two helper functions `isSwapNeeded()` and `swap()` are defined which represent fundamental operations performed by each algorithm. <br> 
The specifics of their implementation are left to the reader.  

---

| Algorithm                                     |
| --------------------------------------------- |
| [Bogo Sort](#bogo-sort)                       |
| [Brick Sort](#brick-sort)                     | 
| [Bubble Sort](#bubble-sort)                   |
| [Cocktail Shaker Sort](#cocktail-shaker-sort) |
| [Gnome Sort](#gnome-sort)                     |
| [Insertion Sort](#insertion-sort)             |
| [Merge Sort](#merge-sort)                     |
| [Quick Sort](#quick-sort)                     |
| [Selection Sort](#selection-sort)             |
| [Tim Sort](#tim-sort)                         |

---
### Bogo Sort:

#### Algorithm Steps: 

1. While array is not sorted:
2. Randomly shuffle array 
3. If array is sorted: <br> 
    \- Stop Algorithm.
4. End While. 

#### Time-Space Complexities: 

Time Complexity: O((n + 1)!)<br>
Space Complexity: O(1)

---
### Brick Sort 

#### Algorithm steps:

1. Set a variable `swapped = True`  
2. While swapped is True: 
3. Set `swapped = False` 
4. for i in range(1, array.length() - 1, 2) 
5. If isSwapNeeded(array[i], array[i + 1]): <br>
    \- swap(array[i], array[i + 1]). <br>
    \- Set `swapped = True `
6.  for i in range(0, array.length() - 1, 2) 
7. If isSwapNeeded(array[i], array[i + 1]): swap(array[i], array[i + 1]). Set `swapped = True`
8. End While Loop.

#### Time-Space Complexities: 

Time Complexity: O(n<sup>2</sup>)<br>
Space Complexity: O(1) 

---
### Bubble Sort:

#### Algorithm steps: 

1. for i in range(0, array.length())
2. Set a variable `swapped = False`
3. for j in range(0, array.length() - i - 1) 
4. if isSwapNeeded(array[j], array[j + 1]): <br>
    \- swap(array[j], array[j + 1]). <br> 
    \- Set `swapped = True`
6. if swapped == False: Array is sorted, return 0
7. End For Loop.

#### Time-Space Complexities: 

Time Complexity: O(n<sup>2</sup>) <br>
Space Complexity: O(1)

#### End of unsorted array formula: 

$$ index = n - i - 1$$

n -> length of the array <br>
i -> index of current element 

---
### Cocktail Shaker Sort 

#### Algorithm steps:

1. Set a variable `swapped = True` 
2. While swapped = True: 
3. Set `swapped = False`
4. for i in range(0, array.length() - 1)
5. If isSwapNeeded(array[i], array[i + 1]): <br>
    \- swap(array[i], array[i + 1]). <br> 
    \- Set `swapped = True`
6. If swapped = False. Array is sorted, return 0. 
7. for i in range(array.length() - 1, 1)
8. If isSwapNeeded(array[i], array[i - 1]): <br>
    \- swap(array[i], array[i - 1]). <br>
    \- Set `swapped = True`
9. If swapped = False. Array is sorted, return 0. 
10. End While Loop. 

#### Time-Space Complexities: 

Time Complexity: O(n<sup>2</sup>)<br>
Space Complexity: O(1) 

---
### Gnome Sort 

#### Algorithm steps:

1. Set a variable `pos = 0` 
2. While pos < array.length(): 
3. If pos = 0: `pos = pos + 1` 
4. If isSwapNeeded(array[pos], array[pos - 1]): <br>
    \- swap(array[pos], array[pos - 1]). <br>
    \- Set `pos = pos - 1`
5. Else: Set `pos = pos + 1` 
6. End While Loop. 

#### Time-Space Complexities: 

Time Complexity: O(n<sup>2</sup>)<br>
Space Complexity: O(1) 

---
### Insertion Sort:

#### Algorithm Steps: 

1. for i in range(1, array.length()):
2. Set variable `j = i`
3. while j > 0 AND isSwapNeeded(array[j - 1], array[j]): <br> 
    \- swap(array[j - 1], array[j]).<br> 
    \- Set `j = j - 1`
4. End While Loop. 

#### Time-Space Complexities: 

Time Complexity: O(n<sup>2</sup>)<br>
Space Complexity: O(1)

---
### Merge Sort:

#### Algorithm Steps:

1. Repeatedly split the array into sub-arrays containing only one element 
2. Take pairs of sub-arrays
3. Merge both sub-arrays by comparing elements, creating a new larger sub-array.  
4. Repeat the merging process creating larger sorted sub-arrays 
5. Continue until only one sorted array remains 

#### Time-Space Complexities: 

Time Complexity: O(n log n) <br>
Space Complexity: O(n)


#### A Note On Space Complexity 

An O(1) space complexity can be achieved by merging the sub arrays in-place. 

---
### Quick Sort:

#### Algorithm Steps: 

1. Set a variable `pivot = selectPivot()`
2. All elements < pivot: 
    \- Shifted to the left of the pivot 
3. All elementd > pivot: 
    \- Shifted to the right of the pivot 
4. Repeat the process on the left sub-array (elements to the left of the pivot)
5. Repeat the process on the right sub-array (elements to the right of the pivot)
6. Recurively repeat process until sub-arrays contain only a single element 


#### Time-Space Complexities: 

Time Complexity: O(n log n) <br>
Space Complexity: O(1)  

#### Pivot Selection 

Multiple different methods can be used to determine the pivot. <br> 
This project uses the <b>Median Of Three</b>; an explanation of this method and other pivot selection methods can be found [here.](https://dev.to/pineapples/writing-a-median-of-three-pivot-helper-for-quicksort-289m) 


#### A Note On Time Complexity 

If the pivot is not chosen efficiently, the worst case time complexity becomes O(n<sup>2</sup>)

---
### Selection Sort:

#### Algorithm Steps: 

1. for i in range(0, array.length()): 
2. Set variable `minIdx = i`
3. for j in range(i + 1, array.length()):
4. If isSwapNeeded(minIdx, j): <br>
    \- minIdx = j 
5. Set variable `value = array[minIdx]`
6. Shift all elements between `i` and `minIdx` one place to the right  
7. Set `array[i] = value`
8. End For Loop 
9. End For Loop

#### Time-Space Complexities: 

Time Complexity: O(n<sup>2</sup>)<br>
Space Complexity: O(1)

---
### Tim Sort:

#### Algorithm Steps: 

1. Set variable `runSize = calculateRunSize()`  
2. Perform Insertion Sort on each run 
3. Perform Merge Sort (The starting sub-arrays are the sorted runs). 

#### Time-Space Complexities: 

Time Complexity: O(n log n)<br>
Space Complexity: O(n) 

#### A Note On Space Complexity 

An O(1) space complexity can be achieved by merging the sub arrays in-place. 

#### Run Size Calculation

The official Tim Sort implementation uses run sizes in the range 32 - 64 (inclusive). <br>
For arrays that are smaller than 64 elements only an insertion sort is performed. <br> 
Further details on how run size is officially calculated can be found [here.](https://en.wikipedia.org/wiki/Timsort)

For the purposes of visulisation this project calculates the run size such that the number of runs is approximately <b>16</b>. <br>
For arrays shorter than 16 elements, only insertion sort is performed.

--- 

Go to [README.md](../README.md)

<!-- Listen to Dear Maria, Count Me In by All Time Low  -->
