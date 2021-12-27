from collections import deque, Counter
from utils import input_from_stream
import numpy

class Packet:
    def __init__(self, type, version):
        self.type = type
        self.version = version

class PacketOp (Packet):
    def __init__(self, type, version, packets = []):
        self.type = type
        self.version = version
        self.packets = packets

    def value(self):
        subvals = [p.value() for p in self.packets]
        if self.type == 0:
            return sum(subvals)
        elif self.type == 1:
            return numpy.prod(subvals)
        elif self.type == 2:
            return min(subvals)
        elif self.type == 3:
            return max(subvals)
        elif self.type == 5:
            return 1 if subvals[0] > subvals[1] else 0
        elif self.type == 6:
            return 1 if subvals[0] < subvals[1] else 0
        elif self.type == 7:
            return 1 if subvals[0] == subvals[1] else 0
        else:
            raise Exception(f'Unknown packet type {self.type}')

    def sum_versions(self):
        return self.version + sum([p.sum_versions() for p in self.packets])

class PacketLiteral (Packet):
    def __init__(self, type, version, literal = 0):
        self.type = type
        self.version = version
        self.literal = literal

    def value(self):
        return self.literal

    def sum_versions(self):
        return self.version

def _debug(str):
    if False:
        print(str)

map = { '0' : '0000', '1' : '0001', '2' : '0010', '3' : '0011',
        '4' : '0100', '5' : '0101', '6' : '0110', '7' : '0111',
        '8' : '1000', '9' : '1001', 'A' : '1010', 'B' : '1011',
        'C' : '1100', 'D' : '1101', 'E' : '1110', 'F' : '1111' }

def hex_to_bits(hex_str):
    return ''.join([map[c] for c in hex_str])

def bin_to_int(str: str):
    val = 0
    for i, c in enumerate(str[::-1]):
        if c == '1':
            val = val + (2**i)

    return val

def parse_packet(binary: str) -> Packet:

    # Parse header (type and version)
    v = bin_to_int(binary[0:3])
    t = bin_to_int(binary[3:6])

    _debug(f'parsing packet         {binary}')
    _debug(f'  version={v}, type={t}')
    
    # parse the rest of the packet
    if t == 4:
        binary, literal = parse_literal_packet(binary[6:])
        return binary, PacketLiteral(t, v, literal)
    else:
        binary, sub_packets = parse_op_packet(binary[6:])
        return binary, PacketOp(t, v, sub_packets)

def parse_op_packet(binary: str):

    _debug(f'parsing op packet      {binary}')

    # This is where we collect the data
    subpackets = []
    l = binary[0]

    # Eat away a bit more at the input stream...
    binary = binary[1:]

    # Packet with fix number of bits
    if l == '0':
        n_bits = bin_to_int(binary[0:15])

        # Shave off the 15 bytes from the input
        binary = binary[15:]

        # This is the window we want to continue parsing
        packet_binary = binary[0:n_bits]

        # Parse packets from only a fix sub-array
        while len(packet_binary) > 0:
            packet_binary, packet = parse_packet(packet_binary)
            subpackets.append(packet)

        # Leave the rest for other parsing
        binary = binary[n_bits:]

    # Packet with fix number of subpackets        
    elif l == '1':
        n_packets = bin_to_int(binary[0:11])    
        binary = binary[11:]
        for n in range(n_packets):
            binary, packet = parse_packet(binary)
            subpackets.append(packet)
    
    else:
        raise Exception("Unknown length ID")

    _debug(f'--> subpackets: {len(subpackets)}')

    return binary, subpackets

def parse_literal_packet(binary: str):

    _debug(f'parsing literal packet {binary}')

    binary_literal = ''
    n_parts = 1

    while True:
        part = binary[0:5]
        binary = binary[5:]
        binary_literal += part[1:]

        if part[0] == '0':
            break

        n_parts += 1

    # Trim to be multiple of 4
    return binary, bin_to_int(binary_literal)

def part1(hex):
    binary = hex_to_bits(hex)
    _, packet = parse_packet(binary)
    return packet.sum_versions()

def part2(hex):
    binary = hex_to_bits(hex)
    _, packet = parse_packet(binary)
    return packet.value()

lines = input_from_stream()

print()
print(f'Part 1:')
print()
print(f'Test: 8A004A801A8002F478 => {part1("8A004A801A8002F478")}')
print(f'Test: 620080001611562C8802118E34 => {part1("620080001611562C8802118E34")}')
print(f'Test: C0015000016115A2E0802F182340 => {part1("C0015000016115A2E0802F182340")}')
print(f'Test: A0016C880162017C3686B18A3D4780 => {part1("A0016C880162017C3686B18A3D4780")}')
print()
print(f'Actual input: {part1(lines[0])}')
print()

print()
print(f'Part 2:')
print()
print(f'Test: C200B40A82 => {part2("C200B40A82")}')
print(f'Test: 04005AC33890 => {part2("04005AC33890")}')
print(f'Test: 880086C3E88112 => {part2("880086C3E88112")}')
print(f'Test: CE00C43D881120 => {part2("CE00C43D881120")}')
print(f'Test: D8005AC2A8F0 => {part2("D8005AC2A8F0")}')
print(f'Test: F600BC2D8F => {part2("F600BC2D8F")}')
print(f'Test: 9C005AC2F8F0 => {part2("9C005AC2F8F0")}')
print(f'Test: 9C0141080250320F1802104A08 => {part2("9C0141080250320F1802104A08")}')
print()
print(f'Actual input: {part2(lines[0])}')
print()
