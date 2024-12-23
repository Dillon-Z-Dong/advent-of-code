import numpy as np
import networkx as nx
from parse import *

def load(file):
    with open(file) as f:
        lines = [x.strip() for x in f.readlines()]

    L = []
    for line in lines:
        a,b = parse('{}-{}',line)
        L.append((a,b))
    return L


if __name__ == '__main__':
    test = load(f'test_data_day23.txt')
    real = load(f'data_day23.txt')
    
    data = real

    # Part 1
    tees = set()
    connections = {}

    for tup in data:
        for i, node in enumerate(tup):
            if node[0] == 't':
                tees.add(node)
            
            if i == 0:
                other = tup[1]  
            elif i == 1:
                other = tup[0]

            if node in connections:
                connections[node].add(other)
            else:
                connections[node] = set([other])


    three_cycles = []
    for t in tees:
        for c in connections[t]:
            for c2 in connections[c]:
                if t in connections[c2]:
                    three_cycles.append((t,c,c2))



    unique_three_cycles = []
    for cycle in [sorted(x) for x in three_cycles]:
        if cycle not in unique_three_cycles:
            unique_three_cycles.append(cycle)

    print(f'P1 answer: {len(unique_three_cycles)}')


    # Part 2

    G = nx.Graph()
    for tup in data:
        a,b = tup
        for node in [a,b]:
            if node not in G.nodes:
                G.add_node(node)
            G.add_edge(a,b)



    max_clique = max(nx.find_cliques(G), key = len)
    print(f'P2 Password: {','.join(sorted(max_clique))}')

    