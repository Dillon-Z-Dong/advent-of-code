import numpy as np
import networkx as nx
from collections import Counter

def load(file):
    with open(file) as f:
        arr = np.array([list(x.strip()) for x in f.readlines()])

    start = np.where(arr == 'S')
    start = (start[0][0],start[1][0])
    end = np.where(arr == 'E')
    end = (end[0][0],end[1][0])

    return arr, start, end

def get_neighbors(nodes, x_coords, y_coords, sep = 1):
    neighbors = {}
    count = 0
    nodes = np.array(nodes)
    for node in nodes:
        node_tuple = tuple(node)
        y1,x1 = node
        dx = np.abs(x1-x_coords)
        dy = np.abs(y1-y_coords)
        neighbor_indices = np.where(np.abs(dx) + np.abs(dy) <= sep)
        neighbors[node_tuple] = [tuple(n) for n in nodes[neighbor_indices]]
    return neighbors


def p1(data, thresh):
    """Solution for part 1"""
    mp, start, end = data

    y_coords, x_coords = np.where(np.isin(mp, ['.','S','E']))
    nodes = list(zip(y_coords, x_coords))

    neighbors1 = get_neighbors(nodes, x_coords, y_coords, sep = 1)
    neighbors2 = get_neighbors(nodes, x_coords, y_coords, sep = 2)


    G = nx.Graph()
    for node, neighbors in neighbors1.items():
        if node not in G.nodes:
            G.add_node(node)
        for n in neighbors:
            if n not in G.nodes:
                G.add_node(n)
            G.add_edge(node,n)

    costs_from_start = nx.single_source_dijkstra_path_length(G, start)

    count = 0
    L = []
    for node, neighbors in neighbors2.items():
        dist_to_node = costs_from_start[node]
        for neighbor in neighbors:
            dist_to_neighbor = costs_from_start[neighbor]
            diff = dist_to_neighbor - dist_to_node - 2
            if diff >= thresh:
                #print(node, neighbor, diff)
                L.append(diff)
                count += 1

    #print(Counter(sorted(L)))
    print(f'P1 solution: {count}')
    return

def p2(data, thresh):
    """Solution for part 2"""
    mp, start, end = data

    y_coords, x_coords = np.where(np.isin(mp, ['.','S','E']))
    nodes = list(zip(y_coords, x_coords))

    neighbors1 = get_neighbors(nodes, x_coords, y_coords, sep = 1)
    neighbors2 = get_neighbors(nodes, x_coords, y_coords, sep = 20)

    G = nx.Graph()
    for node, neighbors in neighbors1.items():
        if node not in G.nodes:
            G.add_node(node)
        for n in neighbors:
            if n not in G.nodes:
                G.add_node(n)
            G.add_edge(node,n)

    costs_from_start = nx.single_source_dijkstra_path_length(G, start)

    count = 0
    L = []
    for node, neighbors in neighbors2.items():
        y1,x1 = node
        dist_to_node = costs_from_start[node]
        for neighbor in neighbors:
            y2,x2 = neighbor
            dy = np.abs(y2-y1)
            dx = np.abs(x2-x1)
            manhattan_dist = dy + dx
            dist_to_neighbor = costs_from_start[neighbor]
            diff = dist_to_neighbor - dist_to_node - manhattan_dist
            if diff >= thresh:
                #print(node, neighbor, diff)
                L.append(diff)
                count += 1

    #print(Counter(sorted(L)))
    print(f'P2 solution: {count}')
    return

if __name__ == '__main__':
    # Choose appropriate load function after seeing the input
    test = load(f'test_data_day20.txt')
    real = load(f'data_day20.txt')
    
    p1(real,thresh=100)
    p2(real,thresh=100)
    
