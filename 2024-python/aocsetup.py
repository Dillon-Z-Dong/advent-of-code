import os
import sys
from pathlib import Path

def create_python_file_content(day_num):
    return f'''import numpy as np

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
    test = load_grid(f'test_data_day{day_num}.txt')
    print("Test input:", test)
    real = load_grid(f'data_day{day_num}.txt')
    
    p1(test)
'''

def setup_aoc_day(day_num):
    # Create directory
    day_dir = Path(f'day{day_num}')
    if day_dir.exists():
        print(f"Directory day{day_num} already exists!")
        return
    
    day_dir.mkdir(exist_ok=True)
    
    # Create files only if they don't exist
    python_file = day_dir / f'day{day_num}.py'
    test_file = day_dir / f'test_data_day{day_num}.txt'
    data_file = day_dir / f'data_day{day_num}.txt'
    
    if not python_file.exists():
        with open(python_file, 'w') as f:
            f.write(create_python_file_content(day_num))
        print(f"Created {python_file}")
    
    if not test_file.exists():
        test_file.touch()
        print(f"Created {test_file}")
    
    if not data_file.exists():
        data_file.touch()
        print(f"Created {data_file}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python aocsetup.py <day_number>")
        sys.exit(1)
    
    try:
        day_num = int(sys.argv[1])
        setup_aoc_day(day_num)
    except ValueError:
        print("Please provide a valid day number")
        sys.exit(1)