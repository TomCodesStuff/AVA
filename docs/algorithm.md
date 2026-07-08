# Array Class Documentation 

Below are the helper functions provided by the `Algorithm` base class. 


| Function:           | Parameters:                   | Return Value:                          | Description:                                                                                                                                   | 
| --------------------| ----------------------------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| getName             |                               | A string                               | Abstract method. Returns the name of the algorithm which will be displayed to users.                                                           |
| run                 |                               | An Integer                             | Abstract method. Called by AVA to execute an algorithm. <br> Should contain the algorithms implementation. <br> Returning 0 indicates success. |
| getDataStructure    |                               | A DataStructure object                 | Returns the data structure the algorithm interfaces with.                                                                                      |
| setDataStructure    | dataStructure : DataStructure |                                        | Assigns the data structure if it has not been already.                                                                                         |
| setMediator         | mediator : Mediator           |                                        | Assigns the mediator if it has not been already.                                                                                               |
| briefTick           |                               |                                        | Halts algorithm execution for half a second (500 ms).                                                                                          |
| tick                |                               |                                        | Halts algorithm execution for amount defined by the user.                                                                                      |


---

Go to [README.md](../README.md)

<!-- Listen to And I love her by The Beatles -->
