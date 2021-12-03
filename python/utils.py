import sys

# Read all lines into an array of strings (remove newlines at end)
def input_from_stream(inputstream=sys.stdin):
    return [line.replace('\n', '') for line in inputstream]

# Read all lines into an array, assuming that each line contains a single integer value
def input_as_int_array_from_stream(inputstream=sys.stdin):
    return [int(line) for line in input_from_stream(inputstream)]

#
# Invert a bit string
# 
# Examples:
#   '10001' => '01110'
#   '' => ''
#   '1' => '0'
#   '0000' => '1111'
#   '1111' => '0000'
#
def bitstring_inverse(bitstring):
    return ['0' if bit == '1' else '1' for bit in bitstring]

#
# Convert a bit string to a base-10 integer value
# 
# Examples:
#   '10001' => 17
#   '' => 0
#   '1' => 1
#   '0000' => 0
#   '1111' => 15
#
def bitstring_to_base10(bitstring):
    result = 0
    n_bits = len(bitstring)
    for pos, bit in enumerate(list(bitstring)):
        result += int(bit) * (2 ** (n_bits - pos - 1))
    
    return result

def _test_bitstring_inverse():
    for (test, answer) in [('10001','01110'), ('',''), ('1', '0'), ('0000','1111'), ('1111', '0000')]:
        assert bitstring_inverse(test) == answer

def _test_bitstring_to_base10():
    for (test, answer) in [('10001',17), ('',0), ('1', 1), ('0000',0), ('1111', 15)]:
        assert bitstring_to_base10(test) == answer

if __name__ == '__main__':
    _test_bitstring_to_base10()
