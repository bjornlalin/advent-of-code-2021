from utils import input_from_stream

WIRES_TO_DIGITS = {
    'abcefg' : '0',
    'cf' : '1',
    'acdeg' : '2',
    'acdfg' : '3',
    'bcdf' : '4',
    'abdfg' : '5',
    'abdefg' : '6',
    'acf' : '7',
    'abcdefg': '8',
    'abcdfg' : '9'
}

def part1(lines):
    n = 0
    for line in lines:
        d_out = [d.replace(' ','') for d in line.split('|')[1].split(' ') if len(d) > 0]
        n += len([d for d in d_out if len(d) in [2,3,4,7]])
    
    return n


def part2(lines):

    sum = 0

    def str_to_charsets(strings):
        return [set([c for c in string]) for string in strings]

    for line in lines:

        ALL = 'abcdefg'
        ALL_SET = set([c for c in ALL])

        # To start off, each wire can be mapped to each input signal wire
        possible = {c : ALL_SET for c in ALL}

        # These are the 10 signals we have observed
        # ASSUMPTION: EACH DIGIT OCCURS EXACTLY ONCE (INPUT SEEMS TO CONFIRM THIS)
        signals = [d.replace(' ','') for d in line.split('|')[0].split(' ') if len(d) > 0]

        one_set = str_to_charsets([signal for signal in signals if len(signal) == 2])[0]
        seven_set = str_to_charsets([signal for signal in signals if len(signal) == 3])[0]
        four_set = str_to_charsets([signal for signal in signals if len(signal) == 4])[0]
        eight_set = str_to_charsets([signal for signal in signals if len(signal) == 7])[0]

        # the digit for 1 and 7 differs only in the 'aaaa' segment.
        # Since we know 1 and 7 have unique lenghts (2 and 3), we can 
        # always figure out what wire is mapped to 'aaaa'
        possible['a'] = seven_set - one_set

        # ... which means we can remove that option from all other mapping tables
        possible['b'] -= possible['a']
        possible['c'] -= possible['a']
        possible['d'] -= possible['a']
        possible['e'] -= possible['a']
        possible['f'] -= possible['a']
        possible['g'] -= possible['a']

        # From the 1 pattern, We can reduce the 'cccc' and 'ffff' mapping tables to two options
        possible['c'] = one_set
        possible['f'] = one_set

        # From the 4 pattern, we can reduce 'bbbb' and 'dddd' mapping tables to two options as well
        possible['b'] = four_set - one_set
        possible['d'] = four_set - one_set

        # Now let's look at the 3 digits which are only missing a single wire (0, 6 and 9)
        missing_in_zero_six_nine_set = set.union(*[(eight_set - s) for s in str_to_charsets([signal for signal in signals if len(signal) == 6])])

        possible['d'] = possible['d'].intersection(missing_in_zero_six_nine_set)
        possible['e'] = possible['e'].intersection(missing_in_zero_six_nine_set)
        possible['c'] = possible['c'].intersection(missing_in_zero_six_nine_set)

        # Now that we for sure know 'cccc' and 'dddd' mappings (they only had two options
        # each before), we can remove them as options from all other wire mappings as well
        possible['b'] = possible['b'] - possible['c'] - possible['d']
        possible['e'] = possible['e'] - possible['c'] - possible['d']
        possible['f'] = possible['f'] - possible['c'] - possible['d']
        possible['g'] = possible['g'] - possible['c'] - possible['d']

        # Now only 'gggg' needs to be uniquely determined, all other are already done.
        possible['g'] = possible['g'] - possible['b'] - possible['e'] - possible['f']

        # These are the final and unique mappings as a dict()
        wire_mapping = {list(possible[c])[0] : c for c in 'abcdefg'}

        # These are the 4 digits we want to find the value for
        outputs = [d.replace(' ','') for d in line.split('|')[1].split(' ') if len(d) > 0]
        mapped = [''.join(sorted([wire_mapping[c] for c in output])) for output in outputs]

        #print(f'{outputs} ==> {mapped}')
        
        sum += int(''.join([WIRES_TO_DIGITS[m] for m in mapped]))

    return sum

lines = input_from_stream()

print(f'Part 1: {part1(lines)}')
print(f'Part 2: {part2(lines)}')
