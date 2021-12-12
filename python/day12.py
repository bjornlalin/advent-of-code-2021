from collections import deque, Counter
from utils import input_from_stream

def is_small(_cave):
    return _cave.lower() == _cave

def has_2_small_caves(path):
    path_small_caves_only = [p for p in path if is_small(p)]
    return len(path_small_caves_only) > len(set(path_small_caves_only))

def visit(node, path, graph):

    if node == 'start' and len(path) > 0:
        return 0

    if node == 'end':
        return 1

    # we've already been here...
    if (node in path and is_small(node)):
        return 0

    return sum([visit(n, path + [node], graph) for n in graph[node]])

def visit2(node, path, graph):

    if node == 'start' and len(path) > 0:
        return 0

    if node == 'end':
        return 1

    # we've already been here, and have visited another small cave twice on this path...
    if (node in path and is_small(node) and has_2_small_caves(path)):
        return 0

    return sum([visit2(n, path + [node], graph) for n in graph[node]])

def part1(graph):
    return visit('start', [], graph)

def part2(graph):
    return visit2('start', [], graph)

graph = {}
lines = input_from_stream()

for line in lines:
    v1, v2 = line.split('-')

    if not v1 in graph.keys():
       graph[v1] = [v2]
    else:
        graph[v1].append(v2)

    if not v2 in graph.keys():
       graph[v2] = [v1]
    else:
        graph[v2].append(v1)

print(f'Part 1: {part1(graph)}')
print(f'Part 2: {part2(graph)}')
