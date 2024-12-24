import numpy as np
from parse import *
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt

def load(file):
    with open(file) as f:
        lines = [x.strip() for x in f.readlines()]

    inputs = {}
    operations = {}
    for i, line in enumerate(lines):
        if ':' in line:
            gate, value = parse('{}: {}', line)
            inputs[gate] = int(value)

        elif '->' in line:
            gate1, op, gate2, value = parse('{} {} {} -> {}', line)
            operations[(gate1,op,gate2, i)] = value

    return inputs, operations

def operation(gate1, op, gate2):
    if op == 'AND':
        return int(gate1) & int(gate2)

    elif op == 'OR':
        return int(gate1) | int(gate2)

    elif op == 'XOR':
        return int(gate1) ^ int(gate2)


def update(values, ops):
    for tup in ops:
        gate1, op, gate2, _ = tup
        if gate1 in values and gate2 in values:
            target = ops[tup]
            if target not in values:
                g1 = values[gate1]
                g2 = values[gate2]
                values[ops[tup]] = operation(g1,op,g2)
                #print(f'Updated value {gate1 = }, {gate2 = },{target = }')
    return values, ops

def get_final_values(values, ops):
    known_values = len(values)
    while True:
        update(values,ops)
        kv = len(values)
        if kv == known_values:
            break
        else:
            known_values = kv

    return values, ops


def lpad(s):
    return '0'*(2-len(s))+s


def p1(data):
    inputs, ops = data
    values = inputs.copy()
    values, ops = get_final_values(values, ops)
    answer = get_number(values, 'z')
    return answer

def get_number(values, start_str):
    L = []
    for value in values:
        if value.startswith(start_str):
            L.append(value)

    z_string = ''.join([str(values[z]) for z in sorted(L)])
    answer = int(z_string[::-1],2)
    return answer



def info(node):
    return [(v, data) for (u, v, data) in G.out_edges(node, data=True)]

def pred(node):
    return list(G.predecessors(node))

def make_plot(G, adjust, bad, values):
    plt.figure(figsize=(50, 50))
    pos = nx.kamada_kawai_layout(G)

    node_colors = ['red' if node in adjust
                   else 'orange' if node in bad
                   else 'green' if (node.startswith('x') or node.startswith('y'))
                   else 'gray' if values[node] == 0
                   else 'blue' if values[node] == 1
                   else 'lightblue'
                   for node in G.nodes()]

    nx.draw(G, pos, 
            with_labels=True,
            node_color=node_colors,
            node_size=1000,
            arrowsize=20,
            arrows=True)

    plt.savefig('graph.png')


if __name__ == '__main__':
    test = load(f'test_data_day24.txt')
    real = load(f'data_day24.txt')
    
    data = real
    
    inputs, ops = data

    # test random inputs
    #for k in inputs:
    #    inputs[k] = np.random.choice([0,1])


    values = inputs.copy()
    values, ops = get_final_values(values,ops)

    x = get_number(inputs, 'x')
    y = get_number(inputs, 'y')

    goal = x+y
    target_zs = {}
    for i, bit in enumerate(bin(goal)[2:][::-1]):
        target_zs['z'+lpad(str(i))] = int(bit)


    ok = []
    adjust = []
    for z in target_zs:
        if values[z] != target_zs[z]:
            print(f'Incorrect value for {z}: {values[z]}, should be {target_zs[z]}')
            adjust.append(z)
        else:
            ok.append(z)



    G = nx.DiGraph()
    for tup, value in ops.items():
        g1,op,g2, _ = tup

        if g1 not in G.nodes:
            G.add_node(g1)

        if g2 not in G.nodes:
            G.add_node(g2)

        if value not in G.nodes:
            G.add_node(value)

        G.add_edge(g1,value, op = op)
        G.add_edge(g2,value, op = op)

    G.add_node('START')
    values['START'] = None
    for node in G.nodes:
        if node.startswith('x') or node.startswith('y'):
            G.add_edge('START',node)


    for i in range(45):
        i = lpad(str(i))
        xnode = 'x'+i
        ynode = 'y'+i
        znode = 'z'+i

        if info(xnode) != info(ynode):
            raise Exception('x and y not linked')

        # print(i, info(xnode))

        for intermediate in info(xnode):
            name, data = intermediate
            if data['op'] == 'AND':
                s = name

            elif data['op'] == 'XOR':
                c = name

        if i != '00':
            if s.startswith('z'):
                print(f'BAD: {s} (z output as direct sum)')

            if c.startswith('z'):
                print(f'z output as direct carry: {c}')
                swap.append(c)

        #print(i, info(c))
        if (znode,{'op':'XOR'}) not in info(c):
            if i != '00':
                print('-'*50)
                print(f'BAD: {znode} (z node not fed by carry bit {c})')
                predecessors = pred(znode)
                for p in predecessors:
                    print(f'predecessor of {znode} {p} has outgoing edges {info(p)}')
                print('-'*50)

    # manual inspection
    bad = ['chv','jpj','kgj','rts','vvw','z07','z12','z26']


    make_plot(G,adjust,bad, values)
