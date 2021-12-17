from io import StringIO
from math import prod


class Packet:
    def __init__(self, bit_stream: StringIO):
        self.bit_stream = bit_stream
        self.version = parseBinary(self.bit_stream.read(3))
        self.type_id = parseBinary(self.bit_stream.read(3))
        self.subpackets = [] if self.type_id == 4 else self.read_subpackets()
        self.summed_versions = sum(self.versions())
        self.literal_value = {
            0: self.sum,
            1: self.prod,
            2: self.min,
            3: self.max,
            4: self.read_literal,
            5: self.greater_than,
            6: self.less_than,
            7: self.equal,
        }[self.type_id]()

    def read_literal(self):
        heading = ""
        literal = ""

        while heading != "0":
            heading = self.bit_stream.read(1)
            literal += self.bit_stream.read(4)

        return parseBinary(literal)

    def read_subpackets(self):
        length_type_id = self.bit_stream.read(1)

        if length_type_id == "0":
            total_subpacket_bit_length = parseBinary(self.bit_stream.read(15))
            upper_read_limit = self.bit_stream.tell() + total_subpacket_bit_length
            subpackets = []

            while self.bit_stream.tell() < upper_read_limit:
                packet = Packet(self.bit_stream)
                subpackets.append(packet)

            return subpackets

        total_subpacket_count = int(self.bit_stream.read(11), 2)
        subpackets = [Packet(self.bit_stream) for _ in range(total_subpacket_count)]

        return subpackets

    def sum(self):
        return sum(subpacket.literal_value for subpacket in self.subpackets)

    def prod(self):
        return prod(subpacket.literal_value for subpacket in self.subpackets)

    def min(self):
        return min(subpacket.literal_value for subpacket in self.subpackets)

    def max(self):
        return max(subpacket.literal_value for subpacket in self.subpackets)

    def greater_than(self):
        first, second, *_ = self.subpackets

        return int(first.literal_value > second.literal_value)

    def less_than(self):
        first, second, *_ = self.subpackets

        return int(first.literal_value < second.literal_value)

    def equal(self):
        first, second, *_ = self.subpackets

        return int(first.literal_value == second.literal_value)

    def versions(self):
        yield self.version

        for subpacket in self.subpackets:
            yield from subpacket.versions()


def parseHexadecimal(value: str) -> int:
    return int(value, 16)


def parseBinary(value: str) -> int:
    return int(value, 2)


def hexadecimalToBinary(hexadecimal: str) -> str:
    return "".join(f"{parseHexadecimal(character):04b}" for character in hexadecimal)


with open("input.txt", "r") as f:
    hexadecimal = f.read()
    binary = hexadecimalToBinary(hexadecimal)
    bit_stream = StringIO(binary)
    solution = Packet(bit_stream)

    print(f"part_one: {solution.summed_versions}")
    print(f"part_two: {solution.literal_value}")
