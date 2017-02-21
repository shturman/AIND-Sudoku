# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Naked Twins is an additional heuristic strategy in reducing the number of possible board configurations. The tenet of this strategy is: inside the unit it is not possible to have options from naked twins boxes (because 2 numbers are stuck inside them) somewhere else except these 2 boxes. So in case we found twins inside the unit we can remove these 2 options from the rest of the unit. It is significantly decrease the number of configurations to check before solution found.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Diagonal sudoku problem adds 2 additional rules (constraints) to existing one: inside each from 2 main diagonals (A1-I9, I1-A9) the numbers 1 to 9 should all appear exactly once. In our case we just need to add 2 additional units (diagonals) to existing ones due to the same rule is applicable to all of them. The more constraints we have, the more possible ways to apply our strategies (only choice/naked twins/etc).

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.