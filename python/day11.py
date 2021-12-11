from collections import deque
from utils import input_from_stream

class IntMatrix:

    def __init__(self, rows):
        # Sanity check - each row must be equally long
        for idx, row in enumerate(rows):
            if idx > 0:
                assert(len(row) == len(rows[idx-1]))

        # Note to self: in a more realistic use case, we would like to make sure
        # we do a COPY of parameter data, as this is a mutable data structure...
        self.rows = rows

    def nrows(self):
        return len(self.rows)

    def ncols(self):
        return len(self.rows[0])

    def neighbours(self, row, col, radius=1):
        result = []
        offsets = []

        # All relative neighbours (based on radius)
        for i in range(-radius, radius+1):
            for j in range(-radius, radius+1):
                if not (i == 0 and j == 0):
                    offsets.append((i,j))

        # Get all neighbour coordinates within bounds        
        for o in offsets:
            r = row + o[0]
            c = col + o[1]
            if r in range(0, self.nrows()) and c in range(0, self.ncols()):
                result.append((r, c))

        return result

    def get_all_matching(self, predicate):
        result = []
        for r in range(self.nrows()):
            for c in range(self.ncols()):
                if predicate(self.get(r, c)):
                    result.append((r, c))

        return result

    def get(self, row, col):
        return self.rows[row][col]

    def set(self, row, col, val):
        self.rows[row][col] = val

    def print(self):
        for row in self.rows:
            print(row)

    # Note to self: 
    # The following two methods are specific to the use case.
    # They should not be part of a reusable data structure 
    # but implemented outside of data structure (by caller) 
    def inc_all(self):
        for r in range(self.nrows()):
            for c in range(self.ncols()):
                self.rows[r][c] += 1

    def inc(self, row, col):
        self.rows[row][col] += 1


def trigger_flashes(matrix: IntMatrix):
    n_flashes = 0
    d = deque()

    # Increase all by 1
    matrix.inc_all()

    # Queue up all positions that will flash
    flashing = matrix.get_all_matching(lambda x: x == 10)
    for f in flashing:
        d.appendleft(f)

    # Flash, update neighbours and continue until no more positions trigger a flash
    while d:
        n_flashes += 1
        f = d.pop()
        matrix.inc(*f)
        for n in matrix.neighbours(*f):
            matrix.inc(*n)
            if matrix.get(*n) == 10:
                d.appendleft(n)

    # Set all > 10 to 0
    for flashed in matrix.get_all_matching(lambda x : x >= 10):
        matrix.set(*flashed, 0)

    return n_flashes


def part1(matrix: IntMatrix):
    n_flashes = 0

    for step in range(100):
        n_flashes += trigger_flashes(matrix)

    return n_flashes

def part2(matrix):
    step = 1
    while trigger_flashes(matrix) != 100:
        step += 1

    return step

lines = input_from_stream()

print(f'Part 1: {part1(IntMatrix([[int(x) for x in line] for line in lines]))}')
print(f'Part 2: {part2(IntMatrix([[int(x) for x in line] for line in lines]))}')
