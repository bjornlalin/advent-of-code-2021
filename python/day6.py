from utils import input_from_stream

def part1(fish, days):

    all_fish = fish.copy()

    # Run simulation
    for day in range(0, days):
        updated_fish = []
        new_fish = []
        for f in all_fish:
            if f == 0:
                updated_fish.append(6)
                new_fish.append(8)
            else:
                updated_fish.append(f-1)
        
        all_fish = updated_fish + new_fish

    return len(all_fish)

# Problem grows too fast to simulate / keep individual fish in memory
# Find recursive expression and store already-solved sub-problems in memory (DP)
def part2(fish, days):
    
    n_fish = 0
    memory = {}

    for f in fish:
        # Each fish exists (+1) and produces new fish after 'f' days. Sum up all those + their descendents
        n_fish = n_fish + 1 + sum([fish_with_offspring(d, memory) for d in range(days-f, 0, -7)])

    return n_fish

# The number of offspring produced with 'days' days remaining
# Count offspring itself + each of my children and the offspring they produce (recursive step)
def fish_with_offspring(days, memory):
    if not days in memory:
        memory[days] = 1 + sum([fish_with_offspring(d, memory) for d in range(days-9, 0, -7)])

    return memory[days]


fish = [int(f) for f in input_from_stream()[0].split(',')]

print(f'Part 1: {part1(fish, 80)}')
print(f'Part 2: {part2(fish, 256)}')
