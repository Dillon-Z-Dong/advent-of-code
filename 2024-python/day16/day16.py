import numpy as np
import networkx as nx

def load_grid(file):
    with open(file) as f:
        arr = np.array([list(x.strip()) for x in f.readlines()])

    start = np.where(arr == 'S')
    start = (start[0][0],start[1][0])
    end = np.where(arr == 'E')
    end = (end[0][0],end[1][0])

    return arr, start, end


def _print(mp):
    for row in mp:
        print(''.join(row))

def get_front_neighbor(coord, orientation):
    y,x = coord
    o = orientation #0 = ^, 1 = >, 2 = v, 3 = <

    if o == 0:
        return ((y-1,x),o)
    elif o == 1:
        return ((y,x+1),o)
    elif o == 2:
        return ((y+1,x),o)
    elif o == 3:
        return ((y,x-1),o)

def get_rotation_neighbors(coord, orientation):
    y,x = coord

    neighbors = []
    for rotation in [1,-1]:
        new_orientation = (orientation+rotation)%3
        neighbors.append((coord,new_orientation))

    return neighbors


def construct_graph(mp,start,end):
    G = nx.Graph()
    return G


def p1(data):
    """Dijkstra's alg wrapped in networkx"""

    mp, start, end = data

    G = nx.Graph()

    y_coords, x_coords = np.where(np.isin(mp, ['.','S','E']))
    coords = list(zip(y_coords, x_coords))

    for coord in coords:
        for orientation in [0,1,2,3]: #0 = ^, 1 = >, 2 = v, 3 = <
            G.add_node((coord,orientation)) #((y,x),orientation)

    nodes = list(G.nodes)
    for node in nodes:
        coord, orientation = node
        G.add_edge(node,get_front_neighbor(coord,orientation),weight = 1)
        for rotation in get_rotation_neighbors(coord,orientation):
            if coord != end:
                G.add_edge(node,rotation,weight = 1000)
            else:
                # zero cost rotations once you're already on end
                # This enables shortest path finding to any end orientation
                G.add_edge(node,rotation,weight = 0) 

    start_node = (start,1)
    end_node = (end,0)
    path_weight = nx.shortest_path_length(G, source=start_node, target=end_node, weight='weight')

    print(f'Shortest path weight for p1: {path_weight}')
    return path_weight

def p2(data):
    """
    Lemma:

    A node N is on a shortest path if 
    the shortest distance in from start to N 
    + the shortest distance from end to N 
    = the total shortest path

    Proof:
    in the pudding

    Note G is not a digraph so you don't need to invert the graph
    """

    shortest_path_weight = p1(data)

    mp, start, end = data

    G = nx.Graph()
    y_coords, x_coords = np.where(np.isin(mp, ['.','S','E']))
    coords = list(zip(y_coords, x_coords))

    for coord in coords:
        for orientation in [0,1,2,3]: #0 = ^, 1 = >, 2 = v, 3 = <
            G.add_node((coord,orientation)) #((y,x),orientation)

    nodes = list(G.nodes)
    for node in nodes:
        coord, orientation = node
        G.add_edge(node,get_front_neighbor(coord,orientation),weight = 1)
        for rotation in get_rotation_neighbors(coord,orientation):
            if coord != end:
                G.add_edge(node,rotation,weight = 1000)
            else:
                # zero cost rotations once you're already on end
                # This enables shortest path finding to any end orientation
                G.add_edge(node,rotation,weight = 0)



    start_node = (start,1)
    end_node = (end,0)

    costs_from_start = nx.single_source_dijkstra_path_length(G, start_node, weight='weight')
    costs_from_end = nx.single_source_dijkstra_path_length(G, end_node, weight='weight')

    best_seating = []
    for node in nodes:
        if costs_from_start[node] + costs_from_end[node] == shortest_path_weight:
            best_seating.append(node[0]) #append only the position, we don't care about orientation?

    print(f'Length of best seating for p2: {len(set(best_seating))}')


    return

if __name__ == '__main__':
    # Choose appropriate load function after seeing the input
    test = load_grid(f'test_data_day16.txt')
    real = load_grid(f'data_day16.txt')

    p2(real) # This will also solve p1

