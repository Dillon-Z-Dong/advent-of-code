import numpy as np
from parse import *
import mpmath
from mpmath import mp
mp.dps = 20


def load_file(file):
    with open(file) as f:
        lines = [x.strip() for x in f.readlines()]
    machines = []
    prizes = []
    start_new_machine = True
    for i, line in enumerate(lines):
        if start_new_machine:
            machine = np.array([[0,0],[0,0]])
            start_new_machine = False
        
        if 'Button A' in line:
            ax,ay = parse('Button A: X+{}, Y+{}',line)
            machine[0][0] = ax
            machine[1][0] = ay

        elif 'Button B' in line:
            bx,by = parse('Button B: X+{}, Y+{}', line)
            machine[0][1] = bx
            machine[1][1] = by

        elif 'Prize' in line:
            px, py = parse('Prize: X={}, Y={}',line)
            prizes.append(np.array([int(px),int(py)]))
            machines.append(machine)
            start_new_machine = True

    return machines, prizes


def p1(data):
    '''        
    [a1, b1] A_presses       prize_x
    [a2, b2] B_presses    =  prize_y

    [A_presses, B_presses] = machine^-1 * prize
    '''

    machines, prizes = data
    presses = []
    costs = []

    for i, machine in enumerate(machines):
        A_inv = np.linalg.inv(machine)
        p = A_inv @ prizes[i]
       

        try:
            assert np.allclose(p, np.round(p))
            cost = np.sum(p*np.array([3,1]))
            presses.append(p)
            costs.append(cost)
        except:
             #print(f'Error with presses: {p}')
             pass



    print(f'P1 total cost: {int(np.sum(costs))}')

    return presses, costs



def p2(data):
    '''        
    [a1, b1] A_presses       prize_x
    [a2, b2] B_presses    =  prize_y

    [A_presses, B_presses] = machine^-1 * prize
    '''

    machines, prizes = data
    presses = []
    costs = []

    for i, machine in enumerate(machines):
        matrix = mp.matrix(machine.tolist())
        A_inv = mp.inverse(matrix)
        vec = mp.matrix((prizes[i] + np.array([1e13,1e13])).tolist())
        p = A_inv * vec
        diff0,diff1 = p[0] - int(p[0]), p[1] - int(p[1])
        if diff0 < 1e-5 and diff1 < 1e-5:
            cost = 3*p[0] + p[1]
            presses.append(p)
            costs.append(cost)
            #print(f'Successful: {p}')
        else:
             #print(f'Error with presses: {p}')
             pass


    print(f'P2 total cost: {int(np.sum(costs))}')

    return presses, costs

if __name__ == '__main__':

    test = load_file(f'test_data_day13.txt')
    real = load_file(f'data_day13.txt')

    p = p1(real)
    p = p2(real)

