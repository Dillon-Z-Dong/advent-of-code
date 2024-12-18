import numpy as np
import networkx as nx


def load(file, length = 1024):
    with open(file) as f:
        lines = [x.strip().split(',') for x in f.readlines()]
    out = [[int(x) for x in line] for line in lines]
    x_coords, y_coords = zip(*out)
    return x_coords[:length], y_coords[:length], [tuple(l) for l in out][:length]

def _print(mp):
    for row in mp:
        print(''.join(row))

def neighbors(node):
    y,x = node
    return [(y+1,x),(y-1,x),(y,x+1),(y,x-1)]

def p1(data):
    """Solution for part 1"""
    x,y, out = data
    mp = np.full((71,71),'.')

    mp[(x,y)] = '#'
    _print(mp)

    nodes = list(zip(*np.where(mp == '.'))) #areas that are not collapsed

    start_node = (0,0)
    end_node = (np.shape(mp)[0]-1,np.shape(mp)[1]-1)
    G = nx.Graph()

    for node in nodes:
        G.add_node(node)

    for node in nodes:
        for neighbor in neighbors(node):
            if neighbor in nodes:
                G.add_edge(node,neighbor)

    shortest_path = nx.shortest_path_length(G, source=start_node, target=end_node)
    print(f'Shortest path: {shortest_path}')
    return

def p2(data):
    """Solution for part 2"""
    return

if __name__ == '__main__':
    # Choose appropriate load function after seeing the input
    test = load(f'test_data_day18.txt',12)
    real = load(f'data_day18.txt',2879) #total length 3450, the first time it breaks is 2879
    #--> Proper implementation would be a binary search, but I just guessed and checked
    
    x,y, out = real
    mp = np.full((71,71),'.')

    mp[(x,y)] = '#'
    _print(mp)

    nodes = list(zip(*np.where(mp == '.'))) #areas that are not collapsed

    start_node = (0,0)
    end_node = (np.shape(mp)[0]-1,np.shape(mp)[1]-1)
    G = nx.Graph()

    for node in nodes:
        G.add_node(node)

    for node in nodes:
        for neighbor in neighbors(node):
            if neighbor in nodes:
                G.add_edge(node,neighbor)

    shortest_path = nx.shortest_path_length(G, source=start_node, target=end_node)
    print(f'Shortest path: {shortest_path}')

    #p1(test)
