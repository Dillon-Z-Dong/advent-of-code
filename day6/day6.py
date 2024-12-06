# day6.py
import numpy as np
from tqdm import tqdm

class patrol():

	def __init__(self, input_file):
		self.guard_position = None
		self.guard_orientation = 'up'
		self.map = None
		self.map_shape = None
		self.load_map(input_file)


	def load_map(self, input_file):
		with open(input_file) as f:
			lines = [list(line.strip()) for line in f.readlines()] 

		arr = np.array(lines)
		self.map_dimensions = np.shape(arr)
		self.guard_position = np.where(arr == '^')
		self.map = arr
		self.map[self.guard_position] = 'X'
		self.map_shape = self.map.shape
		self.move_counter = 0

	
	def turn(self):
		'''rotates 90 deg to the right'''
		if self.guard_orientation == 'up':
			self.guard_orientation = 'right'
		elif self.guard_orientation == 'right':
			self.guard_orientation = 'down'
		elif self.guard_orientation == 'down':
			self.guard_orientation = 'left'
		elif self.guard_orientation == 'left':
			self.guard_orientation = 'up'


	def move_and_update_map(self):
		'''If there is something directly in front of you, turn right 90 degrees.
			Otherwise, take a step forward.'''
		guard_y, guard_x = self.guard_position[0][0], self.guard_position[1][0]

		if self.guard_orientation == 'up':
			next_position = (np.array([guard_y - 1]),np.array([guard_x]))
		elif self.guard_orientation == 'right':
			next_position = (np.array([guard_y]),np.array([guard_x + 1]))
		elif self.guard_orientation == 'down':
			next_position = (np.array([guard_y + 1]),np.array([guard_x]))
		elif self.guard_orientation == 'left':
			next_position = (np.array([guard_y]),np.array([guard_x -1]))


		if next_position[0][0] < 0 or next_position[0][0] >= self.map_shape[0] or next_position[1][0] < 0 or next_position[1][0] >= self.map_shape[1]:
			return False #out of bounds

		elif self.move_counter > self.map_shape[0] * self.map_shape[1]:
			raise Exception('Infinite loop!') # better to keep track of orientation state but this should work


		elif self.map[next_position] == '#':
			self.turn() 
			return True #turn due to obstacle

		elif self.map[next_position] in ['.','X']: 
			self.map[next_position] = 'X'
			self.guard_position = next_position
			return True #move forward one step and record that you were there in that orientation


	def p1(self, verbose = False):
		run = True
		while run:
			run = self.move_and_update_map()
			self.move_counter += 1

		if verbose:
			print(f'Final map:\n\n {self.map}')
			print(f'Number of Xs: {len(np.where(self.map == 'X')[0])}')
			print(f'Number of moves: {self.move_counter}')



	def p2(self):
		inf_loop_counter = 0
		total_iterations = self.map_shape[0] * self.map_shape[1]

		with tqdm(total=total_iterations, desc="Processing map") as pbar:
			for x in range(self.map_shape[0]):
				for y in range(self.map_shape[1]):
					self.__init__(input_file)
					obstacle_position = (np.array([y]), np.array([x]))
					if self.map[obstacle_position] != '.':
						pbar.update(1)
						continue
					else:
						self.map[obstacle_position] = '#'
						try:
							self.p1()
						except:
							inf_loop_counter += 1
					pbar.update(1)


		print(f'Number of infinite loops found: {inf_loop_counter}')







input_file = 'data_day6.txt'
#input_file = 'test_data_day6.txt'

pat = patrol(input_file)
#pat.p1()
pat.p2()


