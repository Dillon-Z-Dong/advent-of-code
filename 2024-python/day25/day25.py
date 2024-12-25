import numpy as np

def load_grid(file):
    """Load input as 2D character grid"""
    with open(file) as f:
        lines = [x.strip() for x in f.readlines()]

    schematics = {'lock':[],'key':[]}

    for i, line in enumerate(lines):
        row = i % 8
        if row == 0:
            if i != 0:
                schematics[stype].append(schematic)

            schematic = [-1]*5
            if line[0] == '#':
                stype = 'lock'
            else:
                stype = 'key'
            #print(stype)

        for j, colval in enumerate(line):
            schematic[j] += (colval == '#')

        #print(i, row, line)

    schematics[stype].append(schematic)
    return schematics





def p1(data):
    """Solution for part 1"""
    locks = [np.array(x) for x in data['lock']]
    keys = [np.array(x) for x in data['key']]

    fit_count = 0
    for lock in locks:
        for key in keys:
            if np.all((lock + key) < 6):
                fit_count += 1

    print(f'P1 answer: {fit_count}')
    return


def p2(data):
    print('Merry Christmas!!')

if __name__ == '__main__':
    test = load_grid(f'test_data_day25.txt')
    real = load_grid(f'data_day25.txt')
    

    p1(real)
    p2(real)
