from os import path


def project_disk(filesystem):
    disk = []
    fileId = 0

    for i, char in enumerate(filesystem):
        count = int(char)

        if i % 2 == 0:
            disk += [fileId] * count
            fileId += 1
        else:
            disk += [-1] * count

    return disk


def project_disk_without_fragmentation(filesystem):
    files = {}
    blanks = []
    fileId = 0
    position = 0

    for index, char in enumerate(filesystem):
        count = int(char)

        if index % 2 == 0:
            files[fileId] = (position, count)
            fileId += 1
        else:
            blanks.append((position, count))

        position += count

    return files, blanks, fileId, position


def optimise_disk(disk, blanks):
    for index in blanks:
        while disk[-1] == -1:
            disk.pop()

        if len(disk) <= index:
            break

        disk[index] = disk.pop()

    return disk


def optimise_disk_without_fragmentation(filesystem):
    files, blanks, fileId, position = project_disk_without_fragmentation(filesystem)

    while fileId > 0:
        fileId -= 1
        position, size = files[fileId]

        for i, (start, length) in enumerate(blanks):
            if start >= position:
                blanks = blanks[:i]

                break

            if size <= length:
                files[fileId] = (start, size)

                if size == length:
                    blanks.pop(i)
                else:
                    blanks[i] = (start + size, length - size)

                break

    return files


def calculate_filesystem_checksum(filesystem):
    disk = project_disk(filesystem)
    blanks = [index for index, count in enumerate(disk) if count == -1]
    fragmented_disk = optimise_disk(disk, blanks)

    return sum(index * count for index, count in enumerate(fragmented_disk))


def calculate_filesystem_checksum_without_fragmentation(filesystem):
    files = optimise_disk_without_fragmentation(filesystem)
    total = 0

    for id, (position, size) in files.items():
        for point in range(position, position + size):
            total += id * point

    return total


with open(path.dirname(path.realpath(__file__)) + "/input.txt") as file:
    filesystem = file.read()
    part_one = calculate_filesystem_checksum(filesystem)
    part_two = calculate_filesystem_checksum_without_fragmentation(filesystem)

    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")
