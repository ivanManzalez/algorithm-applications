###############################################################################################
###############################################################################################
### Comparison and Enhancement of BFS, DFS, and A* Algorithms #################################
###############################################################################################
###############################################################################################

from collections import deque 
import time 
import heapq
import math
import copy

def load_maze(filepath):
    data = []
    with open(filepath, 'r') as grid:
        for row in grid:
            row = row.strip()
            if ' ' in row:
                data_row = [int(col) for col in row.split()]
            else:
                data_row = [int(col) for col in row]
            data.append(data_row)
    return data

def show_maze(maze):
    for row in maze:
        for spot in row:
            if(spot==1):
                print("|", end=" ")
            elif(spot == 8):
                print("x",  end=" ")
            else:
                print("0",end=" ")
        print()

# BFS Implementation ############################################################
def bfs(data):
    
    start = time.time()
    nodes_expanded = 0
    TOP, BOTTOM, LEFT, RIGHT = 0, len(data)-1, 0, len(data[0])-1
    visited = set()
    q = deque([(0, 0, 0)])
    q_size = len(q)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] # R, D, U, L
    while q:
        x, y, path_length = q.popleft()
        nodes_expanded += 1
        visited.add((x, y))
        data[x][y] = 8
        
        if((x, y) == (BOTTOM, RIGHT)):
            return nodes_expanded, path_length+1, q_size, time.time() - start, data

        for d in directions:
            if(x+d[0] >= TOP and x+d[0] <= BOTTOM and y+d[1] >= LEFT and y+d[1] <= RIGHT and (x+d[0], y+d[1]) not in visited and data[x+d[0]][y+d[1]] == 0):
                q.append((x+d[0], y+d[1], path_length+1))
        
        q_size = max(q_size, len(q))
    
    return None

# DFS Implementation ############################################################
def dfs(data):
    
    start = time.time()
    visited = set()
    nodes_expanded = 0
    TOP, BOTTOM, LEFT, RIGHT = 0, len(data)-1, 0, len(data[0])-1
    stack = [(0,0,0)]
    stack_size = len(stack)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while(stack):
        x, y, path_length = stack.pop()
        nodes_expanded += 1
        visited.add((x, y))
        data[x][y] = 8

        if((x, y) == (BOTTOM, RIGHT)):
            return nodes_expanded, path_length, stack_size, time.time() - start, data

        for d in directions:
            if(x+d[0] >= TOP and x+d[0] <= BOTTOM and y+d[1] >= LEFT and y+d[1] <= RIGHT and (x+d[0], y+d[1]) not in visited and data[x+d[0]][y+d[1]] == 0):
                stack.append((x+d[0], y+d[1], path_length+1))
        stack_size = max(stack_size, len(stack))
    
    return None

# A* Implementation ################################################

def h_euclid(x, y, data_w, data_l):
    return math.sqrt( (x - data_w)**2 + (y - data_l)**2 )

def h_manhattan(x, y, data_w, data_l):
    return (x - data_w) + (y - data_l)

def a_star(data, h):
    data_w, data_l  = len(data) - 1, len(data[0]) - 1
    TOP, BOTTOM, LEFT, RIGHT = 0, len(data)-1, 0, len(data[0])-1
    
    max_heap = [(10*h(0,0, data_w, data_l), (0,0,0))]
    
    start = time.time()
    visited = set()

    nodes_expanded = 0
    max_heap_size = 1
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
   
    while(max_heap):
        x, y, path_length = heapq.heappop(max_heap)[1]
        nodes_expanded += 1
        visited.add((x, y))
        
        data[x][y] = 8
        
        if((x, y) == (BOTTOM, RIGHT)):
            return nodes_expanded, path_length, max_heap_size, time.time() - start, data

        for d in directions:
            if(TOP <= x+d[0] <= BOTTOM and
               LEFT <= y+d[1] <= RIGHT and
               (x+d[0], y+d[1]) not in visited and 
               data[x+d[0]][y+d[1]] == 0):
                
                path_cost =  0
                h_end   = h(x+d[0], y+d[1], data_w, data_l)

                heapq.heappush(max_heap, ( round(10*(path_cost+h_end),1), (x+d[0], y+d[1], path_length+1)))

        max_heap_size = max(max_heap_size, len(max_heap))
    
    return None

# Empirical Scaling Analysis ##############################
# Plots ################################################
 
if __name__ == "__main__":

    mazes = ["10x10", "15x15", "20x20"]

    sm_nodes, md_nodes, lg_nodes = [], [] ,[]
    sm_path, md_path, lg_path = [], [] ,[]
    sm_max_q, md_max_q, lg_max_q = [], [] ,[]
    sm_time, md_time, lg_time = [], [] ,[]


    for maze in reversed(mazes):

        print(f"\n== {maze} MAZE ============================\n")
        data1 = load_maze(maze) 
        data2 = copy.deepcopy(data1)
        data3 = copy.deepcopy(data1)

        # show_maze(data)
        
        print("\n-- BFS -----------------------------------\n")
        nodes_expanded, path_length, max_q, execution_time, map = bfs(data1)
        show_maze(map)
        print("\nnodes_expanded: ", nodes_expanded)
        print("path_length: ", path_length)
        print("max_q: ", max_q)
        print("execution_time: ", execution_time)
        sm_nodes.append(nodes_expanded)
        sm_path.append(path_length)
        sm_max_q.append(max_q)
        sm_time.append(execution_time)
        
        print("\n-- DFS -----------------------------------\n")
        nodes_expanded, path_length, max_stack, execution_time, map = dfs(data2)
        show_maze(map)
        print("\nnodes_expanded: ", nodes_expanded)
        print("path_length: ", path_length)
        print("max_stack: ", max_stack)
        print("execution_time: ", execution_time)
        md_nodes.append(nodes_expanded)
        md_path.append(path_length)
        md_max_q.append(max_q)
        md_time.append(execution_time)
        
        print("\n-- A* -----------------------------------\n")
        nodes_expanded, path_length, max_stack, execution_time, map = a_star(data3, h = h_euclid)
        show_maze(map)
        print("\nnodes_expanded: ", nodes_expanded)
        print("path_length: ", path_length)
        print("max_stack: ", max_stack)
        print("execution_time: ", execution_time)
        lg_nodes.append(nodes_expanded)
        lg_path.append(path_length)
        lg_max_q.append(max_q)
        lg_time.append(execution_time)
        print("\n------------------------------------------")


    