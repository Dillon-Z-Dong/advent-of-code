import numpy as np
import networkx as nx

def load(file):
    with open(file) as f:
        lines = f.readlines()

    patterns = [x.strip() for x in lines[0].strip().split(',')]
    desired = [x.strip() for x in lines[2:]]

    return patterns, desired




def p1(data):

    patterns, desired = data

    n_works = 0
    for i, towel in enumerate(desired):
        G = nx.DiGraph()
        G.add_node('END')
        
        contained = [c for c in patterns if c in towel]
        for i in range(len(towel)):
            remainder = towel[i:]
            for c in contained:
                if remainder.startswith(c):
                    if (i,c) not in G.nodes: # might have already been added due to next_remainder
                        G.add_node((i,c)) 

                    if len(c) == len(remainder):
                        G.add_edge((i,c),'END')

                    else:
                        next_remainder = remainder[len(c):]
                        for c2 in contained:
                            if next_remainder.startswith(c2):
                                G.add_node((i+len(c),c2))
                                G.add_edge((i,c),(i+len(c),c2))


        start_nodes = []
        for c in contained:
            if towel.startswith(c):
                start_nodes.append((0,c))

        success = False
        for start in start_nodes:
            try:
                shortest_path = nx.shortest_path_length(G, start, 'END')
                success = True
                n_works += 1
                break
            except:
                continue

        #print(f'Success = {success} for {towel}')

    print(f'P1 solution: {n_works}')
    return


def count_paths(G, start, end, memo = None):
    if memo is None:
        memo = {}

    if start == end:
        return True

    if start in memo:
        return memo[start]

    total = 0
    for nextnode in G.successors(start):
        total += count_paths(G, nextnode, end, memo)

    memo[start] = total
    return total



def p2(data):
    patterns, desired = data
    count = 0
    for i, towel in enumerate(desired):
        #print(f'Processing towel {i}')
        G = nx.DiGraph()
        G.add_node('END')
        
        contained = [c for c in patterns if c in towel]
        for i in range(len(towel)):
            remainder = towel[i:]
            for c in contained:
                if remainder.startswith(c):
                    if (i,c) not in G.nodes: # might have already been added due to next_remainder
                        G.add_node((i,c)) 

                    if len(c) == len(remainder):
                        G.add_edge((i,c),'END')

                    else:
                        next_remainder = remainder[len(c):]
                        for c2 in contained:
                            if next_remainder.startswith(c2):
                                G.add_node((i+len(c),c2))
                                G.add_edge((i,c),(i+len(c),c2))


        start_nodes = []
        for c in contained:
            if towel.startswith(c):
                start_nodes.append((0,c))

        for start in start_nodes:
            count += count_paths(G, start, 'END')

    print(f'P2 answer: {count}')
    return

if __name__ == '__main__':
    test = load(f'test_data_day19.txt')
    real = load(f'data_day19.txt')
    
    p1(real)
    p2(real)
    

    



