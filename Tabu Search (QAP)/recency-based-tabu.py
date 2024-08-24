import numpy as np
from math import comb
import random
import heapq

dist = np.genfromtxt('Distance.csv', delimiter=',', dtype=np.int32)
flow = np.genfromtxt('Flow.csv', delimiter=',', dtype=np.int32)

MAX_ITERATIONS = 200
HEAP_SIZE = 10

# Viewing purposes
def show_state(state):
    for row in state:
        print(row)

def create_tabu_list( n = 4, m = 5 ):
    dist = np.zeros(shape=(n, m))
    tabu = {}

    for i in range(n):
        for j in range(m):
            value = i*m + j + 1
            dist[i, j] = value
            tabu[value] = (i, j)
    
    # print("Tabu:\n",tabu)
    return dist, tabu

def update_state(i, j, state, positions):
    xi, yi = positions[i+1]
    xj, yj = positions[j+1]
    
    temp   = state[xi, yi]
    state[xi, yi] = state[xj, yj]
    state[xj, yj] = temp

    positions[i+1] = xj, yj
    positions[j+1] = xi, yi

    return state, positions

# Generate all position swaps
def gen_moves(locations = 20):
    moves = {}
    for i in range(locations):
        for j in range(i+1, locations):
            moves[i, j] = 0
    
    return moves

# Calculate partial score from current i and j positions
def partial_score(i, j, dist, flow):
    return np.dot(dist[i, :], flow[i,:]) + np.dot(flow[j,:], dist[j, :])

# Calculate new partial score after swap
def new_partial_score(i, j, dist, flow):
    row_i = dist[i, :]
    row_j = dist[j, :]
    subscore = 0
    for k in range(len(row_i)):
        if(k == i or k == j):
            subscore += row_i[k]*flow[i, k] + row_j[k]*flow[j, k]
        else:
            subscore += row_j[k]*flow[i, k] + row_i[k]*flow[j, k]
    
    return subscore
    
# Given possible moves, return heap'd list of moves
def choose_moves(moves, dist, flow, n=None):
    swaps = list(moves.keys())
    chosen = []
    
    if(n is None or n > len(swaps)):
        n = len(swaps)
        # print(f"\nGenerate {n} swaps.\n")

    while(n > 0):
        n -= 1
        choose = random.choice(swaps)
        if(moves[choose] <= 0):
            i,j = choose
            swaps.remove(choose)
            subscore = new_partial_score(i, j, dist, flow) - partial_score(i, j, dist, flow)
            chosen.append((subscore, i, j))
        

    heapq.heapify(chosen)
    return chosen

# Global state score
def score(dist, flow):
    dist = dist.astype(np.int32)
    flow = flow.astype(np.int32)
    return np.sum(dist*flow)

# Swap (col_i w/ col_j) and (row_i w/ row_j)
def move(i, j, dist = dist):    
    # print(f"\nSwap object {i+1} w/ {j+1}")

    #Swap columns i and j
    dist[:, [i, j]] = dist[:, [j, i]]
    
    #Swap rows i and j
    dist[[i, j], :] = dist[[j, i], :]
    
    return dist 

# Reduce all recent moves by 1
def reduce_recency(moves):
    for move in moves:
        moves[move] = max(0, moves[move] - 1)
    return moves

# Main 
def tabu_search(dist, flow, OPTIMAL_SCORE = 1285, tenure_factor = 1, list_size=None, tenure_factors_list = None):

    # State
    state, positions = create_tabu_list()
    # print("INITIAL STATE:")
    # show_state(state)

    # All object swaps (i, j) no repeats (j, i)
    tabu_tenure = len(dist)
    all_moves = gen_moves(tabu_tenure)

    # Initial set of (n) moves
    next_moves = choose_moves(all_moves, n = list_size, dist= dist, flow=flow)
    
    # Calculate score of initial state, return if optimal
    state_score = score(dist, flow)/2
    iteration = 0
    min_score = state_score
    min_state = []
    min_iter  = 0
    
    """
    Record: 1295

        State:
    [ 5.  8.  1.  3. 18.]
    [17. 19. 12. 11. 14.]
    [ 6. 15.  4.  2. 16.]
    [13. 20.  7. 10.  9.]

    Optimal State(s):
    [18. 14. 10.  3.  9.]
    [ 4.  2. 12. 11. 16.]
    [19. 15. 20.  8. 13.]
    [17.  5.  7.  1.  6.]

    [ 6.  1.  7.  5. 17.]
    [13.  8. 20. 15. 19.]
    [16. 11. 12.  2.  4.]
    [ 9.  3. 10. 14. 18.]
    """
    while(next_moves and iteration < MAX_ITERATIONS):
        # print(f"\nCurrent Score (#{iteration}):", state_score)

        # Track min score found
        if(min_score > state_score):
            min_score = state_score
            min_state = state
            min_iter  = iteration

        # Break if optimal solution found
        if(state_score <= OPTIMAL_SCORE):
            # print("\n# of Moves:", iteration)
            # print("Score:", state_score)
            break
        
        # Get move that reduces score most
        subscore, i, j  = heapq.heappop(next_moves)

        # View updated matrix
        dist = move(i, j, dist)
        state, positions = update_state(i, j, state, positions)
        # show_state(state)

        # New State score
        state_score = score(dist, flow)/2

        # Reduce recent moves by 1
        all_moves = reduce_recency(all_moves)

        # Set most recent move = T 
        if(type(tenure_factor) == int or type(tenure_factor) == float):
            all_moves[(i, j)] = tabu_tenure*tenure_factor

        # Get new move
        next_moves = choose_moves(all_moves, n = list_size, dist= dist, flow=flow)

        # Ascending order
        heapq.heapify(next_moves)

        iteration += 1

    # print("\n##############################\n")
    # print(f"Min Score Found (#{min_iter}):", min_score)
    # print("MINIMUM STATE:")
    # show_state(min_state)
    # print("\n##############################\n")
    return min_state, min_score, min_iter
            
if __name__ == "__main__":
    n_tests = 10
    avg_score, avg_iters = 0, 0
    for i in range(1, n_tests+1):
        dist_n = dist.copy()
        optimal_state, opt_score, opt_iter = tabu_search(dist=dist_n, flow=flow, list_size=200, tenure_factor=1.2)
        avg_score += opt_score
        avg_iters += opt_iter
        print(f"\n\n### RUN No.{i} #######################\n")
        print(f"Min Score Found (#{opt_iter}):", opt_score)
        print("MINIMUM STATE:")
        show_state(optimal_state)
        
    print("#####################################")
    print("\nAvg Score     :", avg_score/n_tests)
    print("\nAvg Iterations:", avg_iters/n_tests)