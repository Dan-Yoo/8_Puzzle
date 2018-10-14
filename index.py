import sys
from puzzle import Puzzle

size_x = 4
size_y = 3
state = []

if len(sys.argv) != 13:
    print("Puzzle is not a 3x4")
    sys.exit()

for i in range(1, len(sys.argv)):
    state.append(int(sys.argv[i]))

# check if all unique integers between 0 and 11

puzzle = Puzzle(size_x, size_y, state)

print("Which search algorithm to use ?")
print("0 - Depth First Search")
print("1 - Best First Search")
print("2 - A* Algorithm")

search = int(input())

if search > 2 or search < 0:
    print("Wrong selection")
    sys.exit()

# run DFS
if search == 0:
    puzzle.DFS()
    puzzle.generateSolution("puzzleDFS")

# Pick heuristic
print("Pick heuristic A or B")
heuristic_choice = input()

# run best first search
if search == 1:
    if heuristic_choice == 'A':
        puzzle.BFS(puzzle.heuristicA)
        puzzle.generateSolution("puzzleBFS-h1")
    else:
        puzzle.BFS(puzzle.heuristicB)
        puzzle.generateSolution("puzzleBFS-h2")

# run a* algorithm
if search == 2:
    if heuristic_choice == 'A':
        puzzle.Astar(puzzle.heuristicA)
        puzzle.generateSolution("puzzleAs-h1")
    else:
        puzzle.Astar(puzzle.heuristicB)
        puzzle.generateSolution("puzzleAs-h2")