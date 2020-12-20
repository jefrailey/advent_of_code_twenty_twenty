"""
--- Day 17: Conway Cubes ---

As your flight slowly drifts through the sky, the Elves at the Mythical Information Bureau at the North Pole contact you. They'd like some help debugging a malfunctioning experimental energy source aboard one of their super-secret imaging satellites.

The experimental energy source is based on cutting-edge technology: a set of Conway Cubes contained in a pocket dimension! When you hear it's having problems, you can't help but agree to take a look.

The pocket dimension contains an infinite 3-dimensional grid. At every integer 3-dimensional coordinate (x,y,z), there exists a single cube which is either active or inactive.

In the initial state of the pocket dimension, almost all cubes start inactive. The only exception to this is a small flat region of cubes (your puzzle input); the cubes in this region start in the specified active (#) or inactive (.) state.

The energy source then proceeds to boot up by executing six cycles.

Each cube only ever considers its neighbors: any of the 26 other cubes where any of their coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2, the cube at x=0,y=2,z=3, and so on.

During a cycle, all cubes simultaneously change their state according to the following rules:

    If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.

The engineers responsible for this experimental energy source would like you to simulate the pocket dimension and determine what the configuration of cubes should be at the end of the six-cycle boot process.

For example, consider the following initial state:

.#.
..#
###

Even though the pocket dimension is 3-dimensional, this initial state represents a small 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1 region of the 3-dimensional space.)

Simulating a few cycles from this initial state produces the following configurations, where the result of each cycle is shown layer-by-layer at each given z coordinate (and the frame of view follows the active cells in each cycle):

Before any cycles:

z=0
.#.
..#
###


After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.


After 2 cycles:

z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....


After 3 cycles:

z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
.......

After the full six-cycle boot process completes, 112 cubes are left in the active state.

Starting with your given initial configuration, simulate six cycles. How many cubes are left in the active state after the sixth cycle?
"""


"""

    If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
"""

from typing import Any, Sequence

ACTIVE = "#"


def make_space(plane: Sequence[str]) -> set[tuple[int, int, int]]:
    """
    Return a set of points in space that contain active "cubes."
    """
    space = set()
    z = 0
    for y, row in enumerate(plane):
        for x, cell in enumerate(row):
            if cell == ACTIVE:
                space.add((x, y, z))
    return space


def part_one(initial_plane: Sequence[str], cycles: int) -> int:
    """
    Return the count of active cubes after playing cycles.
    """
    space = make_space(initial_plane)
    for _ in range(cycles):
        space = simulate(space)
    return len(space)


def simulate(space: set[tuple[int, int, int]]) -> set[tuple[int, int, int]]:
    """
    Return a copy of space mutated based on the rules of the game.
    """
    iteration = set()
    # each point in space represents an active cube.
    # for each active cube we need to identify and collect all of its inactive neighbors
    # we also need to identify the count of its active neighbors (which would be total neighbors - inactive neighbors)
    # finally, if it should remain active, based on the count of its active neighbors, then it needs to be
    # added to the next space
    inactives = set()
    for active_cube in space:
        neighbors = find_neighbors(active_cube)
        active_count = 0
        for neighbor in neighbors:
            if neighbor not in space:
                inactives.add(neighbor)
            else:
                active_count += 1
        if active_count in {2, 3}:
            iteration.add(active_cube)

    for inactive in inactives:
        neighbors = find_neighbors(inactive)
        active_count = sum((neighbor in space) for neighbor in neighbors)
        if active_count == 3:
            iteration.add(inactive)
    return iteration


def find_neighbors(point: tuple[int, int, int]) -> Sequence[tuple[int, int, int]]:
    x_0, y_0, z_0 = point
    neighbors = []
    for z in range(z_0 - 1, z_0 + 2):
        for y in range(y_0 - 1, y_0 + 2):
            for x in range(x_0 - 1, x_0 + 2):
                if x_0 == x and y_0 == y and z_0 == z:
                    continue
                neighbors.append((x, y, z))
    return neighbors


