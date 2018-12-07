# **movit**

Small project to find the solution to the puzzle outlined below. The  solution involves moving pieces around the board 
and eventually moving ```b``` through ​```Z```​ in as few moves as possible.

Once solved, it shows the moves from initial state to the final state in the optimal solution.

### The puzzle:

To solve the puzzle, you must move the pieces around the board and move b out of the exit ```Z```.

The rules are:

* A piece may only move vertically or horizontally into empty space next to it. (example moves are illustrated below)
* If there are 2 empty spaces in given direction, the given piece may move 1 or 2 spaces (counting as 1 move)
* Pieces may not occupy the space Z.
* The piece b may move through Z solving the problem.
* A piece can not overlap with another piece.
* There are always 2 empty spaces on the board.

The following is a visualisation of the pieces with the board in the initial state :
```
XXXXXX
XabbcX
XabbcX
XdeefX
XdghfX
Xi  jX
XXZZXX
```
X is a border, and Z is a gap through which the main piece b can move.

## Requirements
**movit** requires you have [Python3](https://www.python.org/downloads/) and [pip](https://pypi.org/project/pip/) installed.

Other required packages are downloaded during installation.

## Installation
To install **movit**:

```
$ git clone https://github.com/callumski/movit.git
$ cd movit
$ make setup
```
This will:

* download the git repository
* cd into the folder
* run a ```make``` command that creates a virtualenv and installs are the required dependencies

For convenience there is also:

```
$ make all
```
Which will setup **movit** and run the tests.

N.B. Running  ```make all``` also runs ```make clean``` which will remove the virtualenv and any Python bytecode files.


## Running the tests
The tests are written using [pytest](https://pytest.org). To run them:

```
$ make test
```
N.B. **movir** has been tested with Python 3 on OSX High Sierra.

## Usage
In addition to running the tests there are some other make targets for your convenience.
To attempt to solve the problem you can:

```
$ make run
```

This will run **movit** against the board shown in these instructions.

You can also:

```
$ make run-json:
```
To output in [JSON Lines](http://jsonlines.org/) format.

```
$ make run-profile:
```
To run with Python's cProlife library.

```
$ make run-ten:
```
To find the first 10 solutions.
```
$ make run-ten-json:
```
To find the first 10 solutions and output the in [JSON Lines](http://jsonlines.org/) format.

```
$ make run-ten-profile:
```
To find the first 10 solutions and run with Python's cProlife library.

```
$ make run-all:
```
To search for all solutions.
```
$ make run-all-profile:
```
To search for all solutions and run with Python's cProlife library.

You can also call the **movit** Python module directly from the command line:

```
$ python3 movit/movit.py --help
usage: movit.py [-h] [--find-all FIND_ALL] [--find-n FIND_N]
                [--json-output JSON_OUTPUT]
                [file]

movit.py: Finds solutions to a board problem.

positional arguments:
  file                  full path to JSON file of board setup

optional arguments:
  -h, --help            show this help message and exit
  --find-all FIND_ALL   find all possible solutions
  --find-n FIND_N       find N solutions: default is 1
  --json-output JSON_OUTPUT
                        output solutions as JSON Lines see:
                        http://jsonlines.org/
```


## Approach taken

This project does not use any special libraries. It is built to do a Breadth First Search to find the solution. This means 
that it is guaranteed to find the the shortest solution first. This property means it is same to dun **movit** in it's 
defailt mode with confidence.

I tried a number of different strategies to improve performance, porting in those changes that seemed to work. I did not make
a comprehensive study of potential performance improvements. I think there is still room for many performance enhancements.

[JSON Lines](http://jsonlines.org/) was chosen as an output format as it will generate a valid JSON file, even if the 
search is stopped part way. It also means that the output can be parsed in a memory efficient way if necessary.


###Assmuptions:

* The 2 blank spots rule does not apply on exit
* It is always a ```b``` piece that is the be removed from the board.
* All pieces will have names that are lower-case ascii. Any letter from ```a-z``` will do. Double-letter names should also work.
* No assumptions have been made about board size or shape, other than all rows have the same length and all columns have same length. (i.e. the board is rectangular).


## Possible extensions:

The following extensions are possible:

* More tests for the display
* Validation of functionality on other operating systems
* Giving it an end-to-end HTML UI to allow it to be deployed as a web application
* Deploying in a Docker container
* Improving the Board handling as it is quite ineffiecient
* Refactoring to a simpler structure
