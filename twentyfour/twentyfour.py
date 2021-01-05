"""
--- Day 24: Lobby Layout ---

Your raft makes it to the tropical island; it turns out that the small crab was an excellent navigator. You make your way to the resort.

As you enter the lobby, you discover a small problem: the floor is being renovated. You can't even reach the check-in desk until they've finished installing the new tile floor.

The tiles are all hexagonal; they need to be arranged in a hex grid with a very specific color pattern. Not in the mood to wait, you offer to help figure out the pattern.

The tiles are all white on one side and black on the other. They start with the white side facing up. The lobby is large enough to fit whatever pattern might need to appear there.

A member of the renovation crew gives you a list of the tiles that need to be flipped over (your puzzle input). Each line in the list identifies a single tile that needs to be flipped by giving a series of steps starting from a reference tile in the very center of the room. (Every line starts from the same reference tile.)

Because the tiles are hexagonal, every tile has six neighbors: east, southeast, southwest, west, northwest, and northeast. These directions are given in your list, respectively, as e, se, sw, w, nw, and ne. A tile is identified by a series of these directions with no delimiters; for example, esenee identifies the tile you land on if you start at the reference tile and then move one tile east, one tile southeast, one tile northeast, and one tile east.

Each time a tile is identified, it flips from white to black or from black to white. Tiles might be flipped more than once. For example, a line like esew flips a tile immediately adjacent to the reference tile, and a line like nwwswee flips the reference tile itself.

Here is a larger example:

sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew

In the above example, 10 tiles are flipped once (to black), and 5 more are flipped twice (to black, then back to white). After all of these instructions have been followed, a total of 10 tiles are black.

Go through the renovation crew's list and determine which tiles they need to flip. After all of the instructions have been followed, how many tiles are left with the black side up?
"""

from typing import Any, Sequence


def flip_tiles(instructions: Sequence[str]) -> set[tuple[float, int]]:
    black_tiles = set()
    for instruction in instructions:
        destination = follow_instruction(instruction)
        if destination in black_tiles:
            black_tiles.remove(destination)
        else:
            black_tiles.add(destination)
    return black_tiles


def follow_instruction(instruction: str) -> tuple[float, int]:
    x = 0  # east-west
    y = 0  # north-south
    idx = 0
    while idx < len(instruction):
        current = instruction[idx]
        if current == "e":
            x += 1
        elif current == "w":
            x -= 1
        elif current in {"n", "s"}:
            idx += 1
            next_ = instruction[idx]
            if current == "n":
                y += 1
            else:
                y -= 1
            if next_ == "e":
                x += 0.5
            else:
                x -= 0.5
        idx += 1
    return (x, y)


def part_one(instructions: Sequence[str]) -> int:
    """
    Return the number of tiles that display their black side after following the instructions.
    """
    return len(flip_tiles(instructions))


"""
--- Part Two ---

The tile floor in the lobby is meant to be a living art exhibit. Every day, the tiles are all flipped according to the following rules:

    Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
    Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.

Here, tiles immediately adjacent means the six tiles directly touching the tile in question.

The rules are applied simultaneously to every tile; put another way, it is first determined which tiles need to be flipped, then they are all flipped at the same time.

In the above example, the number of black tiles that are facing up after the given number of days has passed is as follows:

Day 1: 15
Day 2: 12
Day 3: 25
Day 4: 14
Day 5: 23
Day 6: 28
Day 7: 41
Day 8: 37
Day 9: 49
Day 10: 37

Day 20: 132
Day 30: 259
Day 40: 406
Day 50: 566
Day 60: 788
Day 70: 1106
Day 80: 1373
Day 90: 1844
Day 100: 2208

After executing this process a total of 100 times, there would be 2208 black tiles facing up.

How many tiles will be black after 100 days?

"""


def part_two(instructions: Sequence[str], days: int) -> int:
    """
    Return the number of tiles that will display their black side after days of evolution.

    The initial state is determined by following the instructions. After the first day, the
    tiles are flipped based on the state of the tiles next to them.

    - Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
    - Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
    """
    black_tiles = flip_tiles(instructions)
    for _ in range(days):
        black_tiles = evolve(black_tiles)
    return len(black_tiles)


def evolve(black_tiles: set[tuple[float, int]]) -> set[tuple[float, int]]:
    """
    Return a set of tiles displaying their black side after conditionally flipping every tile based on the state of its neighbor.

        - Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
        - Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
    """
    # generate a map of tiles that neighbor a black tile to all of their neighbors
    neighbors = map_neighbors(black_tiles)
    # # Need to remove black tiles that do not have black neighbors
    flipped = {tile for tile in black_tiles if tile in neighbors}

    for tile, others in neighbors.items():
        black_neighbor_count = len(black_tiles.intersection(others))
        if tile in black_tiles:
            if black_neighbor_count > 2:
                flipped.remove(tile)
        else:
            if black_neighbor_count == 2:
                flipped.add(tile)
    return flipped


def map_neighbors(
    black_tiles: set[tuple[float, int]]
) -> dict[tuple[float, int], set[tuple[float, int]]]:
    neighbors = {}
    for tile in black_tiles:
        for neighbor in generate_neighbors(tile):
            neighbors.setdefault(neighbor, set()).add(tile)
    return neighbors


def generate_neighbors(tile: tuple[float, int]) -> set[tuple[float, int]]:
    x, y = tile
    return {
        (x + 1, y),
        (x - 1, y),
        (x - 0.5, y - 1),
        (x - 0.5, y + 1),
        (x + 0.5, y - 1),
        (x + 0.5, y + 1),
    }


if __name__ == "__main__":

    def verify(expected: Any, actual: Any) -> None:
        assert expected == actual, f"{expected} != {actual}"

    verify((0.0, 0), follow_instruction("nwwswee"))

    diagnostic = [
        "sesenwnenenewseeswwswswwnenewsewsw",
        "neeenesenwnwwswnenewnwwsewnenwseswesw",
        "seswneswswsenwwnwse",
        "nwnwneseeswswnenewneswwnewseswneseene",
        "swweswneswnenwsewnwneneseenw",
        "eesenwseswswnenwswnwnwsewwnwsene",
        "sewnenenenesenwsewnenwwwse",
        "wenwwweseeeweswwwnwwe",
        "wsweesenenewnwwnwsenewsenwwsesesenwne",
        "neeswseenwwswnwswswnw",
        "nenwswwsewswnenenewsenwsenwnesesenew",
        "enewnwewneswsewnwswenweswnenwsenwsw",
        "sweneswneswneneenwnewenewwneswswnese",
        "swwesenesewenwneswnwwneseswwne",
        "enesenwswwswneneswsenwnewswseenwsese",
        "wnwnesenesenenwwnenwsewesewsesesew",
        "nenewswnwewswnenesenwnesewesw",
        "eneswnwswnwsenenwnwnwwseeswneewsenese",
        "neswnwewnwnwseenwseesewsenwsweewe",
        "wseweeenwnesenwwwswnew",
    ]

    verify(10, part_one(diagnostic))

    verify(15, part_two(diagnostic, 1))
    verify(37, part_two(diagnostic, 10))
    verify(2208, part_two(diagnostic, 100))

    from twentyfour_input import input_

    print("Part one: ", part_one(input_))
    print("Part two: ", part_two(input_, 100))
