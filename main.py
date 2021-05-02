
class Node:

    # Initialize each node with the state representation(list of lists), g value and f value 
    def __init__(self,state,g,f):
        self.state = state
        self.g = g
        self.f = f

    # Expand the current state by using the four operators: blank up, blank down, blank left 
    # and blank right. Then return the expanded nodes if operators are valid.
    def expansion(self):
        
        x,y = self.locate(self.state)

        # All possible operators
        candidates = [[x,y-1], [x,y+1], [x-1,y], [x+1,y]]
        children = []

        for i in candidates:
            child = self.operate(self.state, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.g+1, 0)
                children.append(child_node)
        return children
     
    # Apply operators to current state and return the next state   
    def operate(self, current_state, x1, y1, x2, y2):

        # In case the blank is on the boundary
        if x2 >= 0 and x2 < len(self.state) and y2 >= 0 and y2 < len(self.state):
            next_state = []
            next_state = self.copy(current_state)
            temp = next_state[x2][y2]
            next_state[x2][y2] = next_state[x1][y1]
            next_state[x1][y1] = temp
            return next_state
        else:
            return None   

    # Create a copy of the state for replacement
    def copy(self, a_state):
        outer_list = []
        for i in a_state:
            inner_list = []
            for j in i:
                inner_list.append(j)
            outer_list.append(inner_list)
        return outer_list   
    
    # Locate where the blank is
    def locate(self, state):
        for i in range(0,len(self.state)):
            for j in range(0,len(self.state)):
                if state[i][j] == '_':
                    return i,j


class Puzzle:

    # Initialize the puzzle with the width if the puzzle, frontier and explored set.
    def __init__(self, size):
        self.size = size
        self.frontier_list = []
        self.explored_set = []

    # Read in the initial state from the user
    def read(self):
        initial_state = []
        for i in range(0,self.size):
            row = input().split(" ")
            initial_state.append(row)
        return initial_state

    # F value for uniform cost search
    def fucs(self, current_node, goal):
        return current_node.g

    # F value for A* search with misplace tiles heuristic
    def fmth(self, current_node, goal):
        return self.hmth(current_node.state, goal) + current_node.g

    # F value for A* search with euclidean distance heuristic
    def fedh(self, current_node, goal):
        return self.hedh(current_node.state, goal) + current_node.g


    # Heuristic function for uniform cost search
    def hucs(self, current_node, goal):
        return 0

    # Heuristic function for A* search with misplace tiles heuristic
    def hmth(self, current_node, goal):
        temp = 0
        for i in range(self.size):
            for j in range(self.size):
                if current_node[i][j] != goal[i][j] and current_node[i][j] != '_':
                    temp += 1
        return temp

    # Heuristic function for A* search with euclidean distance heuristic
    def hedh(self, current_node, goal):
        temp = 0
        for i in range(self.size):
            for j in range(self.size):
                if current_node[i][j] != '_':
                    num = int(current_node[i][j])
                    quotient = num//3
                    remainder = num % 3
                    if remainder == 0:
                        quotient -= 1
                        remainder += 3
                    remainder -= 1 

                    temp += ((i-quotient)**2 + (j-remainder)**2)**0.5
        return temp

 
    # Search algorithm
    def a_star_search(self):

        print("Enter the intial state: \n")
        start = self.read()

        print("Enter your choice of algorithm \n 1. Unifrom Cost Search \n 2. A-star with Misplaced tile heuristic \n 3. A-star with Euclidean distance heuristic")
        alg = input()

        if alg == "1":
            self.h = self.hucs
            self.f = self.fucs
        elif alg == "2":
            self.h = self.hmth
            self.f = self.fmth
        else:
            self.h = self.hedh
            self.f = self.fedh
    
        goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '_']]

        start = Node(start, 0, 0)
        start.fval = self.f(start,goal)

        self.frontier_list.append(start)
        print("\n\n")

        counter = 0
        max_node = 0

        while True:
            if not self.frontier_list:
                print('Failure')
                break

            # Explore the first node in the frontier list
            cur = self.frontier_list[0]

            print("")
            print("  | ")
            print(" \\|/ \n")

            # Add the currently exploring state to the explored set and delete from the frontier list
            self.explored_set.append(cur)
            del self.frontier_list[0]

            # Print the currently eploring state
            for i in cur.state:
                for j in i:
                    print(j,end=" ")
                print("")
            
            # If current state is the goal state, we succeed!
            if(cur.state == goal):
                break

            frontier = []
            for k in self.frontier_list:
                frontier.append(k.state)

            explored = []
            for j in self.explored_set:
                explored.append(j.state)

            # Apply operators to find the next states if the state is not in the frontier or in the explored set
            for i in cur.expansion():
                i.f = self.f(i, goal)
                if i.state not in frontier and i.state not in explored:
                    self.frontier_list.append(i)
            
            # Record the length of the frontier list
            length = len(self.frontier_list)
            max_node = max(max_node, length)
            
            #Sort the frontier nodes based on f value
            self.frontier_list.sort(key = lambda x:x.f, reverse=False)

            counter += 1

        print('\n')

        print('Goal!!! \n')

        print('To solve this problem the search algorithm expanded a total of %d nodes. \n'%counter)

        print('The maximum number of nodes in the queue at any one time: %d \n'%max_node)


eight_puzzle = Puzzle(3)

eight_puzzle.a_star_search()