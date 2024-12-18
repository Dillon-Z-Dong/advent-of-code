import numpy as np
from parse import *
import time
from functools import cache

def load(file):
    with open(file) as f:
        lines = [x.strip() for x in f.readlines()]

    registers = {}
    for line in lines:
        if 'Register' in line:
            letter, value = parse('Register {}: {}',line)
            registers[letter] = int(value)
        elif 'Program' in line:
            program = [int(x) for x in parse('Program: {}', line)[0].split(',')]

    return registers, program


def combo(operand, reg):
    if operand in [0,1,2,3]:
        return operand
    elif operand == 4:
        return reg['A']
    elif operand == 5:
        return reg['B']
    elif operand == 6:
        return reg['C']
    else:
        raise Exception(f'Illego combo operand: {operand = }, {reg = }')


def exe(opcode, operand, reg, pointer, verbose=True):
    '''returns (new pointer location, output if any)'''
    if opcode == 0: #adv: register A / combo operand
        new_val = reg['A'] // 2**(combo(operand,reg))
        if combo(operand,reg) != 3:
            raise Exception(f'Opcode 0: Denominator was not 8') 
        if verbose:
            print(f"Op0: Set A from {reg['A']} to {new_val} [A = {new_val}, B={reg['B']}, C={reg['C']}] (A // 8)")
        reg['A'] = new_val
        return (pointer+2, None)

    elif opcode == 1: #bxl: bitwise XOR of register B and literal operand
        new_val = reg['B'] ^ operand
        if operand not in [2,7]:
            raise Exception(f'Opcode 1: operand {operand} was not 2 or 7') # 2 is for step 2, 7 is for step 6

        #if operand == 2: #skip step 2, check if answer is the same <--- it is not!!!
        #    return (pointer+2, None)

        if verbose:
            print(f"Op1: Set B from {reg['B']} to {new_val} [A = {reg['A']}, B={new_val}, C={reg['C']}] (B XOR {operand})")
        reg['B'] = new_val
        return (pointer+2, None)

    elif opcode == 2: #bst: combo operand % 8
        combo_val = combo(operand,reg)
        new_val = combo_val % 8
        if verbose:
            print(f"Op2: Set B from {reg['B']} to {new_val} [A = {reg['A']}, B={new_val}, C={reg['C']}] (from combo={combo_val}) mod 8")
        reg['B'] = new_val
        return (pointer+2, None)

    elif opcode == 3: #jnz
        if reg['A'] == 0:
            if verbose:
                print(f"Op3: A is zero, continuing to next instruction [A = {reg['A']}, B={reg['B']}, C={reg['C']}]")
            return (pointer+2, None)
        else:
            if operand != 0:
                raise Exception(f'Jumped to {operand = }, which is not 0 (the start of the sequence)')
            if verbose:
                print(f"Op3: A={reg['A']} (binary: {split(bin(reg['A'])[2:])}) is non-zero, jumping to address {operand} [A = {reg['A']}, B={reg['B']}, C={reg['C']}]")
                print('.'*50)
                print()
            return (operand, None)

    elif opcode == 4: #bxc
        new_val = reg['B'] ^ reg['C']
        if verbose:
            print(f"Op4: Set B from {reg['B']} to {new_val} [A = {reg['A']}, B={new_val}, C={reg['C']}] (XOR with C)")
        reg['B'] = new_val
        return (pointer+2, None)

    elif opcode == 5: #out
        out_val = combo(operand,reg) % 8
        if verbose:
            print(f"Op5: Output value {out_val} [A={reg['A']}, B={reg['B']}, C={reg['C']}] (from combo={combo(operand,reg)})")
        return (pointer+2, out_val)

    elif opcode == 6: #bdv
        #new_val = int(reg['A'] / 2**(combo(operand,reg)))
        #if verbose:
        #    print(f"Op6: Set B from {reg['B']} to {new_val} [A = {reg['A']}, B={new_val}, C={reg['C']}] (A divided by 2**{combo(operand,reg)})")
        #reg['B'] = new_val
        #return (pointer+2, None)
        raise Exception('Opcode 6 does not appear in the program')

    elif opcode == 7: #cdv
        new_val = int(reg['A'] / 2**(combo(operand,reg)))
        if verbose:
            print(f"Op7: Set C from {reg['C']} to {new_val} [A = {reg['A']}, B={reg['B']}, C={new_val}] (A divided by 2**B = 2**{combo(operand,reg)})")
        reg['C'] = new_val
        return (pointer+2, None)


def show_cache_info(func):
    """Display cache statistics."""
    info = func.cache_info()
    print(f"Cache info for {func.__name__}:")
    print(f"- Hits: {info.hits}")
    print(f"- Misses: {info.misses}")
    print(f"- Max size: {info.maxsize}")
    print(f"- Current size: {info.currsize}")

def p1(data, regA = None, verbose = False):
    """Solution for part 1"""
    reg, prog = data

    if regA is not None:
        reg['A'] = regA

    pointer = 0
    outputs = []
    reg_A_at_output = []
    reg_C_at_output = []

    while True:
        if pointer >= len(prog):
            break

        opcode = prog[pointer]
        operand = prog[pointer+1]
        pointer, output = exe(opcode,operand,reg,pointer, verbose)
        if output is not None:
            outputs.append(output)
            reg_A_at_output.append(reg['A'])
            reg_C_at_output.append(reg['C'])
            if verbose:
                print('-'*20)
                print(f'Output: {output} --- A = {reg['A']}, B = {reg['B']}, C = {reg['C']}')
                print('-'*20)

    print(f'P1 answer: {','.join([str(x) for x in outputs])}')
    if verbose:
        print()
        print('-'*50)
        print(f'Final register state: {reg}')
        print('-'*50)
        print(f'Original program: {prog}')
        print('-'*50)
        print(f'Full output: {outputs}')
    
    return outputs, reg_A_at_output, reg_C_at_output



def loop(A):
    ''' 
    Run a single loop. Takes only the value of the A register as input, returns output and new value of A
    This is ~10x faster than running the full program. Didn't need this optimization in the end because of backwards search
    '''
    newA = A//8
    B = (A%8)^2
    C = A//2**(B)
    B2 = B^C
    output = (B2^7)%8

    return output, newA


def split(s, dec=False):
    # Pad string with leading zeros if needed to make length divisible by 3
    padded = '0' * ((3 - len(s) % 3) % 3) + s
    
    # Split into groups of 3
    groups = [padded[i:i+3] for i in range(0, len(padded), 3)]
    
    if dec:
        # Convert each binary group to decimal
        groups = [str(int(group, 2)) for group in groups]
    
    return ' '.join(groups)


def searchA(desired_out, desired_A):
    for i in range(max(1,desired_A*8), (desired_A+1)*8):
        output, newA = loop(i)
        if output == desired_out and newA == desired_A:
            #print(f'Found match: A = {i} produces {output = }, {newA = }')
            return i
    raise Exception('Could not find match: expand search space!')


def p2(data):
    """ Does a backwards search for the value of A that produces the correct next value of A and the desired next output value """
    reg, prog = data
    desired_A = 0
    for desired_out in prog[::-1]:
        desired_A = searchA(desired_out, desired_A)

    print(f'P2 answer: {desired_A}')
    return desired_A



if __name__ == '__main__': 
    test = load(f'test_data_day17.txt')
    real = load(f'data_day17.txt')

    p1(real)
    p2(real)

    

    

    