"""
--- Part Two ---

For some reason, your simulated results don't match what the experimental energy source engineers expected. Apparently, the pocket dimension actually has four spatial dimensions, not three.

The pocket dimension contains an infinite 4-dimensional grid. At every integer 4-dimensional coordinate (x,y,z,w), there exists a single cube (really, a hypercube) which is still either active or inactive.

Each cube only ever considers its neighbors: any of the 80 other cubes where any of their coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3,w=4, its neighbors include the cube at x=2,y=2,z=3,w=3, the cube at x=0,y=2,z=3,w=4, and so on.

The initial state of the pocket dimension still consists of a small flat region of cubes. Furthermore, the same rules for cycle updating still apply: during each cycle, consider the number of active neighbors of each cube.

For example, consider the same initial state as in the example above. Even though the pocket dimension is 4-dimensional, this initial state represents a small 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1x1 region of the 4-dimensional space.)

Simulating a few cycles from this initial state produces the following configurations, where the result of each cycle is shown layer-by-layer at each given z and w coordinate:

Before any cycles:

z=0, w=0
.#.
..#
###


After 1 cycle:

z=-1, w=-1
#..
..#
.#.

z=0, w=-1
#..
..#
.#.

z=1, w=-1
#..
..#
.#.

z=-1, w=0
#..
..#
.#.

z=0, w=0
#.#
.##
.#.

z=1, w=0
#..
..#
.#.

z=-1, w=1
#..
..#
.#.

z=0, w=1
#..
..#
.#.

z=1, w=1
#..
..#
.#.


After 2 cycles:

z=-2, w=-2
.....
.....
..#..
.....
.....

z=-1, w=-2
.....
.....
.....
.....
.....

z=0, w=-2
###..
##.##
#...#
.#..#
.###.

z=1, w=-2
.....
.....
.....
.....
.....

z=2, w=-2
.....
.....
..#..
.....
.....

z=-2, w=-1
.....
.....
.....
.....
.....

z=-1, w=-1
.....
.....
.....
.....
.....

z=0, w=-1
.....
.....
.....
.....
.....

z=1, w=-1
.....
.....
.....
.....
.....

z=2, w=-1
.....
.....
.....
.....
.....

z=-2, w=0
###..
##.##
#...#
.#..#
.###.

z=-1, w=0
.....
.....
.....
.....
.....

z=0, w=0
.....
.....
.....
.....
.....

z=1, w=0
.....
.....
.....
.....
.....

z=2, w=0
###..
##.##
#...#
.#..#
.###.

z=-2, w=1
.....
.....
.....
.....
.....

z=-1, w=1
.....
.....
.....
.....
.....

z=0, w=1
.....
.....
.....
.....
.....

z=1, w=1
.....
.....
.....
.....
.....

z=2, w=1
.....
.....
.....
.....
.....

z=-2, w=2
.....
.....
..#..
.....
.....

z=-1, w=2
.....
.....
.....
.....
.....

z=0, w=2
###..
##.##
#...#
.#..#
.###.

z=1, w=2
.....
.....
.....
.....
.....

z=2, w=2
.....
.....
..#..
.....
.....


After the full six-cycle boot process completes, 848 cubes are left in the active state.

Starting with your given initial configuration, simulate six cycles in a 4-dimensional space. How many cubes are left in the active state after the sixth cycle?
"""


def part_two(initial_plane: Sequence[str], cycles: int) -> int:
    """
    Return the count of active cubes after playing cycles.
    """
    space = make_four_dimensional_space(initial_plane)
    for _ in range(cycles):
        space = simulate_four_dimensions(space)
    return len(space)


def make_four_dimensional_space(plane: Sequence[str]) -> set[tuple[int, int, int, int]]:
    """
    Return a set of points in space that contain active "cubes."
    """
    space = set()
    w = 0
    z = 0
    for y, row in enumerate(plane):
        for x, cell in enumerate(row):
            if cell == ACTIVE:
                space.add((x, y, z, w))
    return space


def simulate_four_dimensions(
    space: set[tuple[int, int, int, int]]
) -> set[tuple[int, int, int, int]]:
    """
    Return a copy of space mutated based on the rules of the game.
    """
    next_space = set()
    inactives = set()
    for active_cube in space:
        neighbors = find_four_dimensional_neighbors(active_cube)
        active_count = 0
        for neighbor in neighbors:
            if neighbor not in space:
                inactives.add(neighbor)
            else:
                active_count += 1
        if active_count in {2, 3}:
            next_space.add(active_cube)

    for inactive in inactives:
        neighbors = find_four_dimensional_neighbors(inactive)
        active_count = sum((neighbor in space) for neighbor in neighbors)
        if active_count == 3:
            next_space.add(inactive)
    return next_space


def find_four_dimensional_neighbors(
    point: tuple[int, int, int, int]
) -> Sequence[tuple[int, int, int, int]]:
    """
    Return the 80 neighbors of a four-dimensional point.
    """
    x_0, y_0, z_0, w_0 = point
    neighbors = []
    for w in range(w_0 - 1, w_0 + 2):
        for z in range(z_0 - 1, z_0 + 2):
            for y in range(y_0 - 1, y_0 + 2):
                for x in range(x_0 - 1, x_0 + 2):
                    if x_0 == x and y_0 == y and z_0 == z and w_0 == w:
                        continue
                    neighbors.append((x, y, z, w))
    return neighbors


if __name__ == "__main__":

    def verify(expected: Any, actual: Any) -> None:
        assert expected == actual, f"{expected} != {actual}"

    diagnostic = [
        ".#.",
        "..#",
        "###",
    ]
    verify(5, part_one(initial_plane=diagnostic, cycles=0))
    verify(11, part_one(initial_plane=diagnostic, cycles=1))
    verify(112, part_one(initial_plane=diagnostic, cycles=6))

    verify(848, part_two(initial_plane=diagnostic, cycles=6))

    input_ = [
        ".##...#.",
        ".#.###..",
        "..##.#.#",
        "##...#.#",
        "#..#...#",
        "#..###..",
        ".##.####",
        "..#####.",
    ]
    print("Part one: ", part_one(initial_plane=input_, cycles=6))
    print("Part one: ", part_two(initial_plane=input_, cycles=6))
