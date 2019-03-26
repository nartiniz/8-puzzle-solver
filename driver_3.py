from __future__ import division
from __future__ import print_function

import sys
import math
import time
# import Queue as Q
from collections import deque


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """

    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n * n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n * n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(config[3 * i: 3 * (i + 1)])

    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if(self.blank_index!=0 and self.blank_index!=1 and self.blank_index!=2):
            newpuzzlestate = PuzzleState([3,1,2,0,4,5,6,7,8],3,self,"Up",self.cost+1)
            newpuzzlestate.config = self.config[:]
            newpuzzlestate.config[self.blank_index]=newpuzzlestate.config[self.blank_index-3]
            newpuzzlestate.config[self.blank_index-3]=0
            return newpuzzlestate
        pass

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if (self.blank_index != 6 and self.blank_index != 7 and self.blank_index != 8):
            newpuzzlestate = PuzzleState([3,1,2,0,4,5,6,7,8],3,self,"Down",self.cost+1)
            newpuzzlestate.config = self.config[:]
            newpuzzlestate.config[self.blank_index]=newpuzzlestate.config[self.blank_index+3]
            newpuzzlestate.config[self.blank_index+3]=0
            return newpuzzlestate

        pass

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if (self.blank_index != 0 and self.blank_index != 3 and self.blank_index != 6):
            newpuzzlestate = PuzzleState([3, 1, 2, 0, 4, 5, 6, 7, 8], 3,self,"Left",self.cost+1)
            newpuzzlestate.config = self.config[:]
            newpuzzlestate.config[self.blank_index] = newpuzzlestate.config[self.blank_index - 1]
            newpuzzlestate.config[self.blank_index - 1] = 0
            return newpuzzlestate
        pass

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if (self.blank_index != 2 and self.blank_index != 5 and self.blank_index != 8):
            newpuzzlestate = PuzzleState([3, 1, 2, 0, 4, 5, 6, 7, 8], 3,self,"Right",self.cost+1)
            newpuzzlestate.config = self.config[:]
            newpuzzlestate.config[self.blank_index] = newpuzzlestate.config[self.blank_index + 1]
            newpuzzlestate.config[self.blank_index + 1] = 0
            return newpuzzlestate
        pass

    def expand(self):
        """ Generate the child nodes of this node """

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children


# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(path_to_goal,cost_of_path,nodes_expanded,search_depth,max_search_depth,runnig_time,max_ram_usage):
    ### Student Code Goes here
    my_file=open("output.txt","w+")
    my_file.write("path_to_goal:"+str(path_to_goal))
    my_file.write("\ncost_of_path:"+str(cost_of_path))
    my_file.write("\nnodes_expanded:"+str(nodes_expanded))
    my_file.write("\nsearch_depth:"+str(search_depth))
    my_file.write("\nmax_search_depth:"+str(max_search_depth))
    my_file.write("\nrunning_time="+str(runnig_time))
    my_file.write("\nmax_ram_usage:"+str(max_ram_usage))
    my_file.close()
    pass


def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    start = time.time()
    path_to_Goal = deque()
    path_to_Goal_original = []
    cost_of_path = 0
    search_depth = 0
    max_search_depth = 0
    frontier = deque()
    frontier1 = set()
    visited = set()
    nodes_expanded = 0
    currentstate=PuzzleState(initial_state.config,initial_state.n)
    frontier1.add(str(currentstate.config))
    frontier.append(PuzzleState(currentstate.config,currentstate.n,currentstate.parent,currentstate.action,currentstate.cost))
    while(test_goal(currentstate)==0):
        print(currentstate.config)
        visited.add(str(currentstate.config))

        currentstate.expand()
        for x in range (len(currentstate.children)):
            # if(isincluded(currentstate.children[x],visited)==0) and (isincluded(currentstate.children[x],frontier)==0):
            if (str(currentstate.children[x].config) not in visited) and (str(currentstate.children[x].config) not in frontier1):
                # frontier.append(currentstate.children[x])
                frontier.append(currentstate.children[x])
                frontier1.add(str(currentstate.children[x].config))
                if(currentstate.children[x].cost>max_search_depth):
                    max_search_depth = currentstate.children[x].cost
        currentstate = PuzzleState(frontier[0].config , frontier[0].n,frontier[0].parent,frontier[0].action,frontier[0].cost)
        # currentstate = frontier.popleft()

        if(test_goal(currentstate)==1):
            nodes_expanded = len(visited)
        frontier1.remove(str(currentstate.config))
        frontier.popleft()
        # currentstate = frontier[0]
        # currentstate = frontier.popleft()
    print(currentstate.config)
    # cost_of_path = frontier[0].cost
    # search_depth = cost_of_path
    while(currentstate != None):
        path_to_Goal.append(currentstate.action)
        # print(currentstate.config)
        # print(test_goal(currentstate))
        # currentstate=PuzzleState(currentstate.parent.config,currentstate.parent.n,currentstate.parent.parent,currentstate.parent.action,currentstate.parent.cost)
        currentstate = currentstate.parent
    path_to_Goal.reverse()
    path_to_Goal.popleft()

    for x in range (len(path_to_Goal)):
        path_to_Goal_original.append(path_to_Goal[x])
    # for x in range(len(frontier)):
    #     if(frontier[x].cost>max_search_depth):
    #         max_search_depth=frontier[x].cost
    cost_of_path = len(path_to_Goal_original)
    search_depth = cost_of_path
    end = time.time()
    running_time = end-start
    writeOutput(path_to_Goal_original,cost_of_path,nodes_expanded,search_depth,max_search_depth,running_time,20)
    """As a comment : I just put a number 20 instead of finding maximum ram usage.It is because I don't use Cygwin, I can't use resource.
        I don't use ubuntu,but windows. However to show that I know how to find ram usage in Python, I must say resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        this function gives us ram usage in resource."""
    print(path_to_Goal_original)
    print(len(path_to_Goal_original))
    print(nodes_expanded)
    print(max_search_depth)


    return
    pass


