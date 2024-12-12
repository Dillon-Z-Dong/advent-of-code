# day12.py

import numpy as np
import networkx as nx
import time

def load_file(file):
	with open(file) as f:
		lines = [list(x.strip()) for x in f.readlines()]
	return np.array(lines)


def construct_graph(arr):
	'''
	finds all contiguous islands of the same value in arr
	- start with np.where() for each unique value. 
	- then add edges between adjacent values (exactly one index differs by 1)
	- then check which nodes are reachable

	returns list of all island indices

	Would be much faster to just handle the indices directly
	'''

	unique_values = np.unique(arr)
	
	island_dict = {}
	for val in unique_values:
		island_dict[val] = {}
		val_indices = np.where(arr == val)
		
		# Construct graph
		# set up nodes
		G = nx.Graph()
		island_dict[val]['graph'] = G
		for i in range(len(val_indices[0])):
			r, c = val_indices[0][i], val_indices[1][i]
			G.add_node((r,c))

		# set up edges
		for node1 in G.nodes:
			for node2 in G.nodes:
				if ((np.abs(node1[0]-node2[0]) == 1) and (node1[1] == node2[1])) or ((np.abs(node1[1]-node2[1]) == 1) and (node1[0] == node2[0])): #vertical or horizontal adjacency
					G.add_edge(node1,node2)

		# compute islands
		val_islands = {}
		island_dict[val]['islands'] = val_islands
		part_of_island = []
		val_island_index = 0

		# check all nodes including self for connectivity if node1 is not already part of an island
		for node1 in G.nodes:
			if node1 not in part_of_island:
				current_island = []
				for node2 in G.nodes:
					try:
						nx.shortest_path(G,node1,node2)
						current_island.append(node2)
						part_of_island.append(node2)
					except:
						pass
				val_islands[val_island_index] = current_island
				val_island_index += 1

	return island_dict


def generate_neighbors(index: tuple):
	x,y = index
	return [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] #left, right, down, up


def p1(arr):
	'''
	- perimeter is 4 - the number of neighbors in the island for each node in island
		- number of neighbors is the number of nodes for which the shortest path is 1 (or can just check with indices)
	- area is the size of the island
	- cost = perimeter * area
	'''
	start = time.time()
	print('Constructing graph')
	island_dict = construct_graph(arr)
	print(f'Constructed graph in {time.time()-start}')

	total_cost = 0
	for val,v in island_dict.items():
		G = v['graph']
		val_cost = 0
		for key, nodes in v['islands'].items():
			area = len(nodes)
			perimeter = 0
			for node in nodes:
				perim = 4
				for neighbor in generate_neighbors(node):
					if neighbor in G.nodes:
						perim -= 1
				perimeter += perim

			cost = perimeter * area
			val_cost += cost
			#print(f'For val = {val}: total cost = {cost}, perimeter = {perimeter}, area = {area}')
		total_cost += val_cost

	print(f'Total cost of everything is {total_cost} in {time.time() - start}')
	return 


def p2(arr):
	'''
	- perimeter is 4 - the number of neighbors in the island for each node in island
		- number of neighbors is the number of nodes for which the shortest path is 1 (or can just check with indices)
	- area is the size of the island
	- cost = perimeter * area
	'''
	start = time.time()
	print('Constructing graph')
	island_dict = construct_graph(arr)
	print(f'Constructed graph in {time.time()-start}')

	total_cost = 0
	for val,v in island_dict.items():
		G = v['graph']
		val_cost = 0
		for key, nodes in v['islands'].items():
			area = len(nodes)
			perimeter = 0
			counted_edges = {} 
			

			# Initialize all sides of each square to be counted
			for i, node in enumerate(nodes):
				counted_edges[node] = {}
				for side in ['left','up','right','down']:
						counted_edges[node][side] = 1 

			# Adjust counted edges based on neighbor config
			processed_nodes = []
			for i, node in enumerate(nodes):
				#print(f'\nProcessing {node}')
				processed_nodes.append(node)
				y,x = node
				up, down, left, right = generate_neighbors(node)
				#print(f'{left = }, {right = }, {down = }, {up = }')

				if left in processed_nodes:
					#print(f'{left = } in nodes')
					# Internal edge
					counted_edges[left]['right'] = 0
					counted_edges[node]['left'] = 0

					if (y-1,x-1) not in nodes: # up neighbor of left node
						#print('a')
						counted_edges[node]['up'] = 0 # up edge is continuation

					if (y+1,x-1) not in nodes: # down neighbor of left node
						#print('b')
						counted_edges[node]['down'] = 0

				if up in processed_nodes:
					#print(f'{up = } in nodes')
					counted_edges[up]['down'] = 0
					counted_edges[node]['up'] = 0

					if (y-1,x-1) not in nodes: # left neighbor of up node
						#print('c')
						counted_edges[node]['left'] = 0

					if (y-1,x+1) not in nodes: # right neighbor of up node
						#print('d')
						counted_edges[node]['right'] = 0

				if right in processed_nodes:
					#print(f'{right = } in nodes')
					counted_edges[right]['left'] = 0
					counted_edges[node]['right'] = 0

					if (y-1,x+1) not in nodes: # up neighbor of right node
						#print('e')
						counted_edges[node]['up'] = 0

					if (y+1,x+1) not in nodes: # down neighbor of right node
						#print('f')
						counted_edges[node]['down'] = 0

				if down in processed_nodes:
					#print(f'{down = } in nodes')
					counted_edges[down]['up'] = 0
					counted_edges[node]['down'] = 0

					if (y+1,x-1) not in nodes: # left neighbor of down node
						#print('g')
						counted_edges[node]['left'] = 0

					if (y+1,x+1) not in nodes: # right neighbor of down node
						#print('h')
						counted_edges[node]['right'] = 0

			# total perimeter
			for node, edges in counted_edges.items():
				#print(node, edges)
				perim = sum(edges[x] for x in ['up','down','left','right'])
				perimeter += perim


			cost = perimeter * area
			val_cost += cost
			print(f'For val = {val}: perimeter = {perimeter}, area = {area}, cost cost = {cost}')
		total_cost += val_cost

	print(f'Total cost of everything is {total_cost} in {time.time() - start}')
	return 


if __name__ == '__main__':
	test = load_file('test_data_day12.txt')
	real = load_file('data_day12.txt')

	p1(real)
	p2(real)











