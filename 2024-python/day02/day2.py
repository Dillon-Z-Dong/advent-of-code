import pandas as pd
import numpy as np

#Problem 1

def problem1(df):
	'''
	Do columnwise computations checking difference and save the sign of the first difference

	- difference >= 1 and <= 3
	- all increasing or all decreasing

	Mask along the way
	'''

	#Column iteration
	n_cols = df.shape[1]
	col_generator = df.items()

	# initialize current_col with first column
	current_col = np.array(next(col_generator)[1])

	#Initialize array of "safe reports" (rows)
	safe_rows = np.ones_like(current_col)

	# Iterate over columns checking conditions
	for i in range(n_cols-1):
		print(f'Iteration {i}: total number of safe rows: {np.sum(safe_rows)}')
		next_col = np.array(next(col_generator)[1])
		diff = next_col - current_col
		if i == 0:
			first_sign = diff > 0

		# Check which rows np.abs(diff) >= 1 and <= 3 and sign is same as original. nans are automatically ok (no new data)
		sign = diff > 0
		min_diff = (np.abs(diff) >= 1)
		max_diff = (np.abs(diff) <= 3)
		same_sign = (sign == first_sign)
		safe_mask = (min_diff & max_diff & same_sign) | np.isnan(diff)

		# Multiply safe_rows by safe_mask which will act like a sieve, preserving ones and keeping any 0 at 0
		safe_rows *= safe_mask

		# Save the current next_col and repeat
		current_col = next_col

	print(f'Total number of safe rows: {np.sum(safe_rows)}')
	return safe_rows


# Problem 2

def check_row(arr): 
	'''
	Input arr, checks to see whether it satisfies all the rules. 
		- np.abs(diff) >= 1
		- np.abs(diff) <= 3
		- monotonic

	Returns True if next element is nan, else False
	'''

	# Convert to np array and drop nans (which are all at the back)
	arr = np.array(arr)
	arr = arr[np.where(np.isnan(arr) == False)]

	# Check monotonic
	sorted_arr = np.sort(arr)
	if np.all(arr == sorted_arr) or np.all(arr == np.flip(sorted_arr)):
		pass
	else:
		return False
	
	# Check diffs
	diff = np.abs(arr[1:] - arr[:-1])
	if np.nanmin(diff) < 1 or np.nanmax(diff) > 3:
		return False

	return True


def check_row_with_drop(row):
	'''
	Input list
	Tries check_row on full row and all subsets of the row
	If any succeed return True
	else return False
	'''

	# Try full row
	if check_row(row):
		return True

	else: # try combinations missing one element
		for i in range(len(row)):
			subrow = row[:i] + row[i+1:]
			if check_row(subrow):
				return True

	return False


def problem2(df):
	success = []
	count = 0
	for row in df.iterrows():
		row = list(row[1])
		if check_row_with_drop(row):
			count += 1
			success.append(True)
		else:
			success.append(False)

	print(f'Number of safe rows allowing one drop: {count}')

	return success

if __name__ == '__main__':
	df = pd.read_csv('data_day2.txt',header = None, sep = "\\s+")
	safe_rows = problem1(df)
	safe_rows2 = problem2(df)

# how to handle nans?