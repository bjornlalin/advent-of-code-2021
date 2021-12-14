import re
from collections import defaultdict, deque, Counter
from utils import input_from_stream

def simulate(template, rules, steps):
    poly = template
    for _ in range(steps):
        poly2 = poly[0]
        pairs = [poly[i:i+2] for i in range(len(poly)-1)]
        for pair in pairs:
            poly2 += rules[pair] + pair[1]
        
        poly = poly2
    
    return poly


def part1(template, rules):
    poly =  simulate(template, rules, 10)
    counts = Counter(poly).most_common()

    return counts[0][1] - counts[-1][1]

def part2(template, rules, reverse_rules):

    # These are all letters that can occur
    all_letters = set([t for t in template] + [t for t in reverse_rules.keys()])

    # Count occurrances of pairs and letters
    n_letters = [defaultdict(lambda: 0) for _ in range(41)]
    n_pairs = [defaultdict(lambda: 0) for _ in range(41)]

    # Bootstrap for the first word    
    n_pairs[0] = Counter([template[i:i+2] for i in range(len(template)-1)])
    n_letters[0] = Counter([l for l in template])

    # Sum up:
    # #N[step] = #N[step-1] + #XX[step-1] for all XX which can produce an N
    # #NN[step] = all pairs produced from the pairs in step-1
    for step in range(1, 41):
        for l in all_letters:
            n_letters[step][l] = n_letters[step-1][l] + sum([n_pairs[step-1][pair] for pair in reverse_rules[l]])
        for (pair, n) in n_pairs[step-1].items():
            pair1 = pair[0] + rules[pair]
            pair2 = rules[pair] + pair[1]
            n_pairs[step][pair1] += n
            n_pairs[step][pair2] += n
        
    counts = Counter(n_letters[40]).most_common()
    return counts[0][1] - counts[-1][1]

lines = input_from_stream()

template = lines[0]

rules = {}
reverse_rules = {}

for line in lines[2:]:
    a = line.split("->")[0].replace(' ', '')
    b = line.split("->")[1].replace(' ', '')
    rules[a] = b
    if b not in reverse_rules.keys():
        reverse_rules[b] = [a]
    else:
        reverse_rules[b] += [a]

print(f'Part 1: {part1(template, rules)}')
print(f'Part 2: {part2(template, rules, reverse_rules)}')