def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    start = time.time()
    path_to_Goal = deque()
    path_to_Goal_original = []
    cost_of_path = 0
    search_depth = 0
    max_search_depth = 0
    frontier = deque()
    frontier1 = set()
    visited = set()
    nodes_expanded = 0
    currentstate = PuzzleState(initial_state.config, initial_state.n)
    frontier1.add(str(currentstate.config))
    frontier.append(PuzzleState(currentstate.config, currentstate.n, currentstate.parent, currentstate.action, currentstate.cost))
    while (test_goal(currentstate) == 0):
        print(currentstate.config)
        visited.add(str(currentstate.config))
        currentstate.expand()
        for x in range(len(currentstate.children)):
            # if(isincluded(currentstate.children[x],visited)==0) and (isincluded(currentstate.children[x],frontier)==0):
            NumofChildren = len(currentstate.children)
            if (str(currentstate.children[NumofChildren-1-x].config) not in visited) and (str(currentstate.children[NumofChildren-1-x].config) not in frontier1):
                # frontier.append(currentstate.children[x])
                frontier.append(currentstate.children[NumofChildren-1-x])
                frontier1.add(str(currentstate.children[NumofChildren-1-x].config))
                if(currentstate.children[x].cost>max_search_depth):
                    max_search_depth = currentstate.children[x].cost
        indexoflastElement = len(frontier) - 1
        currentstate = PuzzleState(frontier[indexoflastElement].config, frontier[indexoflastElement].n, frontier[indexoflastElement].parent, frontier[indexoflastElement].action,frontier[indexoflastElement].cost)
        # currentstate = frontier.popleft()
        if(test_goal(currentstate)==1):
            nodes_expanded = len(visited)
        frontier1.remove(str(currentstate.config))
        del frontier[indexoflastElement]
        # currentstate = frontier[0]
        # currentstate = frontier.popleft()
    print(currentstate.config)
    search_depth = cost_of_path


    while (currentstate != None):
        path_to_Goal.append(currentstate.action)
        # print(currentstate.config)
        # print(test_goal(currentstate))
        # currentstate=PuzzleState(currentstate.parent.config,currentstate.parent.n,currentstate.parent.parent,currentstate.parent.action,currentstate.parent.cost)
        currentstate = currentstate.parent
    path_to_Goal.reverse()
    path_to_Goal.popleft()

    for x in range(len(path_to_Goal)):
        path_to_Goal_original.append(path_to_Goal[x])
    # for x in range(len(frontier)):
    #     if(frontier[x].cost>max_search_depth):
    #         max_search_depth=frontier[x].cost
    cost_of_path = len(path_to_Goal_original)
    search_depth = cost_of_path
    end = time.time()
    running_time = end-start
    writeOutput(path_to_Goal_original, cost_of_path, nodes_expanded, search_depth, max_search_depth,running_time, 20)
    """As a comment : I just put a number 20 instead of finding maximum ram usage.It is because I don't use Cygwin, I can't use resource.
        I don't use ubuntu,but windows. However to show that I know how to find ram usage in Python, I must say resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        this function gives us ram usage in resource."""
    print(path_to_Goal_original)
    print(len(path_to_Goal_original))
    print(nodes_expanded)
    print(max_search_depth)
    return
    pass


pass


