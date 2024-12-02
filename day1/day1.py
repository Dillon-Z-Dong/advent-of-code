#day1.py

import numpy as np
import pandas as pd
from collections import Counter

d1_data = pd.read_csv('day1_data.txt', sep = "\\s+", names = ['left','right'])

def problem1(df):
	diff = np.sum(np.abs(np.sort(df.right) - np.sort(df.left))) #np.abs so that the difference is always positive (order doesn't matter)
	return diff


def problem2(df):
	total_count = 0
	right_counts = Counter(df.right)
	for k in df.left:
		total_count += k*right_counts.get(k,0)

	return total_count

if __name__ == '__main__':
	print(f'Problem 1: sum of abs(differences) = {problem1(d1_data)}')
	print(f'Problem 2: similarity score = {problem2(d1_data)}')