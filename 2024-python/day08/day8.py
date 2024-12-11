# day8.py
import numpy as np
import itertools
from fractions import Fraction

def load_data(file):
	with open(file) as f:
		lines = [list(line.strip()) for line in f.readlines()]

	arr = np.array(lines)
	arr[np.where(arr == '#')] = '.'
	unique = np.unique(arr)
	unique = list(unique[np.where(unique != '.')])
	return arr, unique


def _print(arr):
	for row in arr:
		print(''.join(row)+'\n')
	print(len(np.where(arr == '#')[0]))



def p1(data):

	arr, unique = load_data(data)
	source_arr = arr.copy()
	ymax,xmax = np.shape(arr)

	for u in unique:
		print(f'Processing {u}')
		combs = itertools.combinations(list(zip(np.where(source_arr == u)[0], np.where(source_arr == u)[1])), 2)
		for t1,t2 in combs:
			r1,c1 = t1
			r2,c2 = t2

			rdiff = np.abs(r1-r2)
			cdiff = np.abs(c1-c2)

			if r1 < r2 and c1 < c2: # first point is left, up
				if r1 - rdiff >= 0 and c1 - cdiff >= 0:
					arr[r1-rdiff][c1-cdiff] = '#"'
				if r2 + rdiff < ymax and c2 + cdiff < xmax:
					arr[r2+rdiff][c2+cdiff] = '#'

			elif r1 < r2 and c1 > c2: # first point is left, down
				if r1 - rdiff >= 0 and c1 + cdiff < xmax:
					arr[r1-rdiff][c1+cdiff] = '#'
				if r2+rdiff < xmax and c2-cdiff >= 0:
					arr[r2+rdiff][c2-cdiff] = '#'

			elif r1 > r2 and c1 < c2: # first point is right, up
				if r1+rdiff < ymax and c1-cdiff >= 0:
					arr[r1+rdiff][c1-cdiff] = '#'
				if r2-rdiff >= 0 and c2+cdiff < ymax:
					arr[r2-rdiff][c2+cdiff] = '#'
				
			elif r1 > r2 and c1 > c2: # first point is right, down
				if r1+rdiff < xmax and c1+cdiff < ymax:
					arr[r1+rdiff][c1+cdiff] = '#'
				if r2-rdiff >= 0 and c2-cdiff >=0:
					arr[r2-rdiff][c2-cdiff] = '#'

	_print(arr)



def p2(data):
	arr, unique = load_data(data)
	source_arr = arr.copy()
	ymax,xmax = np.shape(arr)

	for u in unique:
		print(f'Processing {u}')
		combs = itertools.combinations(list(zip(np.where(source_arr == u)[0], np.where(source_arr == u)[1])), 2)
		for t1,t2 in combs:
			r1,c1 = t1
			r2,c2 = t2

			dx = np.abs(c2-c1)
			dy = np.abs(r2-r1)

			slope = Fraction(dy, dx)
			y = slope.numerator
			x = slope.denominator

			if (r1 > r2 and c1 > c2) or (r1 < r2 and c1 < c2):
				i = 0
				go_pos = True
				while go_pos:
					r,c = r1+i*y, c1+i*x
					if r < ymax and c < xmax:
						arr[r][c] = '#'
						i+=1
					else:
						go_pos = False
				i = 0
				go_neg = True
				while go_neg:
					r,c = r1-i*y, c1-i*x
					if r >= 0 and c >= 0:
						arr[r][c] = '#'
						i+=1
					else:
						go_neg = False

			else:
				i = 0
				go_pos = True
				while go_pos:
					r,c = r1+i*y, c1-i*x
					if r < ymax and c >= 0:
						arr[r][c] = '#'
						i+=1
					else:
						go_pos = False
				i = 0
				go_neg = True
				while go_neg:
					r,c = r1-i*y, c1+i*x
					if r >= 0 and c < ymax:
						arr[r][c] = '#'
						i+=1
					else:
						go_neg = False



	_print(arr)







if __name__ == '__main__':
	test_data = 'test_data_day8.txt'
	real_data = 'data_day8.txt'
	p1(real_data)
	p2(real_data)



