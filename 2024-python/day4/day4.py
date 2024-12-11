import numpy as np
import re

def get_array(file):
    '''Reads a file of characters into a np array'''

    with open(file) as f:
        lines = [list(line.strip()) for line in f.readlines()] 

    return np.array(lines)

def concat_diagonal(arr):
    '''
    Reads a 2D array of chars in diagonals from top right to bottom left and concatinates all of the values into 1 string.
    Uses the fact that each of those diagonals contains all of the combinations of indices that sum to a single integer
    The total number of diagonals is the array's x dimension + y dimension - 1
    '''
    concat_list = []
    concat_list_original_indices = []
    y,x = arr.shape
    for diagonal in range(1,x+y):
        concat = ''
        original_indices = []
        #print(f'{diagonal = }')
        for i in range(max(0, diagonal - x), min(y,diagonal)):
            j = min(diagonal - 1 - i, x-1)
            #print(f'{i = }, {j = }')
            char = arr[i][j]
            #print(f'{char = }')
            concat += char
            original_indices.append((i,j))
        concat_list.append(concat)
        concat_list_original_indices.append((original_indices))
    return concat_list, concat_list_original_indices

def p1(file):
    input_array = get_array(file)
    total_count = 0
    for k in range(4): # Consider all possible row and diagonal orientations
        arr = np.rot90(input_array, k)
        diags, _ = concat_diagonal(arr)
        row_xmas = [re.findall('XMAS', ''.join(list(row))) for row in arr]
        diag_xmas = [re.findall('XMAS', diag) for diag in diags]
        for result in row_xmas:
            total_count += len(result)
        for result in diag_xmas:
            total_count += len(result)

    print(f'Total p1 xmas count: {total_count}')
    return total_count



def get_pivot_indices(arr):
    pivot_indices = []
    concat_list, original_indices = concat_diagonal(arr)

    for i, diag in enumerate(concat_list):
        mas_centers = [match.span()[0]+1 for match in re.finditer('MAS', diag)]
        sam_centers = [match.span()[0]+1 for match in re.finditer('SAM', diag)]
        for center in mas_centers + sam_centers:
            pivot_indices.append(original_indices[i][center])

    return pivot_indices


def p2(file):
    arr = get_array(file)
    pivots = get_pivot_indices(arr)
    xmas_count = 0

    # Check other direction for MAS or SAM
    for pivot in pivots:
        i,j = pivot
        if set([arr[i-1][j-1],arr[i+1][j+1]]) == set(['S','M']):
            xmas_count += 1

    print(f'Total p2 xmas_count: {xmas_count}')
    return xmas_count




if __name__ == '__main__':
    test_data = './test_data.txt'
    real_data = './data_day4.txt'
    p1(real_data)
    p2(real_data)
    

        

    


    


    





