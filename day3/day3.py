# day3.py
import re

def read(file):
	with open(file) as f:
		lines = f.readlines()
	s = ''.join(lines)
	return s

def multiply_and_sum(mul_string_list):
	return sum([int(x)*int(y) for x,y in [pair.strip('mul()').split(',') for pair in mul_string_list]])


def p1(s):
	pattern = r'mul\(\d+,\d+\)'  # find anything that's literally 'mul(X,Y)' where X and Y are 1 or more digits. r is necessary for strings with \
	muls = re.findall(pattern,s)
	answer = multiply_and_sum(muls)
	print(f'Searched string of length {len(s)}')
	print(f'N multiplication instructions: {len(muls)}')
	print(f'Sum of multiplied instructions: {answer}')
	return answer

def p2(s):
	do_pattern = r'do\(\)'
	dont_pattern = r'don\'t\(\)'
	enabled = True
	position = 0
	running_sum = 0

	while True:
		print(f'\n\n{i = }, {enabled = }, {position = }, {running_sum = }')
		if enabled:
			next_dont = re.search(dont_pattern,s[position:])
			print(f'next_dont: {next_dont}')
			if next_dont is not None:
				enabled_string = s[position:position+next_dont.span()[0]]
				running_sum += p1(enabled_string)
				position += next_dont.span()[1]
				print(f'updated position (dont): {position}')
				enabled = False
			else:
				running_sum += p1(s[position:])
				print(f'Final value of running_sum: {running_sum}')
				break

		else:
			next_do = re.search(do_pattern, s[position:])
			print(f'next_do: {next_do}')
			if next_do is not None:
				position += next_do.span()[1]
				print(f'updated position (do): {position}')
				enabled = True
			else:
				print(f'Final value of running_sum: {running_sum}')
				break

	return running_sum


if __name__ == '__main__':
	s = read('data_day3.txt')
	p1(s)
	p2(s)

