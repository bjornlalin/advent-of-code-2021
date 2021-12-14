from collections import deque
from utils import input_from_stream

def fold(coords, fold):
    if fold[0] == 'x':
        return fold_x(coords, fold[1])
    else:
        return fold_y(coords, fold[1])

def fold_y(coords, y):
    coords_after = [coord for coord in coords if coord[1] < y]
    for coord in [coord for coord in coords if coord[1] > y]:
        new_y = coord[1] - 2 * (coord[1] - y)
        coords_after.append((coord[0], new_y))

    return coords_after

def fold_x(coords, x):
    coords_after = [coord for coord in coords if coord[0] < x]
    for coord in [coord for coord in coords if coord[0] > x]:
        new_x = coord[0] - 2 * (coord[0] - x)
        coords_after.append((new_x, coord[1]))

    return coords_after

def part1(coords, folds):
    return len(set(fold(coords, folds[0])))

def part2(coords, folds):
    c = coords
    for f in folds:
        c = fold(c, f)

    # Build message string for printing
    max_x = max([_c[0] for _c in c])
    max_y = max([_c[1] for _c in c])
    msg = (max_y+1) * [""]
    for y in range(0, max_y+1):
        for x in range(0, max_x+1):
            if (x,y) in c:
                msg[y] += "*"
            else:
                msg[y] += " "

    # Print code to console
    for m in msg:
        print(m)


lines = input_from_stream()
coords = []
folds = []

for line in lines:
    if line.startswith('fold'):
        folds.append((line.split("=")[0][-1:], int(line.split("=")[1])))
    elif not len(line) == 0:
        coords.append((int(line.split(",")[0]),int(line.split(",")[1])))

print(f'Part 1: {part1(coords, folds)}')
print(f'Part 2: {part2(coords, folds)}')
