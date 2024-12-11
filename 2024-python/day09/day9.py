# day9.py

import numpy as np

def read_file(file):
	with open(file) as f:
		lines = f.readlines()
	disk_string = lines[0].strip()
	return disk_string


def parse_disk(disk_string):
	'''

	The value of every even character is the length of a file, and its index//2 is that file's index
	The value of every odd character is the number of free spaces

	returns dict mapping each expanded index to its value (either '.'' for free space or the file ID number)
	'''
	mapping = {}
	current_expanded_index = 0

	for i, char in enumerate(list(disk_string)):
		if i%2 == 0: # length of file
			filelength = int(char)

			for _ in range(filelength):
				mapping[current_expanded_index] = int(i//2) 
				current_expanded_index += 1

		else: #free space
			free_space_length = int(char)
			for _ in range(free_space_length):
				mapping[current_expanded_index] = '.'
				current_expanded_index += 1

	return mapping


def sort_from_end(mapping):
	'''
	1. Iterates through map key range in reverse. Finds indices and values of non free space entries in reverse order.
	2. Iterates down the range of map keys. If map[key] is '.', swaps values with the precomputed first (reverse) value
		- do this only if it increases the index. otherwise terminate.
	'''

	r = list(mapping.items())
	r.reverse()

	for i,val in mapping.items(): #may need to sort here
		if val == '.':
			get_last_nonfree = True
			while get_last_nonfree:
				rev_idx, rev_val = r.pop(0) #get first element of reverse list, remove it from list
				if rev_idx <= i:
					return mapping
				elif rev_val != '.':
					mapping[i] = rev_val
					mapping[rev_idx] = val
					get_last_nonfree = False

	raise Exception('something went wrong, mapping should have returned')


def calc_checksum(mapping):
	checksum = 0
	for i, val in mapping.items():
		if type(val) is int:
			checksum += i*val
	return checksum


def p1(file):
	s = read_file(file)

	mapping = parse_disk(s)
	sorted_mapping = sort_from_end(mapping)

	#print('Sorted mapping:')
	#print(''.join([str(x) for x in sorted_mapping.values()]))

	print(f'Checksum: {calc_checksum(sorted_mapping)}')



def sort_from_end_whole(disk_string):
	'''
	start with original disk string (keeping track of which are files, which are free spaces, and what the original ID numbers were). 
	sort dense format backwards
	'''

	# Parse

	files = [] #start index: (filelength, original file ID)
	free_spaces = [] #start index: free space length
	expanded_index = 0

	for i, char in enumerate(list(disk_string)):
		if i%2 == 0:
			#print(f'Assigning file char {char} at index {i}, {expanded_index = }')
			files.append((expanded_index, int(char), int(i//2))) #int(char) is the file length, and int(i//2) is the file ID (contents of the file)
		else:
			#print(f'Assigning free space char {char} at index {i}, {expanded_index = }')
			free_spaces.append([expanded_index, int(char)]) #int(char) is the length of the free space
		expanded_index += int(char)

	checksum = 0
	files.reverse()

	for (fileidx, filelength, filevalue) in files: # starting with the last file, attempt to move
		moved = False
		for i, (space_idx, space_length) in enumerate(free_spaces):
			if filelength <= space_length and fileidx > space_idx and not moved:
				#print(f'Moving file at index {fileidx} of length {filelength} and value {filevalue} to free space at index {space_idx} of length {space_length}')
				moved = True
				for idx in range(space_idx, space_idx + filelength):
					#print(idx)
					checksum += idx * filevalue
					#print(f'Incremented checksum by {idx} x {filevalue} = {idx * filevalue}')
					free_spaces[i][0] += 1 # increment the start position of the free space
					free_spaces[i][1] -= 1 # decrease available free space length by 1

		if not moved:
			#print(f'File at index {fileidx} of length {filelength} and value {filevalue} was not moved')
			for idx in range(fileidx, fileidx+filelength):
				checksum += idx * filevalue
				#print(f'Incremented checksum by {idx} x {filevalue} = {idx * filevalue}')


	return files, free_spaces, checksum

def p2(file):
	disk_string = read_file(file)
	files, free_spaces, checksum = sort_from_end_whole(disk_string)
	print(f'p2 checksum: {checksum}')
	return files, free_spaces, checksum




if __name__ == '__main__':
	test_file = 'test_data_day9.txt'
	real_file = 'data_day9.txt'
	
	#p1(real_file)
	files, free_spaces, checksum = p2(real_file)
	
	


