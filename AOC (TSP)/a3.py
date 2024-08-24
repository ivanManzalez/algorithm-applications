import argparse, sys
import random
import numpy as np
import matplotlib.pyplot as plt

"""
RUNTIME
MEMORY
CONVERGENCE RATE
"""

class AOC:
    INIT_PHEROMONE = 1
    PHEROMONE_DEPOSIT = 1
    EVAP_RATE = 0.5
    ITERATIONS = 1
    ALPHA, BETA = 1, 1

    def main(self):
        
        shortest_paths = []        

        for i in range(self.iterations):
            print(f"\n\n------ Iter #{i} ------")
            SHORTEST_PATH = None
            SHORTEST_PATHLENGTH = np.inf
            pheromone_paths = []

            for ant in range(self.n_ants):
                print(f"\n* Ant #{ant} *")
                
                position = self.get_starting_position()
                path = [position]

                for _ in range(self.n_nodes - 1):
                    probabilities = self.get_probabilities(position, path)
                    position      = self.get_next_position(probabilities)
                    path.append(position)

                path_length = self.calc_length(path)
                
                if(path_length < SHORTEST_PATHLENGTH):
                    SHORTEST_PATHLENGTH = path_length
                    SHORTEST_PATH = path
                
                
                self.display_path(path, path_length)

                pheromone_paths.append((path, path_length))
                self.update_pheromone_matrix(pheromone_paths)
                pheromone_paths = []
                
            shortest_paths.append([SHORTEST_PATH, SHORTEST_PATHLENGTH])
        
        # print("\n\n============================================")
        # print(f"SHORTEST PATH FOUND ({SHORTEST_PATHLENGTH}):")
        # self.display_path(SHORTEST_PATH)
        # self.display_adj_matrix()
        # print("============================================")
        return shortest_paths, self.n_ants, self.iterations, self.EVAP_RATE, self.alpha, self.beta, self.INIT_PHEROMONE, self.PHEROMONE_DEPOSIT
        
                

    def __init__(self, filepath=None, n_ants = None, iterations = None, beta = None, alpha = None):
       
        self.adjacency_matrix = []
        self.pheromones = {}
        self.desirability = {}
        
        ###### Iterations ############################
        if(iterations is None):
            self.iterations = self.ITERATIONS
        else:
            self.iterations = iterations
        
        ###### Filepath to Adjacency Matrix  #########
        if(filepath is None):
            self.filepath = "adjacency.txt"
        else:
            self.filepath = filepath
        
        ##############################################

        self.load_adj_matrix()
        self.n_nodes = len(self.adjacency_matrix)
        self.create_desirability_matrix()
        self.create_pheromone_matrix()
        
        ####### Num of Ants #########################
        if(n_ants is not None):
            self.n_ants = n_ants
        else:
            self.n_ants = len(self.adjacency_matrix)

        ####### Alpha ###############################
        if(alpha is not None):
            self.alpha = alpha
        else:
            self.alpha = self.ALPHA
        
        ####### Beta  ###############################
        if(beta is not None):
            self.beta = beta
        else:
            self.beta = self.BETA

        ##############################################

    def load_adj_matrix(self):
        with open(self.filepath, "r") as datafile:
            for line in datafile:
                line = line.strip("\n")
                entries = line.split(", ")
                self.adjacency_matrix.append(entries)
    
    def create_desirability_matrix(self):
        for r in range(0, self.n_nodes):
            for c in range(r+1, self.n_nodes):
                self.desirability[(r, c)] = 1 / int(self.adjacency_matrix[r][c])                

    def create_pheromone_matrix(self):
        for r in range(0, self.n_nodes):
            for c in range(r+1, self.n_nodes):
                self.pheromones[(r, c)] = self.INIT_PHEROMONE
    
    def calc_length(self, path):
        length = 0
        for i in range(self.n_nodes-1):
            length += int(self.adjacency_matrix[path[i]][path[i+1]])

        return length + int(self.adjacency_matrix[path[-1]][path[0]])

    def update_pheromone_matrix(self, paths):
        for path_segment, _ in self.pheromones.items():
            self.pheromones[path_segment] *= (1-self.EVAP_RATE)
        
        for path, path_length in paths:
            for i in range(self.n_nodes - 1):
                path_segment = [path[i], path[i+1]]
                path_segment.sort()
                self.pheromones[tuple(path_segment)] += self.PHEROMONE_DEPOSIT / path_length

    def get_next_position(self, probabilities):
        return random.choices(range(self.n_nodes), weights = probabilities)[0]
    
    def get_probabilities(self, position, path):
        probabilities = np.zeros(self.n_nodes)
        
        for i in range(self.n_nodes):
            if(i in path):
                continue
            
            path_segment = [position, i]
            path_segment.sort()
            path_segment = tuple(path_segment)
            probabilities[i] = (self.pheromones[path_segment]**self.alpha) * (self.desirability[path_segment]**self.beta)
        
        return probabilities/np.sum(probabilities)
    
    def get_starting_position(self):
        return random.choice(range(self.n_nodes))
    
    def display_path(self, path, path_length):
        for i in range(self.n_nodes):
            if(i == self.n_nodes - 1):
                print(f"{path[i]} ({path_length})")
            else:
                print(f"{path[i]}", end=" -> ")
    
    def display_adj_matrix(self):
        for r in range(self.n_nodes):
            for c in range(r+1, self.n_nodes):
                print((r, c),self.adjacency_matrix[r][c])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description='''<Description>''',
        epilog='''<Epilogue>'''
        )
    
    parser.add_argument('-i','--iterations', type=int)
    parser.add_argument('-f','--adjMatrix',  type=str)
    parser.add_argument('-n','--numAnts', type=int)

    parser.add_argument('-a','--alpha', type=int)
    parser.add_argument('-b','--beta', type=int)
    cli = parser.parse_args()
    

    aoc = AOC(filepath=cli.adjMatrix, n_ants= cli.numAnts, iterations=cli.iterations, alpha=cli.alpha, beta=cli.beta)
    aoc.main()
    # plt.plot()
    # plt.show()


