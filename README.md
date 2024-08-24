# Application of Search Algorithms and Metaheuristics

## BFS, DFS, and A* Algorithm
Implemented and compared Breadth-First Search, Depth-First Search, and A* Search (with a Euclidean heuristic) on mazes of sizes 10x10, 15x15, and 20x20. Each maze consists of walkable (0) and blocked (1) cells, and the goal is to find a path from the top-left to the bottom-right corner. I measured and visualized metrics such as the number of nodes expanded, execution time, maximum fringe size, and path length for each algorithm to analyze how their performance scales with maze size.


## Tabu Search to solve Quadratic Assignment Problem (QAP)
Implemented a Tabu Search algorithm to solve a Quadratic Assignment Problem involving 20 departments and 20 locations arranged in a 5x4 grid. The objective was to minimize the total cost, which is the product of flow and rectilinear (Manhattan) distance between departments. The solution involved using a permutation encoding, exploring all possible moves with a comprehensive neighborhood function, and managing a recency-based tabu list without aspiration criteria to find a near-optimal solution.

## Ant Colony Optimization (ACO) to solve the Traveling Salesman Problem (TSP)
Implemented Ant Colony Optimization to solve the Traveling Salesman Problem for an 8-city complete undirected graph. The goal was to find the shortest route that visits each city exactly once and returns to the starting point. I represented each route as a permutation of cities and calculated the total distance traveled using the provided adjacency matrix. The ACO algorithm efficiently find an optimal or close-to-optimal route for the salesman.
