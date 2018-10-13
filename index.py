from puzzle import Puzzle

# read input
size_x = 4
size_y = 3
# input = [1,2,0,4,5,6,7,3,9,10,11,8]
input = [0,6,11,7,3,2,10,8,1,5,4,9]

# faster input
# size_x = 3
# size_y = 3
# input = [1,2,3,4,0,6,7,8,5]

#fasstest input
# size_x = 3
# size_y = 2
# input = [1,0,2,4,5,3]

# validate input

# init the puzle
puzzle = Puzzle(size_x, size_y, input)

# BFS with heuristic A
# puzzle.BFS(puzzle.heuristicA)
puzzle.Astar(puzzle.heuristicA)
puzzle.generateSolution("A_star")