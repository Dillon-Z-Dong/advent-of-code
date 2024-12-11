# day5.py

def get_rules(file = 'rules_day5.txt'):
	with open(file) as f:
		lines = f.readlines()

	rules = [line.strip().split('|') for line in lines]
	return rules

def compile_violations(rules):
	'''map where if d[key] contains val and key comes before val, it's a violation'''
	d = {}
	for rule in rules:
		early, late = rule
		if late not in d.keys():
			d[late] = [early]
		else:
			d[late].append(early)

	return d

def read_lines(file = 'data_day5.txt'):
	with open(file) as f:
		lines = f.readlines()
	return [line.strip().split(',') for line in lines]


def check_line_and_get_center(line, violations):
	for i, page1 in enumerate(line):
		if page1 not in violations:
			continue
		else:
			remainder = line[i:]
			for page2 in remainder:
				if page2 in violations[page1]:
					return 0
	return int(line[len(line)//2])


def p1(lines, violations):
	middle_sum = 0
	for line in lines:
		middle_sum += check_line_and_get_center(line, violations)
	print(f'Middle sum: {middle_sum}')



def is_not_allowed(early,late,violations):
	if early not in violations.keys():
		return False

	elif late not in violations[early]:
		return False

	else:
		return True


def get_last_element(line, violations):
	'''
	start from the end and work backwards. 
	last one is the first entry that is not a violation for any of the others
	second to last one is the first entry that is not a violation for any of the ones except the last one
	etc.
	'''

	for early in line:
		if sum([is_not_allowed(early, page,violations) for page in line]) == 0:
			line.remove(early)
			return early, line


def reorder_line_and_get_center(line, violations):		
	reverse_allowed = []
	for _ in range(len(line)):
		early, line = get_last_element(line, violations)
		reverse_allowed.append(early)

	center = reverse_allowed[len(reverse_allowed)//2]
	return int(center)



def p2(lines, violations):
	middle_sum = 0
	for line in lines:
		if check_line_and_get_center(line,violations):
			continue
		else:
			middle_sum += reorder_line_and_get_center(line, violations)

	print(f'Middle sum: {middle_sum}')


if __name__ == '__main__':
	rules = get_rules()
	lines = read_lines()
	violations = compile_violations(rules)

	p1(lines,violations)
	p2(lines,violations)




