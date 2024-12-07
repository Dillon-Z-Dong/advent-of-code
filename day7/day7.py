# day7.py
import numpy as np


def read_file(file):
	with open(file) as f:
		lines = f.readlines()
	d = {}
	for line in lines:
		key, sequence = line.strip().split(': ')
		d[int(key)] = [int(x) for x in sequence.split(' ')]

	return d

def generate_possibilities(start_array,next_val,target, use_concatenation):
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

	for i, next_val in enumerate(seq[1:]):
		start_array = generate_possibilities(start_array, next_val, target, use_concatenation)

	if target in start_array:
		return True
	return False


def p12(d, use_concatenation):
	total_calibration_result = 0
	for target, seq in d.items():
		if check_line(target,seq, use_concatenation):
			total_calibration_result += target

	print(f'Total calibration result: {total_calibration_result}')




if __name__ == '__main__':
	test = read_file('test_data_day7.txt')
	real = read_file('data_day7.txt')

	p12(real, use_concatenation = False)
	p12(real, use_concatenation = True)



