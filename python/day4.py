import sys
from utils import input_from_stream

class Board:

    def __init__(self, board_nums) -> None:
        self.rows = [set(board_nums[n*5:n*5+5]) for n in range(0, 5)]
        self.cols = [set(board_nums[n:len(board_nums)+1:5]) for n in range(0, 5)]
        self.all = set().union(*self.rows)

    def bingo(self, drawn):
        drawn_set = set(drawn)
        for row in self.rows:
            if len(drawn_set.intersection(row)) == 5:
                return True
        for col in self.cols:
            if len(drawn_set.intersection(col)) == 5:
                return True

    def unmarked(self, drawn):
        return self.all.difference(drawn)

def part1(bingo_num_generator, boards):
    for drawn in bingo_num_generator:
        winners = [board for board in boards if board.bingo(drawn)]
        
        # If we have found a winner, calculate answer
        if len(winners) > 0:
            return sum(winners[0].unmarked(drawn)) * drawn[-1]

def part2(bingo_num_generator, boards):
    for drawn in bingo_num_generator:
        winners = [board for board in boards if board.bingo(drawn)]

        # Remove any boards which received 'bingo' already
        for winner in winners:
            boards.remove(winner)

        # If there are none left we are done - pick the last winner (i.e. the loser) and calculate answer
        if len(boards) == 0:
            return sum(winners[0].unmarked(drawn)) * drawn[-1]

########################
# Execution starts here
########################

import re

# Read all input
lines = input_from_stream(sys.stdin)

# Remove empty lines
lines = [line for line in lines if len(line.replace(r'\s+', '')) > 0]

# Get the first line 
numbers = [int(n) for n in lines[0].replace('\n', '').replace(' ', '').split(',')]

def create_bingo_drawer(numbers):
    for n in range(0, len(numbers)):
        yield numbers[:n+1]

# Flatten each board input into 1-D list (Board class constructor expects that representation)
def create_board(lines):
    board_nums = [int(n) for line in lines for n in re.findall(r'\S+', line)]
    return Board(board_nums)        

# Read 5 lines each to fetch boards and construct Board instance
boards = [create_board(lines[idx:idx+5]) for idx in range(1, len(lines), 5)]

# Solve puzzles
print(f'Part 1: {part1(create_bingo_drawer(numbers), boards)}')
print(f'Part 2: {part2(create_bingo_drawer(numbers), boards)}')
