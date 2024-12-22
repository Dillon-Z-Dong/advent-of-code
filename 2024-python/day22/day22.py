import numpy as np

def load(file):
    with open(file) as f:
        return np.array([int(x.strip()) for x in f.readlines()])
   

def p1(data):
    """Solution for part 1"""
    total = np.sum(generate_iter(data, 2000))

    print(f'P1 answer: {total}')
    return

def p2(data):
    """Solution for part 2"""
    niter = 2000
    prices = np.zeros((niter,len(data)))
    changes = np.zeros((niter,len(data)))
    n = data
    for i in range(niter):
        n = generate(n)
        digits = get_first_digit(n)
        if i == 0:
            price = get_first_digit(data)
            prices[i] = price
            diff = digits - price

        else:
            diff = digits - prev_digits
            prices[i] = prev_digits

        if i < len(changes) - 1:
            changes[i+1] = diff

        prev_digits = digits


    subseqs = get_all_subsequences(changes)

    best_seq = ''
    best_total_price = 0
    for seq, indices in subseqs.items():
        price = 0
        seen_cols = []
        for idx in indices:
            #if seq == (-2,1,-1,3):
            col, start_row = idx
            if col not in seen_cols:
                price += prices[start_row+3, col]
                seen_cols.append(col)

        if price > best_total_price:
            best_seq = seq
            best_total_price = price
            #print(f'{best_seq = }, {price = }')

    #print(best_seq)
    print(f'P2 answer: {int(best_total_price)}')
    return


def mix(a,b):
    return a^b

def prune(n):
    return n % 16777216


def generate(n):
    n = prune(mix(n,n*64))
    n = prune(mix(n,n//32))
    n = prune(mix(n,n*2048))

    return n

def generate_iter(n, niter):
    for i in range(niter):
        n = generate(n)
        #print(n)

    return n


def get_first_digit(vec):
    return np.array([int(str(n)[-1]) for n in vec])


def get_all_subsequences(arr):
    '''gets all subsequences of length 4 except starting nan and their (col,row) indices where they occur'''
    arr = arr.astype(int)
    subseqs = {}
    y,x = np.shape(arr)
    for start_row in range(1,y-4):
        for col in range(x):
            subseq = tuple(arr[start_row:start_row+4,col])
            if subseq in subseqs:
                subseqs[subseq].append((col, start_row))
            else:
                subseqs[subseq] = [(col,start_row)]

    return subseqs



if __name__ == '__main__':
    test = load(f'test_data_day22.txt')
    real = load(f'data_day22.txt')
    
    p1(real)
    p2(real)
    

        




    