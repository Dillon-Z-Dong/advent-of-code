import numpy as np
import networkx as nx

def load(file):
    with open(file) as f:
        return [x.strip() for x in f.readlines()]

def p1(data):
    '''Original solution for p1'''
    npad = get_npad()
    apad = get_apad()

    total_sum = 0
    print('-'*50)
    for d in data:
        print(f'Processing {d}')
        number = int(d[:-1])
        npad_seqs = robot(d, npad)

        # Robot 1
        robot1 = []
        best_length = 1e10
        for seq in npad_seqs:
            apad_seqs = robot(seq,apad)
            las = len(apad_seqs[0])
            if las < best_length:
                robot1 = apad_seqs
                best_length = las
            elif las == best_length:
                robot1 += apad_seqs

        print(f'{len(robot1)} possible optimum sequences of length {len(robot1[0])} for robot 1')

        # Robot 2
        robot2 = []
        best_length = 1e10
        for seq in robot1:
            apad_seqs = robot(seq,apad)
            las = len(apad_seqs[0])
            if las < best_length:
                robot2 = apad_seqs
                best_length = las
            elif las == best_length:
                robot2 += apad_seqs

        print(f'{len(robot2)} possible optimal sequences of length {len(robot2[0])} for robot 2')

        total_sum += number * len(robot2[0])
        print('-'*50)
        print(f'P1 solution: {total_sum}')
    return



def get_path_seq(G,path, final_A = True):
    seq = ''
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i+1]
        seq += G[current_node][next_node]['direction']

    if final_A:
        seq += 'A'
    return seq


def get_npad():
    npad_dirs = {7:{'>':8,'v':4},8:{'<':7,'>':9,'v':5},9:{'<':8,'v':6},\
    4:{'^':7,'>':5,'v':1},5:{'<':4,'^':8,'>':6,'v':2},6:{'^':9,'<':5,'v':3},\
    1:{'^':4,'>':2},2:{'<':1,'^':5,'>':3,'v':0},3:{'^':6,'<':2,'v':'A'},\
    0:{'^':2,'>':'A'},'A':{'^':3,'<':0}}

    npad = nx.DiGraph() #numeric keypad
    for node in list(range(10)) + ['A']:
        npad.add_node(node)

    for node in npad.nodes:
        for direct,button in npad_dirs[node].items():
            npad.add_edge(node,button, direction = direct)

    return npad

def get_apad():
    apad = nx.DiGraph() # arrow pad
    #robot2 = nx.DiGraph()
    #you = nx.DiGraph() # you -> robot2 -> robot1 -> npad
    for node in ['^','>','v','<','A']:
        apad.add_node(node)
        #for G in [robot1,robot2,you]:
            #G.add_node(node)

    apad_dirs = {'^':{'>':'A','v':'v'},'A':{'<':'^','v':'>'},\
    '<':{'>':'v'},'v':{'^':'^','<':'<','>':'>'},'>':{'^':'A','<':'v'}}

    for node in ['^','>','v','<','A']:
        for direct,button in apad_dirs[node].items():
            apad.add_edge(node,button, direction = direct)

    return apad


def robot(d, G):
    numeric_seq = [int(x) if x in [str(y) for y in range(10)] else x for x in list(d)]
    #print(numeric_seq)
    start = 'A'
    current_pos = start

    seqs = {}
    for i, pos in enumerate(numeric_seq):
        seqs[i] = []
        paths = nx.all_shortest_paths(G, current_pos, pos)
        for path in paths:
            #print(path)
            path_seq = get_path_seq(G, path)

            if i == 0:
                seqs[i].append(path_seq)
            else:
                for seq in seqs[i-1]:
                    seqs[i].append(seq + path_seq)

        current_pos = pos
        #print(f'new pos: {pos}')
        #print(seqs[i])

    return seqs[i]

def compute_cache(G):
    '''
    returns node1+node2: list of all shortest paths
    '''

    memo = {}
    cost = {}
    for node1 in G.nodes:
        for node2 in G.nodes:
            tup = str(node1)+str(node2)
            if node1 == node2:
                memo[tup] = ['']
            else:       
                memo[tup] = []
                paths = nx.all_shortest_paths(G, node1, node2)
                for path in paths:
                    memo[tup].append(get_path_seq(G,path, final_A = False))

    for key, val in memo.items():
        cost[key] = len(val[0])

    return memo, cost


def get_all_subproblems(input_seq):
    L = ['A'+input_seq[0]]
    for i in range(len(input_seq) - 1):
        L.append(input_seq[i] + input_seq[i+1])
    return L


def get_all_sequences(input_seq, memo, subproblems=None, i=0, seq='', result=None):
    '''Gets all sequences at depth - 1 that produce the input_seq'''
    if result is None:
        result = []
    
    if subproblems is None:
        subproblems = get_all_subproblems(input_seq)
    
    if i == len(subproblems):
        result.append(seq)
        return result
    
    subproblem = subproblems[i]
    paths = memo[subproblem]
    
    for path in paths:
        get_all_sequences(input_seq, memo, subproblems, i+1, seq+path+'A', result)
    
    return result

def get_best_sequence_length(input_seq, depth, memo, seq_memo = None):
    #print(f'{input_seq = }')

    if seq_memo is None:
        seq_memo = {}

    if depth == 0:
        return len(input_seq)

    if (depth, input_seq) in seq_memo:
        #print(f'Cache hit for {(depth, input_seq)}')
        return seq_memo[(depth, input_seq)]


    # Partition the problem into subproblems that all end with 'A' and add back the A

    subproblems = [x+'A' for x in input_seq.split('A')][:-1]
    #print(f'Subproblems: {subproblems}')

    total_cost = 0
    for subproblem in subproblems:
        sequences_to_try = get_all_sequences(subproblem, memo)
        #print(f'Trying {sequences_to_try} for {subproblem = }')
        
        subproblem_cost = np.inf
        for seq in sequences_to_try:
            cost = get_best_sequence_length(seq, depth-1, memo, seq_memo)
            if cost < subproblem_cost:
                subproblem_cost = cost

        total_cost += subproblem_cost

    seq_memo[(depth, input_seq)] = total_cost
    return total_cost


def p12(data, depth):
    """Solution for parts 1 and 2"""
    npad = get_npad()
    apad = get_apad()

    nmemo, ncost = compute_cache(npad)
    memo, cost = compute_cache(apad) #cost is at depth 1

    #foo = get_best_sequence_length('<A', 1, memo)
    #foo = get_best_sequence_length('<A^A>^^AvvvA', 8, memo)

    total_sum = 0
    #print('-'*50)
    for d in data:
        #print(f'Processing {d}')
        number = int(d[:-1])
        npad_seqs = robot(d,npad)

        best_seq_length = np.inf
        for seq in npad_seqs:
            #print(f'Processing possible sequence {seq}')
            length = get_best_sequence_length(seq, depth, memo)
            #print(f'Calculated length {length}')
            if length < best_seq_length:
                best_seq_length = length

        total_sum += number * best_seq_length
        #print('-'*50)

    return total_sum



if __name__ == '__main__':
    test = load(f'test_data_day21.txt')
    real = load(f'data_day21.txt')
    
    print('P1 answer:', p12(real, depth = 2))
    print('P2 answer:', p12(real, depth = 25))

    


'''

Key insight:
- Subproblems can be split at A. The only reason you ever press A is after you've solved a depth d - 1 problem. All problems end with A.

'''
       