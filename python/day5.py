from utils import input_from_stream
from geom import Point, Line

class LineDay5 (Line):

    def points_on_line(self, include_diag=False):
        if not (self.is_straight() or self.is_diagonal()):
            raise Exception('This method only supports vertical, horizontal or diagonal lines')

        dx = 0 if self.p1.x == self.p2.x else (1 if self.p1.x < self.p2.x else -1)
        dy = 0 if self.p1.y == self.p2.y else (1 if self.p1.y < self.p2.y else -1)
        len = max(abs(self.p1.x - self.p2.x), abs(self.p1.y - self.p2.y))
        points = [Point(self.p1.x + (i * dx), self.p1.y + (i * dy)) for i in range(0,len+1)]
        #print(f'These points {points} are on line {self}')

        if self.is_straight() or (self.is_diagonal() and include_diag):
            return points

        return []

def part1(lines):
    return part_both(lines, include_diag=False)

def part2(lines):
    return part_both(lines, include_diag=True)

def part_both(lines, include_diag):
    counts = dict()
    for line in lines:
        for point in line.points_on_line(include_diag=include_diag):
            counts[point] = counts.get(point, 0) + 1
    
    return len([count for count in counts.values() if count > 1])


########################
# Execution starts here
########################

lines = []

for input in input_from_stream():
    pairs = input.replace(' ','').split('->')
    point1 = Point(int(pairs[0].split(',')[0]), int(pairs[0].split(',')[1]))
    point2 = Point(int(pairs[1].split(',')[0]), int(pairs[1].split(',')[1]))
    line = LineDay5(point1, point2)

    lines.append(line)

print(f'Part 1: {part1(lines)}')
print(f'Part 2: {part2(lines)}')