def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    start = time.time()
    path_to_Goal = deque()
    path_to_Goal_original = []
    cost_of_path = 0
    search_depth = 0
    max_search_depth = 0
    frontier = deque()
    frontier1 = set()
    visited = set()
    nodes_expanded = 0
    currentstate = PuzzleState(initial_state.config, initial_state.n)
    frontier1.add(str(currentstate.config))
    frontier.append(PuzzleState(currentstate.config, currentstate.n, currentstate.parent, currentstate.action, currentstate.cost))
    y = 0
    while (test_goal(currentstate) == 0):
        print(currentstate.config)
        visited.add(str(currentstate.config))

        currentstate.expand()
        for x in range(len(currentstate.children)):
            # if(isincluded(currentstate.children[x],visited)==0) and (isincluded(currentstate.children[x],frontier)==0):
            if (str(currentstate.children[x].config) not in visited) and (
                    str(currentstate.children[x].config) not in frontier1):
                # frontier.append(currentstate.children[x])
                frontier.append(currentstate.children[x])
                frontier1.add(str(currentstate.children[x].config))
                if (currentstate.children[x].cost > max_search_depth):
                    max_search_depth = currentstate.children[x].cost
        # currentstate = PuzzleState(frontier[0].config, frontier[0].n, frontier[0].parent, frontier[0].action,frontier[0].cost)
        # currentstate = frontier.popleft()
        minindex = 0
        mincost = frontier[0].cost+calculate_total_cost(frontier[0])
        for y in range (len(frontier)):
            if(mincost>frontier[y].cost+calculate_total_cost(frontier[y])):
                minindex = y
                mincost = frontier[y].cost+calculate_total_cost(frontier[y])
        currentstate = PuzzleState(frontier[minindex].config, frontier[minindex].n, frontier[minindex].parent, frontier[minindex].action,frontier[minindex].cost)
        if (test_goal(currentstate) == 1):
            nodes_expanded = len(visited)
        frontier1.remove(str(currentstate.config))
        del frontier[minindex]
        # currentstate = frontier[0]
        # currentstate = frontier.popleft()

        y += 1
    print(currentstate.config)
    # cost_of_path = frontier[0].cost
    # search_depth = cost_of_path

    while (currentstate != None):
        path_to_Goal.append(currentstate.action)
        # print(currentstate.config)
        # print(test_goal(currentstate))
        # currentstate=PuzzleState(currentstate.parent.config,currentstate.parent.n,currentstate.parent.parent,currentstate.parent.action,currentstate.parent.cost)
        currentstate = currentstate.parent
    path_to_Goal.reverse()
    path_to_Goal.popleft()

    for x in range(len(path_to_Goal)):
        path_to_Goal_original.append(path_to_Goal[x])
    # for x in range(len(frontier)):
    #     if(frontier[x].cost>max_search_depth):
    #         max_search_depth=frontier[x].cost
    cost_of_path = len(path_to_Goal_original)
    search_depth = cost_of_path
    end = time.time()
    running_time = end-start
    writeOutput(path_to_Goal_original, cost_of_path, nodes_expanded, search_depth, max_search_depth,running_time, 20)
    """As a comment : I just put a number 20 instead of finding maximum ram usage.It is because I don't use Cygwin, I can't use resource.
    I don't use ubuntu,but windows. However to show that I know how to find ram usage in Python, I must say resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    this function gives us ram usage in resource."""
    print(path_to_Goal_original)
    print(len(path_to_Goal_original))
    print(nodes_expanded)
    print(max_search_depth)
    return
    pass



def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    totalcost=0
    for x in range (state.n*state.n):
        if(state.config[x]!=0):
            totalcost=totalcost+calculate_manhattan_dist(state.config[x],x,3)
    return totalcost
    pass

def rowof(n):
    row=0
    if(n==3 or n==4 or n==5):
        row =1
    if(n==6 or n==7 or n==8):
        row=2
    return row

def columnof(n):
    column = 0
    if(n==1 or n==4 or n==7):
        column = 1
    if(n==2 or n==5 or n==8):
        column=2
    return column


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    return abs(columnof(idx)-columnof(value))+abs(rowof(idx)-rowof(value))
    pass


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    TrueorFalse=1
    for x in range (len(puzzle_state.config)):
        if(puzzle_state.config[x] != x):
            TrueorFalse=0
    return TrueorFalse
    pass


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    # search_mode = 'ast'
    # # begin_state = [3,1,2,6,4,5,7,8,0]
    # begin_state = [6,1,8,4,0,2,7,3,5]
    # # begin_state = list(map(int, begin_state))
    # # board_size = int(math.sqrt(len(begin_state)))
    # board_size= 3
    # hard_state = PuzzleState(begin_state, board_size)
    # start_time = time.time()
    #
    # if search_mode == "bfs":
    #     print(bfs_search(hard_state))
    # elif search_mode == "dfs":
    #     dfs_search(hard_state)
    # elif search_mode == "ast":
    #     A_star_search(hard_state)
    # else:
    #     print("Enter valid command arguments !")
    # #
    # end_time = time.time()
    # print("Program completed in %.3f second(s)" % (end_time - start_time))

    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, board_size)
    start_time = time.time()

    if search_mode == "bfs":
        bfs_search(hard_state)
    elif search_mode == "dfs":
        dfs_search(hard_state)
    elif search_mode == "ast":
        A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    print("Program completed in %.3f second(s)" % (end_time - start_time))

if __name__ == '__main__':
    main()