import re

def load(file):
    with open(file) as f:
        return [x.strip() for x in f.readlines()]

def p1(data):
    """Simple regex for finding single digits"""
    pattern = r'(\d)'

    total = 0
    for t in data:
        p = re.findall(pattern,t)
        total += int(p[0]+p[-1])

    print(total)
    return

def p2(data):
    """Important to use (?=(...)) in the regex to handle the overlap matching case"""
    pattern = r'(?=(one|two|three|four|five|six|seven|eight|nine|\d))'

    def digit(digit_str):
        digit_map = {'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9}
        if digit_str in ['1','2','3','4','5','6','7','8','9']:
            return digit_str
        else:
            return str(digit_map[digit_str])

    total = 0
    for t in real:
        p = [match.group(1) for match in re.finditer(pattern,t)]
        digit_combo = int(digit(p[0])+digit(p[-1]))
        print(t, p, digit_combo)
        total += digit_combo

    print(total)
    return

if __name__ == '__main__':
    test = load(f'test_data_day1.txt')
    real = load(f'data_day1.txt')

    p1(real)
    p2(real)
