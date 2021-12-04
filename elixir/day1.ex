import sys

def diffs(measures):
    return [measures[i+1] - measures[i] for i in range(0, len(measures)-1)]

def sliding_window_avg(measures):
    return [measures[i+2] + measures[i+1] + measures[i] for i in range(0, len(measures)-2)]

def increases(measures):
    return sum([1 if measure > 0 else 0 for measure in measures])

########################
# Here execution starts
########################

measures = []
inc_1 = 0
inc_2 = 0

for line in sys.stdin:
    measures.append(int(line))

print(f'Part 1: There are {increases(diffs(measures))} increases')
print(f'Part 2: There are {increases(diffs(sliding_window_avg(measures)))} increases')