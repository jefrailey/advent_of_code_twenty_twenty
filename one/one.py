"""
--- Day 1: Report Repair ---

After saving Christmas five years in a row, you've decided to take a vacation at a nice resort on a tropical island. Surely, Christmas will go on without you.

The tropical island has its own currency and is entirely cash-only. The gold coins used there have a little picture of a starfish; the locals just call them stars. None of the currency exchanges seem to have heard of them, but somehow, you'll need to find fifty of these coins by the time you arrive so you can pay the deposit on your room.

To save your vacation, you need to get all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456

In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?

"""

"""Find two entries that sum to 2020 in a list of integers"""


from typing import Optional, Sequence


def find_pair_sums_to(target: int, entries: Sequence[int]) -> Optional[Sequence[int]]:
    compliments = {target - entry: entry for entry in entries}
    for entry in entries:
        if entry in compliments:
            return entry, compliments[entry]


def craft_answer(input_: Sequence[int]) -> Optional[int]:
    entries = find_pair_sums_to(2020, input_)
    if entries:
        return entries[0] * entries[1]


"""
--- Part Two ---

The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.

Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to 2020?
"""


def find_trio_sums_to(target: int, entries: Sequence[int]) -> Optional[Sequence[int]]:
    for entry in entries:
        addends = find_pair_sums_to(target - entry, entries)
        if addends:
            return *addends, entry


def craft_part_two_answer(input_: Sequence[int]) -> Optional[int]:
    entries = find_trio_sums_to(2020, input_)
    if entries:
        return entries[0] * entries[1] * entries[2]


# Added after entering the solution to part two.
def find_sums_to(
    target: int, addend_count: int, entries: Sequence[int]
) -> Optional[Sequence[int]]:
    if addend_count == 2:
        compliments = {target - entry: entry for entry in entries}
        for entry in entries:
            if entry in compliments:
                return entry, compliments[entry]
    for entry in entries:
        addends = find_sums_to(target - entry, addend_count - 1, entries)
        if addends:
            return *addends, entry


if __name__ == "__main__":
    input_ = [
        1721,
        979,
        366,
        299,
        675,
        1456,
    ]
    assert craft_answer(input_) == 514579
    assert craft_part_two_answer(input_) == 241861950
    from input_one import input_

    print(craft_answer(input_))
    print(craft_part_two_answer(input_))