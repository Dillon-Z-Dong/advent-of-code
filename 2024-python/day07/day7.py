# day7.py
import numpy as np
import time


def read_file(file):
	with open(file) as f:
		lines = f.readlines()
	d = {}
	for line in lines:
		key, sequence = line.strip().split(': ')
		d[int(key)] = [int(x) for x in sequence.split(' ')]

	return d

def generate_possibilities(start_array,next_val,target, use_concatenation):
	'''
	Generates all valid combinations of current array plus one more element. 
	Prunes any solutions that exceed the target (since all operations monotonically increase values)
	Exponential growth, but ok because max seq length is 12
	'''

	start_array = np.array(start_array)
	plus = start_array + next_val
	mul = start_array * next_val
	if use_concatenation:
		concat = np.array([int(y+str(next_val)) for y in [str(x) for x in start_array]])
		return np.concatenate([plus[np.where(plus <= target)], mul[np.where(mul <= target)], concat[np.where(concat <= target)]])
	else:
		return np.concatenate([plus[np.where(plus <= target)], mul[np.where(mul <= target)]])


def check_line(target,seq, use_concatenation):
	start_array = np.array(seq[:1])

	for i, next_val in enumerate(seq[1:]): #Iterate through whole array
		start_array = generate_possibilities(start_array, next_val, target, use_concatenation)

	if target in start_array: # check if after incorporating the last element, the target value was generated
		return True
	return False


def p12(d, use_concatenation = False):
	'''p1 and p2 are the same calculation except p2 uses concatenation'''

	total_calibration_result = 0
	for target, seq in d.items():
		if check_line(target,seq, use_concatenation):
			total_calibration_result += target

	print(f'Total calibration result: {total_calibration_result}')




if __name__ == '__main__':
	test = read_file('test_data_day7.txt')
	real = read_file('data_day7.txt')

	p1_start = time.time()
	print(f'p1: {p12(real)} in {(time.time() - p1_start):.6f} seconds')

	p2_start = time.time()
	print(f'p2: {p12(real,use_concatenation = True)} in {(time.time() - p2_start):.6f} seconds')




