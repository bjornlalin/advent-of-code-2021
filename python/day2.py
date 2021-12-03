import sys

def diffs(measures):
    return [measures[i+1] - measures[i] for i in range(0, len(measures)-1)]

def sliding_window_avg(measures):
    return [measures[i+2] + measures[i+1] + measures[i] for i in range(0, len(measures)-2)]

def increases(measures):
    return sum([1 if measure > 0 else 0 for measure in measures])

cmds = [line for line in sys.stdin]

# Part 1
pos = 0
depth = 0

for cmd in cmds:
    dir = cmd.split(' ')[0]
    len = int(cmd.split(' ')[1])

    if dir == 'forward':
        pos += len
    else:
        depth = depth + (-len if dir == 'up' else len)

print(f'Part 1: {depth * pos}')

# Part 2
pos = 0
depth = 0
aim = 0

for cmd in cmds:
    dir = cmd.split(' ')[0]
    len = int(cmd.split(' ')[1])

    if dir == 'aim':
        aim = int(len)
    elif dir == 'forward':
        pos += len
        depth += len * aim
    else:
        aim = aim + (-len if dir == 'up' else len)

print(f'Part 2: {depth * pos}')
