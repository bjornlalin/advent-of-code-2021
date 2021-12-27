import re
from collections import defaultdict, deque
from utils import input_from_stream

class IntMatrix:

    def __init__(self, rows):
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
        offsets.append((0, -1))
        offsets.append((0, 1))
        offsets.append((-1, 0))
        offsets.append((1, 0))
        
        # Get all neighbour coordinates within bounds        
        for o in offsets:
            r = row + o[0]
            c = col + o[1]
            if r in range(0, self.nrows()) and c in range(0, self.ncols()):
                result.append((r, c))

        return result

    def get(self, row, col):
        return self.rows[row][col]

    def set(self, row, col, val):
        self.rows[row][col] = val

    def copy(self):
        cpy = []
        for r in range(self.nrows()):
            row = []
            for c in range(self.ncols()):
                row.append(self.get(r, c))
            cpy.append(row)

        return IntMatrix(cpy)

    def copy_and_inc_1(self):
        cpy = self.copy()
        for r in range(cpy.nrows()):
            for c in range(cpy.ncols()):
                val = (cpy.get(r,c) + 1) % 10
                if val == 0:
                    val = 1
                cpy.set(r, c, val)

        return cpy

    def print(self):
        for row in self.rows:
            print(row)

def _djikstra(node, matrix: IntMatrix, scores):
    d = deque()
    d.append(node)

    while d:
        visiting = d.pop()
        next = matrix.neighbours(*visiting)
        for n in next:
            if not n == (0,0):
                score_n = scores[visiting] + matrix.get(*n)
                if scores[n] > score_n:
                    scores[n] = score_n
                    d.appendleft(n)

def solve(matrix: IntMatrix):
    start = (0, 0)
    scores = defaultdict(lambda : 10000000)
    scores[start] = 0

    _djikstra(start, matrix, scores)

    return scores[(matrix.nrows()-1,matrix.ncols()-1)]


# Read input
lines = input_from_stream()

matrix1 = IntMatrix([[int(x) for x in line] for line in lines])

# Build all matrices to copy together into a bigger one
matrices = []
matrices.append(matrix1.copy())
for i in range(1, 9):
    matrices.append(matrices[i-1].copy_and_inc_1())

# Create a large 2-d array of ints
large = []
for r in range(5 * matrices[0].nrows()):
    large.append([])
    for c in range(5 * matrices[0].nrows()):
        large[r].append(0)

# Copy the matrix entries into large array
for block_r in range(5):
    for block_c in range(5):
        m = matrices[block_r + block_c]
        for r in range(m.nrows()):
            for c in range(m.ncols()):
                large[block_r * m.nrows() + r][block_c * m.ncols() + c] = m.get(r, c)

matrix2 = IntMatrix(large)
matrix2.print()

print(f'Part 1: {solve(matrix1)}')
print(f'Part 2: {solve(matrix2)}')
