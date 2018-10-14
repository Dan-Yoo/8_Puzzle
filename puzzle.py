import heapq
import time
import math

class Puzzle:
    current_state = []
    open = []
    closed = {}
    solution_path = {}
    size_x = 0
    size_y = 0
    start_time = 0
    end_time = 0

    def __init__(self, size_x, size_y, state):
        self.size_x = size_x
        self.size_y = size_y
        self.current_state = state
        self.start_time = time.time()

    def DFS(self):
        print("Running depth first search . . .")
        self.open.append(self.current_state)

        while self.open:
            self.current_state = self.open.pop()
            key = tuple(self.current_state)

            # put into close state
            self.closed[key] = 1

            if self.isFinalState():
                return True

            # else, push all its available next states into the open list
            self.pushNextStates()

        print("Couldn't solve the puzzle")
        return False

    def BFS(self, heuristic):
        print("Running best first search . . .")
        heapq.heappush(self.open, (self.heuristicA(self.current_state), self.current_state))

        while self.open:
            # pop current state
            self.current_state = heapq.heappop(self.open)[1]
            
            # put into closed state
            key = tuple(self.current_state)
            self.closed[key] = 1

            # check if final state
            if self.isFinalState():
                return True
            else:
                # push next states 
                self.pushNextStates(heuristic)
            # repeat


        return False

    def Astar(self, heuristic):
        print("Running A* algorithm . . .")
        heapq.heappush(self.open, (self.heuristicA(self.current_state, 0), (-1, self.current_state)))

        while self.open:
            # pop current state
            temp = heapq.heappop(self.open)[1]
            self.current_state = temp[1]
            depth = temp[0] + 1
            
            # put into closed state
            key = tuple(self.current_state)
            self.closed[key] = 1

            # check if final state
            if self.isFinalState():
                return True
            else:
                # push next states 
                self.pushNextStates(heuristic, depth)
            # repeat


        return False

    def pushNextStates(self, heuristic=None, depth=None):
        start_x = -1
        end_x = 1
        start_y = -1
        end_y = 1
        start_index = self.current_state.index(0)

        # if first row
        if start_index <= self.size_x:
            end_y = 0

        # if last row
        if start_index >= (self.size_x * (self.size_y - 1)):
            start_y = 0

        # if first column
        if start_index % self.size_x == 0:
            start_x = 0

        # if last column
        if start_index % self.size_x == self.size_x - 1:
            end_x = 0
    

        # TODO:: how to order these in a clockwise fashion
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if x != 0 or y != 0:
                    # create the new state with the move done
                    new_state = self.current_state.copy()
                    swap_index = start_index + x + -y * self.size_x 
                    self.swap(start_index, swap_index, new_state)

                    # put into open list and also into solution path
                    # check if this state exists in closed
                    if tuple(new_state) not in self.closed:
                        # if heuristic is passed, you need to push a tuple of (h, state)
                        if heuristic is not None and depth is None:
                            heapq.heappush(self.open, (heuristic(new_state), new_state))
                        # if heuristic and depth is passed, you need to push a tuplle of h, (depth, state)
                        elif heuristic is not None and depth is not None:
                            # heap push with new depth
                            heapq.heappush(self.open, (heuristic(new_state, depth), (depth, new_state)))
                        else:
                            self.open.append(new_state)
                        
                        # push tuple of state, parent_state to trace back solution path
                        self.solution_path[tuple(new_state)] = self.current_state


    def isFinalState(self):
        previous = -1

        for i in range(len(self.current_state) - 1):
            if previous < self.current_state[i]:
                previous = self.current_state[i]
            else:
                return False
        
        if self.current_state[len(self.current_state) - 1] == 0:
            print("Final state was found")
            self.end_time = time.time()
            return True

        return False

    def swap(self, i, j, state):
        temp = state[i]
        state[i] = state[j]
        state[j] = temp

    def generateSolution(self, filename):
        print("Generating the solution path . . .")
        base_char = 'a'
        stack = []
        file = open(filename + ".txt", "w")
        
        key = tuple(self.current_state)
        stack.append(key)

        # push into text file, also reverse the order. (push into a stack then pop them out for printing)
        while key in self.solution_path:
            key = tuple(self.solution_path[key])
            stack.append(key)

        file.write("Program took " + str(round(self.end_time - self.start_time, 4)) + "seconds to find solution\n\n")

        file.write("0 " + str(stack.pop()) + "\n")

        while stack:
            state = stack.pop()
            file.write(chr(ord(base_char) + state.index(0)) + " " + str(state) + "\n")

        print("Solution was generated in file : " + filename + ".txt")

    # hamming distance
    def heuristicA(self, state, depth=0):
        sum = 0

        for i in range(len(state)):
            # compare the current index with the right index
            if state[i] != 0:
                if i != (state[i] - 1):
                    sum += 1
                    
        return sum + depth

    # check how many moves it takes for each tile to reach their destination, excluding empty tile
    def heuristicB(self, state, depth=0):
        sum = 0

        for i in range(len(state)):
            if state[i] != 0:
                current_row = math.floor(i / self.size_x)
                current_column = i % self.size_x 

                final_row = math.floor((state[i] - 1) / self.size_x)
                final_column = (state[i] - 1) % self.size_x

                row_dif = abs(current_row - final_row)
                column_dif = abs(current_column - final_column)

                sum += max(row_dif, column_dif)

        return sum + depth