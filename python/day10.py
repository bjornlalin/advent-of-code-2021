from collections import deque
from utils import input_from_stream

OPEN = set(['(', '{', '[', '<'])
CLOSE = set([')', '}', ']', '>'])
CLOSING = { '(' : ')', '[' : ']', '{' : '}', '<' : '>' }

def score1(corrupt_char):
    SCORES_1 = { ')' : 3, ']' : 57, '}' : 1197, '>' : 25137 }
    return SCORES_1[corrupt_char]

def score2(missing_to_close):
    SCORES_2 = { ')' : 1, ']' : 2, '}' : 3, '>' : 4 }
    score = 0
    for val in missing_to_close:
        score = score * 5 + SCORES_2[val]

    return score

def corrupted(line):
    d = deque()

    for c in line:
        if c in OPEN:
            d.append(c)
        elif c in CLOSE:
            if CLOSING[d.pop()] != c:
                return c

    return None

def invalid(line):
    d = deque()

    for c in line:
        if c in OPEN:
            d.append(c)
        elif c in CLOSE:
            d.pop()
    
    needed_to_close = []
    while d:
        needed_to_close.append(CLOSING[d.pop()])

    return needed_to_close

def part1(lines):
    total = 0
    
    for line in lines:
        corrupt_char = corrupted(line)
        if corrupt_char:
            total += score1(corrupt_char)
    
    return total

def part2(lines):

    scores = []

    for line in lines:
        if not corrupted(line):
            missing = invalid(line)
            scores.append(score2(missing))

    return sorted(scores)[int(len(scores)/2.)]

lines = input_from_stream()

print(f'Part 1: {part1(lines)}')
print(f'Part 2: {part2(lines)}')
