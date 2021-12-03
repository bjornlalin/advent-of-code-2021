import sys
from utils import bitstring_to_base10, bitstring_inverse, input_from_stream

# Same solution by converting to a 1/0 matrix (NumPy) and then using that
# to do column-wise operations (instead of looping)
def part1_np(bitstrings):
    import numpy as np
    
    n_bits = len(bitstrings[0])
    n_vals = len(bitstrings)

    # Split into bits and reshape into 2-d array with #bits columns and #measurements rows
    matrix = np.array([[int(bit) for bit in bitstr] for bitstr in bitstrings])
    matrix.reshape(n_bits, n_vals)

    # If the majority of bits in a column are 1, then gamma is 1 at that position (average >= .5 in column)
    gamma_bitstr = ''.join(['1' if x else '0' for x in np.average(matrix, axis=0) >= .5])

    # Convert to base-10 and calculate epsilion
    gamma = bitstring_to_base10(gamma_bitstr)
    epsilon = bitstring_to_base10(bitstring_inverse(gamma_bitstr))

    # alternative calculation of epsilon (inverse), probably less work
    epsilon = ((2 ** n_bits) - 1) - gamma 

    return gamma * epsilon

def part1(bitstrings):

    # Sizes
    n_bits = len(bitstrings[0])
    n_vals = len(bitstrings)

    # Count set bits in each input
    cnt_bits_set = [0] * n_bits

    # Sum up bit counts at each position
    for bitstring in bitstrings:
        for pos, val in enumerate(list(bitstring)):
            if val == '1':
                cnt_bits_set[pos] += 1

    # Calculate gamma and epsilon
    gamma = 0
    epsilon = 0
    for pos in range(0, n_bits):
        exp = n_bits - pos - 1
        if cnt_bits_set[pos] > n_vals / 2:
            gamma += (2**exp)
        else:
            epsilon += (2**exp)

    # alternative calculation of epsilon (inverse), probably less work
    epsilon = ((2 ** n_bits) - 1) - gamma 

    return gamma * epsilon

def part2(bitstrings):

    # recursive step
    def filter_by_bit_at_pos(bitstrings, pos, keep_most_common=True):
        
        # Some safe-guard which are probably not necessary for the prepared input to the problem
        # (by looking at how the problem is formulated...)
        if len(bitstrings) == 0:
            raise Exception("Assumptions are wrong, there are more cases to cover...")

        # Recursive break condition
        if len(bitstrings) == 1:
            return bitstrings[0]

        # Count how many '1' at position 'pos'
        ones_at_pos = sum([1 if bitstring[pos] == '1' else 0 for bitstring in bitstrings])

        # Is '1' or '0' most common at position 'pos'?
        most_common = '1' if (ones_at_pos >= (len(bitstrings) / 2.)) else '0'

        # Filter bitstrings list and only keep the ones matching the criteria
        if keep_most_common:
            matching = [bitstring for bitstring in bitstrings if bitstring[pos] == most_common]
        else:
            matching = [bitstring for bitstring in bitstrings if bitstring[pos] != most_common]

        # Recursive step        
        return filter_by_bit_at_pos(matching, pos+1, keep_most_common)
        
    oxy_bits = filter_by_bit_at_pos(bitstrings, pos=0, keep_most_common=True)
    co2_bits = filter_by_bit_at_pos(bitstrings, pos=0, keep_most_common=False)

    return bitstring_to_base10(oxy_bits) * bitstring_to_base10(co2_bits)

########################
# Execution starts here
########################

# Read input
bitstrings = input_from_stream(sys.stdin)

# Solve puzzles
print(f'Part 1: {part1(bitstrings)}')
print(f'Part 1 (with NumPy): {part1_np(bitstrings)}')
print(f'Part 2: {part2(bitstrings)}')

