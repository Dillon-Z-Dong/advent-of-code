# day10.py

import networkx as nx
import numpy as np

def read_file(file):
	with open(file) as f:
		lines = [list(x.strip()) for x in f.readlines()]

	return np.array(lines).astype(int)


def construct_graph(file):
	arr = read_file(file)
	max_rows = arr.shape[0]
	max_cols = arr.shape[1]
	
	# Initialize graph with nodes for all positions
	DG = nx.DiGraph()
	nodes = []
	for row in range(max_rows):
		for col in range(max_cols):
			node = (row,col)
			nodes.append(node)
			DG.add_node(node)

	# Add edges for all nodes to neighbors that are within elevation 1
	# also keep track of nines and zeros
	nines = []
	zeros = []
	for node in nodes:
		row, col = node
		elevation = arr[row][col]
		if elevation == 9:
			nines.append(node)
		elif elevation == 0:
			zeros.append(node)

		neighbors = [(row+1,col),(row-1,col),(row,col-1),(row,col+1)]
		for neighbor in neighbors:
			r,c = neighbor
			try:
				if arr[r][c] - elevation == 1:
					DG.add_edge(node,neighbor)
			except: # except when overflowing the bounds of array
				pass

	return DG, nines, zeros

def p1(file):
	DG, nines, zeros = construct_graph(file)
	reachable_nines = 0
	for trailhead in zeros:
		for nine in nines:
			try:
				nx.shortest_path(DG, trailhead,nine)
				reachable_nines += 1
			except:
				pass
	print(reachable_nines)


def p2(file):
	DG, nines, zeros = construct_graph(file)
	rating = 0
	for trailhead in zeros:
		for nine in nines:
			rating += len(list(nx.all_simple_paths(DG, trailhead, nine)))

	print(rating)



if __name__ == '__main__':
	test = 'test_data_day10.txt'
	real = 'data_day10.txt'

	p1(real)
	p2(real)


