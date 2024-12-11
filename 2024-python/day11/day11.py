# day11.py

import numpy as np
import time
from functools import cache

def load_file(file):
	with open(file) as f:
		lines = f.readlines()
	return [int(x) for x in lines[0].strip().split(' ')]


def evolve(number: str) -> list[str]:
	n = int(number)
	l = len(number)
	if n == 0:
		return ['1']
	elif l%2 == 0:
		return [str(int(number[:l//2])),str(int(number[l//2:]))]
	else:
		return [str(n*2024)]

def evolve_list(number_list):
	L = []
	for number in number_list:
		L += evolve(number)
	return L


def p1(line, n):
	line = [str(x) for x in line]
	start = time.time()
	for blink in range(n):
		line = evolve_list(line)
		print(f'length after blinking {blink} times: {len(line)} in time: {time.time()-start}')
		#print(f'line: {line}')
	#return line




def precompute_cache(n, max_iters):
	answers = {}

	@cache
	def evolve_number(n:int, iters, max_iters = max_iters):
		if iters == max_iters:
			return 

		elif n in answers:
			answer = answers[n]
			if type(answer) is int:
				return evolve_number(answer, iters+1)
			else:
				return evolve_number(answer[0],iters+1), evolve_number(answer[1],iters+1)

		else:
			if n == 0:
				answers[n] = 1
				return evolve_number(1,iters+1)

			else:
				l = len(str(n))
				if l%2 == 0:
					answer = (int(str(n)[:l//2]), int(str(n)[l//2:]))
					answers[n] = answer
					return evolve_number(answer[0], iters+1), evolve_number(answer[1],iters+1)

				else:
					answer = n*2024
					answers[n] = answer
					return evolve_number(answer,iters+1)

	evolve_number(n, iters = 0)
	#print(f'Length after {max_iters = } for {n = } is {len(answers)}')
	
	return answers



def recurse(n, max_iters, answers):
	'''
	The key was to have the running count be part of the function output!!!
	Incrementing a count caused entire subtrees to be skipped.
	'''
    @cache
    def evolve_number(n, iters=0, max_iters=max_iters):
        if iters == max_iters:
            return (None, 1)  # Return count of 1 for terminal nodes
        
        answer = answers[n]
        if type(answer) is int:
            next_val, count = evolve_number(answer, iters+1)
            return (next_val, count)
        else:
            left_val, left_count = evolve_number(answer[0], iters+1)
            right_val, right_count = evolve_number(answer[1], iters+1)
            return ((left_val, right_val), left_count + right_count)
    
    _, total_count = evolve_number(n)
    return total_count



if __name__ == '__main__':
	test = load_file('test_data_day11.txt')
	real = load_file('data_day11.txt')
	#p1(real, 25)

	max_iters = 75
	total_answers = {}
	start = time.time()
	for n in real:
		answers = precompute_cache(int(n),max_iters)
		total_answers.update(answers)
	print(f'Time elapsed to precompute {len(total_answers)} for {n = }: {(time.time() - start):.3f}\n')


	start = time.time()
	total_count = 0
	for n in real:
		count = recurse(int(n), max_iters, total_answers)
		total_count += count
		print(f'Time elapsed to add {count = } for {n = }: {(time.time() - start):.3f}')

	print(f'Total count: {total_count}')






