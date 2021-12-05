class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x},{self.y})'

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def __hash__(self) -> int:
        return (self.x, self.y).__hash__()

class Line:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __str__(self) -> str:
        return f'{self.p1} -> {self.p2}'

    def __eq__(self, __o: object) -> bool:
        return self.p1 == __o.p1 and self.p2 == __o.p2

    def __hash__(self) -> int:
        return (self.p1, self.p2).__hash__()

    def is_straight(self):
        return self.is_horizontal() or self.is_vertical()

    def is_horizontal(self):
        return self.p1.y == self.p2.y

    def is_vertical(self):
        return self.p1.x == self.p2.x

    def is_diagonal(self):
        return abs(self.p1.x - self.p2.x) == abs(self.p1.y - self.p2.y)