from utils import input_from_stream

def part1(xs):
    return min([sum([abs(x - n) for x in xs]) for n in range(0, max(xs)-min(xs))])

def part2_shorter(xs):
    return min([int(sum([abs(x - n) * (abs(x - n) + 1)/2 for x in xs])) for n in range(0, max(xs)-min(xs))])

def part2(xs):
    # Moving 1 step costs 1, 2 steps cost 1+2=3, 3 steps costs 1+2+3=6, ...
    costs = [0]*max(xs)*2
    for moves in range(1, len(costs)):
        costs[moves] = costs[moves-1] + moves

    # Calculate sum of all moving costs for each potential #moves, 
    # and pick #moves which results in lowest moving cost
    return min([sum([costs[abs(x - n)] for x in xs]) for n in range(0, max(xs)-min(xs))])


xs = [int(f) for f in input_from_stream()[0].split(',')]

print(f'Part 1: {part1(xs)}')
print(f'Part 2: {part2(xs)}')
print(f'Part 2 (shorter solution): {part2_shorter(xs)}')
