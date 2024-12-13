import numpy as np

def load_grid(file):
    """Load input as 2D character grid"""
    with open(file) as f:
        return np.array([list(x.strip()) for x in f.readlines()])

def load_int_grid(file):
    """Load input as 2D integer grid"""
    with open(file) as f:
        return np.array([[int(x) for x in list(line.strip())] 
                        for line in f.readlines()])

def load_strings(file):
    """Load input as list of strings"""
    with open(file) as f:
        return [x.strip() for x in f.readlines()]

def load_ints(file):
    """Load input as list of integers"""
    with open(file) as f:
        return [int(x.strip()) for x in f.readlines()]

def load_delimited_ints(file, delimiter=","):
    """Load input as list of integers from single delimited line"""
    with open(file) as f:
        return [int(x) for x in f.read().strip().split(delimiter)]

def load_delimited_strings(file, delimiter=","):
    """Load input as list of strings from single delimited line"""
    with open(file) as f:
        return f.read().strip().split(delimiter)

def p1(data):
    """Solution for part 1"""
    return 

def p2(data):
    """Solution for part 2"""
    return 

if __name__ == '__main__':
    # Choose appropriate load function after seeing the input
    test = load_grid(f'test_data_day13.txt')
    print("Test input:", test)
    real = load_grid(f'data_day13.txt')
    
    p1(test)

