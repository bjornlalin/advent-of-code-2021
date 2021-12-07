import sys

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
