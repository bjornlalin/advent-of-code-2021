from collections import deque
from utils import input_from_stream

class IntMatrix:

    def __init__(self, rows):
        # Sanity check - each row must be equally long
        for idx, row in enumerate(rows):
            if idx > 0:
                assert(len(row) == len(rows[idx-1]))

        self.rows = rows

    def nrows(self):
        return len(self.rows)

    def ncols(self):
        return len(self.rows[0])

    def neighbours(self, row, col):
        result = []
        # left
        if col > 0:
            result.append((row, col-1))
        # right
        if col < self.ncols() - 1:
            result.append((row, col+1))
        # up
        if row > 0:
            result.append((row-1, col))
        # down
        if row < self.nrows() - 1:
            result.append((row+1, col))

        return result

    def at(self, row, col):
        return self.rows[row][col]

    def lowpoints(self):
        lowpoints = []

        for row in range(map.nrows()):
            for col in range(map.ncols()):
                neighbours = map.neighbours(row, col)
                neighbour_heights = [map.at(*n) for n in neighbours]
                is_lowpoint = len([h for h in neighbour_heights if h <= map.at(row, col)]) == 0
                if is_lowpoint:
                    lowpoints.append((row, col))

        return lowpoints


def part1(map: IntMatrix):
    lowpoints = map.lowpoints()
    return sum([map.at(*lowpoint) + 1 for lowpoint in lowpoints])
    
# From each low point, find all neighbours which are higher and < 9, and add them to the 
# list of next points to visit. From each such point, do the same. Continue until there
# are no more items left to visit. Now all points we have visited should be the basin.
# (Graph BFS using a dequeue)
def part2(map: IntMatrix):

    basins = []

    # Start a BFS from each low point
    for lowpoint in map.lowpoints():
        basin = set()
        d = deque()

        d.appendleft(lowpoint)

        while d: # as long as the deque is not empty...
            pos = d.pop()

            # Add the item to the basin ...
            basin.add(pos)

            # get all neighbours which belong to basin (if they are not already visited) ...
            neighbours_to_add_to_basin = [n for n in map.neighbours(*pos) if n not in basin and map.at(*n) > map.at(*pos) and map.at(*n) < 9]

            # Continue BFS to build basin ...
            d.extendleft(neighbours_to_add_to_basin)

        basins.append(basin)

    basin_lengths = [len(basin) for basin in basins]
    basin_lengths.sort(reverse=True)

    return basin_lengths[0] * basin_lengths[1] * basin_lengths[2]



lines = input_from_stream()
rows_of_ints = [[int(x) for x in line] for line in lines]
map = IntMatrix(rows_of_ints)

print(f'Part 1: {part1(map)}')
print(f'Part 2: {part2(map)}')
