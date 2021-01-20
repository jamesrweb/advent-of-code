def rotate(tile):
    return list("".join(x[::-1]) for x in zip(*tile))


def flip(tile):
    return list(reversed(tile.copy()))


def configurations(tile):
    x = rotate(tile)
    y = rotate(x)
    z = rotate(y)
    return [tile, x, y, z, flip(tile), flip(x), flip(y), flip(z)]


def generate_tiles(lines):
    id = 0
    grid = []
    tiles = {}

    for line in lines:
        if not line:
            tiles[id] = grid
            id = 0
            grid = []
        elif line.startswith("Tile"):
            id = int(line.replace(":", "").split()[1])
        else:
            grid.append(line)

    return tiles


def generate_possibilities(tiles):
    possibilities = {}
    for id, tile in tiles.items():
        possibilities[id] = configurations(tile)
    return possibilities


def assemble(possibilities):
    n = int(len(possibilities)**0.5)
    assembled = [[(0, 0)] * n for _ in range(n)]
    remaining = set(possibilities.keys())

    def assembly_helper(rc):
        if rc == n * n:
            return True
        row, column = rc // n, rc % n
        for id in list(remaining):
            for pid, possibility in enumerate(possibilities[id]):
                up = True
                left = True
                if row > 0:
                    uid, ut = assembled[row - 1][column]
                    up_tile = possibilities[uid][ut]
                    up = all(
                        possibility[0][i] == up_tile[9][i]
                        for i in range(10)
                    )
                if column > 0:
                    lid, lt = assembled[row][column - 1]
                    left_tile = possibilities[lid][lt]
                    left = all(
                        possibility[i][0] == left_tile[i][9]
                        for i in range(10)
                    )
                if up and left:
                    assembled[row][column] = (id, pid)
                    remaining.remove(id)
                    if assembly_helper(rc + 1):
                        return True
                    remaining.add(id)
        return False

    assembly_helper(0)
    return assembled


def monster_indexes():
    monster_pattern = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   "
    ]
    return [
        (row, column)
        for row in range(len(monster_pattern))
        for column in range(len(monster_pattern[row]))
        if monster_pattern[row][column] == "#"
    ]


def generate_map(image, possibilities):
    n = int(len(possibilities) ** 0.5)
    map = [["."] * (n * 8) for _ in range(n * 8)]
    for row in range(n):
        for column in range(n):
            id, possibility = image[row][column]
            tile = possibilities[id][possibility]
            for i in range(1, 9):
                for j in range(1, 9):
                    map[8 * row + i - 1][8 * column + j - 1] = tile[i][j]
    return map


def count_monsters(area):
    monsters = 0
    for row in range(len(area) - 3):
        for column in range(len(area) - 20):
            matches = []
            for mr, mc in monster_indexes():
                matches.append(area[row + mr][column + mc] == "#")
            monsters += 1 if all(matches) else 0
    return monsters


def solve_part_one(image):
    return image[0][0][0] * image[0][-1][0] * image[-1][0][0] * image[-1][-1][0]


def solve_part_two(image, possibilities):
    map = generate_map(image, possibilities)
    for configuration in configurations(map):
        monsters = count_monsters(configuration)
        if monsters > 0:
            total = sum(row.count("#") for row in configuration)
            return total - monsters * len(monster_indexes())
    return 0


with open("input.txt", "r") as f:
    lines = f.read().splitlines() + [""]
    tiles = generate_tiles(lines)
    possibilities = generate_possibilities(tiles)
    image = assemble(possibilities)

    print(f"part_one: {solve_part_one(image)}")
    print(f"part_two: {solve_part_two(image, possibilities)}")
