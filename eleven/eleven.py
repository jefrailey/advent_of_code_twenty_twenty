"""
--- Day 11: Seating System ---

Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

    If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    Otherwise, the seat's state does not change.

Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##

After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##

This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##

#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##

#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##

At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?
"""

from typing import Any, Callable, Optional, Sequence


FLOOR = "."
EMPTY = "L"
OCCUPIED = "#"

"""
 The following rules are applied to every seat simultaneously:

    If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    Otherwise, the seat's state does not change.
"""

# copy seating chart into new chart by iteratively examining every seat position and checking its adjacent seats.
# If the new seating chart is the same as the old, return the number of occupied seats.


def first_evolver(chart: Sequence[str]) -> Sequence[str]:
    evolution = list(chart)
    for row_idx, row in enumerate(chart):
        for col_idx, _ in enumerate(chart[row_idx]):
            if should_sit(chart, row_idx, col_idx):
                row = insert(row, "#", col_idx)
            elif should_leave(chart, row_idx, col_idx):
                row = insert(row, "L", col_idx)
        evolution[row_idx] = row
    return evolution


def play(
    chart: Sequence[str],
    evolver: Callable[[Sequence[str]], Sequence[str]] = first_evolver,
) -> int:
    previous = chart
    while True:
        evolution = evolver(previous)
        if evolution == previous:
            return sum(row.count("#") for row in evolution)
        previous = evolution


def find_adjacencies(chart: Sequence[str], row_idx: int, col_idx: int) -> Sequence[str]:
    above = [(row_idx - 1, col_idx + i) for i in (-1, 0, 1)]
    below = [(row_idx + 1, col_idx + i) for i in (-1, 0, 1)]
    same_row = [(row_idx, col_idx + i) for i in (-1, 1)]
    candidates = []
    candidates.extend(above)
    candidates.extend(same_row)
    candidates.extend(below)
    return [
        chart[row_idx][col_idx]
        for (row_idx, col_idx) in candidates
        if 0 <= row_idx < len(chart) and 0 <= col_idx < len(chart[0])
    ]


def should_sit(
    chart: Sequence[str],
    row_idx: int,
    col_idx: int,
    adjacency_finder: Callable[
        [Sequence[str], int, int], Sequence[str]
    ] = find_adjacencies,
) -> bool:
    """
    Return True if the someone should sit in the indicated location this round.

    If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    """
    seat = chart[row_idx][col_idx]
    if seat != EMPTY:
        return False
    adjacencies = adjacency_finder(chart, row_idx, col_idx)
    return all(adjacent != OCCUPIED for adjacent in adjacencies)


def insert(row: str, char: str, idx: int) -> str:
    return row[:idx] + char + row[idx + 1 :]


def should_leave(
    chart: Sequence[str],
    row_idx: int,
    col_idx: int,
    adjacency_finder: Callable[
        [Sequence[str], int, int], Sequence[str]
    ] = find_adjacencies,
    max_occupied: int = 4,
) -> bool:
    """
    Return True if the seat should be abandoned.

    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    Otherwise, the seat's state does not change.
    """
    seat = chart[row_idx][col_idx]
    if seat != OCCUPIED:
        return False
    adjacencies = adjacency_finder(chart, row_idx, col_idx)
    occupied_adjacent = sum(adjacent == OCCUPIED for adjacent in adjacencies)
    return occupied_adjacent >= max_occupied


def visible_from(chart: Sequence[str], row_idx: int, col_idx: int) -> Sequence[str]:
    """
    Return the first seat that can be seen in eight directions from the given position in the seating chart.
    """
    # For each of the eight directions, cast a ray.
    # Return
    directions = ((-1, 0), (1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1), (0, -1), (0, 1))
    visibles = (
        first_visible(chart, row_idx, col_idx, direction) for direction in directions
    )
    return [visible for visible in visibles if visible]


def first_visible(
    chart: Sequence[str], row_idx: int, col_idx: int, direction: tuple[int, int]
) -> Optional[str]:
    """
    Return the first empty or occupied seat visible from the given location in the given direction.
    """
    row_delta, col_delta = direction
    row_idx += row_delta
    col_idx += col_delta
    max_row = len(chart)
    max_col = len(chart[0])
    while 0 <= row_idx < max_row and 0 <= col_idx < max_col:
        if (seat := chart[row_idx][col_idx]) != FLOOR:
            return seat
        row_idx += row_delta
        col_idx += col_delta
    return None


def second_evolver(chart: Sequence[str]) -> Sequence[str]:
    evolution = list(chart)
    for row_idx, row in enumerate(chart):
        for col_idx, _ in enumerate(chart[row_idx]):
            if should_sit(chart, row_idx, col_idx, adjacency_finder=visible_from):
                row = insert(row, "#", col_idx)
            elif should_leave(
                chart, row_idx, col_idx, adjacency_finder=visible_from, max_occupied=5
            ):
                row = insert(row, "L", col_idx)
        evolution[row_idx] = row
    return evolution


"""
--- Part Two ---

As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats - they care about the first seat they can see in each of those eight directions!

Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight directions. For example, the empty seat below would see eight occupied seats:

.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....

The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:

.............
.L.L.#.#.#.#.
.............

The empty seat below would see no occupied seats:

.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.

Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an occupied seat to become empty (rather than four or more from the previous rules). The other rules still apply: empty seats that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.

Given the same starting layout as above, these new rules cause the seating area to shift around as follows:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##

#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#

#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#

Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once this occurs, you count 26 occupied seats.

Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?
"""

if __name__ == "__main__":

    def verify(expected: Any, actual: Any) -> None:
        assert expected == actual, f"{expected} != {actual}"

    diagnostic = [
        "L.LL.LL.LL",
        "LLLLLLL.LL",
        "L.L.L..L..",
        "LLLL.LL.LL",
        "L.LL.LL.LL",
        "L.LLLLL.LL",
        "..L.L.....",
        "LLLLLLLLLL",
        "L.LLLLLL.L",
        "L.LLLLL.LL",
    ]

    one_round = [
        "#.##.##.##",
        "#######.##",
        "#.#.#..#..",
        "####.##.##",
        "#.##.##.##",
        "#.#####.##",
        "..#.#.....",
        "##########",
        "#.######.#",
        "#.#####.##",
    ]
    verify(one_round, first_evolver(diagnostic))
    verify(37, play(diagnostic))

    verify(26, play(diagnostic, second_evolver))
    from input_eleven import input_

    print("Part one: ", play(input_))
    print("Part two: ", play(input_, second_evolver))
