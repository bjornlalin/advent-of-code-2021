from collections import deque, Counter
from utils import input_from_stream

def _debug(str):
    if False:
        print(str)

def fire(dx, dy, x_range, y_range):
    x, y, y_max = 0, 0, 0

    _debug(f'Firing with initial velocity: ({dx}, {dy})')

    # As long as we did not overshoot...
    while x <= x_range[1] and y >= y_range[0]:
        x, y = x+dx, y+dy
        y_max = max(y, y_max)

        _debug(f'  velocity: ({dx}, {dy}) => pos ({x},{y}) [y_max = {y_max}]')

        # Landed within the target area
        if x in range(x_range[0], x_range[1] + 1) and y in range(y_range[0], y_range[1] + 1):
            _debug('  -> landed within target area after reaching highest point at y = {y_max}!')
            return y_max

        dx, dy = max(0, dx - 1), dy - 1

    # Missed the target area
    return -1

def search(x_range, y_range):
    hits = {}
    for vel_x in range(0, x_range[1] + 1):
        for vel_y in range(y_range[0], 100): # 100 selected by trial & error
            y_max = fire(vel_x, vel_y, x_range, y_range)
            if y_max != -1:
                hits[(vel_x, vel_y)] = y_max

    return hits

# Test input
x_range = (20, 30)
y_range = (-10, -5)

# Actual input
x_range = (253, 280)
y_range = (-73, -46)

# Search entire space of plausible initial (dx,dy) 
hits = search(x_range, y_range)

print(f'Part 1: {max(hits.values())}')
print(f'Part 2: {len(hits.keys())}')
