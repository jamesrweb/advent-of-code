from functools import reduce


def lookup(inputs, mapping):
    for start, length in inputs:
        while length > 0:
            for line in mapping.split("\n")[1:]:
                destination, source, range_size = map(int, line.split())
                delta = start - source
                if delta in range(range_size):
                    range_size = min(range_size - delta, length)
                    start += range_size
                    length -= range_size
                    yield (destination + delta, range_size)
                    break
            else:
                yield (start, length)
                break


def lookupReducerForSeed(seed):
    locations = reduce(lookup, mappings, seed)

    return min(locations)


with open("input.txt") as file:
    seeds, *mappings = file.read().split("\n\n")
    seed_values = list(map(int, seeds.split()[1:]))

    part_one, part_two = [
        lookupReducerForSeed(seed)[0]
        for seed in [
            zip(seed_values, [1] * len(seed_values)),
            zip(seed_values[0::2], seed_values[1::2]),
        ]
    ]

    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")
