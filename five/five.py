"""
--- Day 5: Binary Boarding ---

You board your plane only to discover a new problem: you dropped your boarding pass! You aren't sure which seat is yours, and all of the flight attendants are busy with the flood of people that suddenly made it through passport control.

You write a quick program to use your phone's camera to scan all of the nearby boarding passes (your puzzle input); perhaps you can find your seat through process of elimination.

Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".

The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127). Each letter tells you which half of a region the given seat is in. Start with the whole list of rows; the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127). The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.

For example, consider just the first seven characters of FBFBBFFRLR:

    Start by considering the whole range, rows 0 through 127.
    F means to take the lower half, keeping rows 0 through 63.
    B means to take the upper half, keeping rows 32 through 63.
    F means to take the lower half, keeping rows 32 through 47.
    B means to take the upper half, keeping rows 40 through 47.
    B keeps rows 44 through 47.
    F keeps rows 44 through 45.
    The final F keeps the lower of the two, row 44.

The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane (numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep the lower half, while R means to keep the upper half.

For example, consider just the last 3 characters of FBFBBFFRLR:

    Start by considering the whole range, columns 0 through 7.
    R means to take the upper half, keeping columns 4 through 7.
    L means to take the lower half, keeping columns 4 through 5.
    The final R keeps the upper of the two, column 5.

So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.

Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357.

Here are some other boarding passes:

    BFFFBBFRRR: row 70, column 7, seat ID 567.
    FFFBBBFRRR: row 14, column 7, seat ID 119.
    BBFFBBFRLL: row 102, column 4, seat ID 820.

As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?
"""


from typing import NamedTuple, Sequence


class BoardingPass(NamedTuple):
    row: int
    column: int
    seat_id: int


def scan_boarding_pass(boarding_pass: str) -> BoardingPass:
    """
    Convert boarding pass character sequence into a BoardingPass.
    """
    row = convert_partition(boarding_pass[:7], lower="F")
    column = convert_partition(boarding_pass[7:], lower="L")
    seat_id = row * 8 + column
    return BoardingPass(row, column, seat_id)


def convert_partition(characters: str, lower: str) -> int:
    """
    Return the location indicated by the binary space partitioning character sequence.
    """
    size = 2 ** len(characters)
    options = list(range(size))
    idx = 0
    while len(options) > 1:
        char = characters[idx]
        mid = len(options) // 2
        if char == lower:
            options = options[:mid]
        else:
            options = options[mid:]
        idx += 1
    return options[0]


# I added this function after submitting the solution. This is an improvement over
# convert_partition because it eliminates the O(2^N) memory requirement of
# convert_partition's options list.
def alternate_partition(characters: str, lower: str) -> int:
    """
    Return the location indicated by the binary space partitioning character sequence.
    """
    size = 2 ** len(characters)
    min_ = 0
    max_ = size - 1
    idx = 0
    while idx < len(characters):
        mid = ((max_ - min_) // 2) + min_
        if characters[idx] == lower:
            max_ = mid
        else:
            min_ = mid
        idx += 1
    return max_


"""
--- Part Two ---

Ding! The "fasten seat belt" signs have turned on. Time to find your seat.

It's a completely full flight, so your seat should be the only missing boarding pass in your list. However, there's a catch: some of the seats at the very front and back of the plane don't exist on this aircraft, so they'll be missing from your list as well.

Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.

What is the ID of your seat?

"""


def find_seat(boarding_passes: Sequence[BoardingPass]) -> int:
    """
    Return the id of the empty seat.

    This function assumes that there is exactly one empty seat, that seat is not
    at the front or the back, and that there exist a seat with an id one less
    than its id and a seat with an id one greater than its id.
    """
    seat_ids = sorted(boarding_pass.seat_id for boarding_pass in boarding_passes)
    for idx, current in enumerate(seat_ids[:-1]):
        next_ = seat_ids[idx + 1]
        if next_ - current == 2:
            return current + 1
    return -1


if __name__ == "__main__":
    assert alternate_partition("FBFBBFF", lower="F") == 44
    assert convert_partition("FBFBBFF", lower="F") == 44
    assert convert_partition("RLR", lower="L") == 5
    assert scan_boarding_pass("FBFBBFFRLR") == (44, 5, 44 * 8 + 5)
    assert scan_boarding_pass("BFFFBBFRRR") == (70, 7, 567)
    assert scan_boarding_pass("FFFBBBFRRR") == (14, 7, 119)
    assert scan_boarding_pass("BBFFBBFRLL") == (102, 4, 820)

    from input_five import input_ as raw_passes

    scanned_passes = [scan_boarding_pass(boarding_pass) for boarding_pass in raw_passes]
    print(
        "Part one: ",
        max(boarding_pass.seat_id for boarding_pass in scanned_passes),
    )

    print("Part two: ", find_seat(scanned_passes))
