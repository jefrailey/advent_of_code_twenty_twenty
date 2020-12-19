"""
--- Day 16: Ticket Translation ---

As you're walking to yet another connecting flight, you realize that one of the legs of your re-routed trip coming up is on a high-speed train. However, the train ticket you were given is in a language you don't understand. You should probably figure out what it says before you get to the train station after the next flight.

Unfortunately, you can't actually read the words on the ticket. You can, however, read the numbers, and so you figure out the fields these tickets must have and the valid ranges for values in those fields.

You collect the rules for ticket fields, the numbers on your ticket, and the numbers on other nearby tickets for the same train service (via the airport security cameras) together into a single document you can reference (your puzzle input).

The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid ranges of values for each field. For example, a rule like class: 1-3 or 5-7 means that one of the fields in every ticket is named class and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are both valid in this field, but 4 is not).

Each ticket is represented by a single line of comma-separated values. The values are the numbers on the ticket in the order they appear; every ticket has the same format. For example, consider this ticket:

.--------------------------------------------------------.
| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
|                                                        |
| ??: 301  ??: 302             ???????: 303      ??????? |
| ??: 401  ??: 402           ???? ????: 403    ????????? |
'--------------------------------------------------------'

Here, ? represents text in a language you don't understand. This ticket might be represented as 101,102,103,104,301,302,303,401,402,403; of course, the actual train tickets you're looking at are much more complicated. In any case, you've extracted just the numbers in such a way that the first number is always the same specific field, the second number is always a different specific field, and so on - you just don't know what each position actually means!

Start by determining which tickets are completely invalid; these are tickets that contain values which aren't valid for any field. Ignore your ticket for now.

For example, suppose you have the following notes:

class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12

It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by considering only whether tickets contain values that are not valid for any field. In this example, the values on the first nearby ticket are all valid for at least one field. This is not true of the other three nearby tickets: the values 4, 55, and 12 are are not valid for any field. Adding together all of the invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.

Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?
"""


from typing import Any, Optional, Sequence
import math


def calculate_error_rate(rules: Sequence[str], tickets: Sequence[str]) -> int:
    parsed_rules = parse_rules(rules)
    invalids = 0
    for ticket in tickets:
        numbers = (int(item) for item in ticket.split(","))
        for number in numbers:
            if number not in parsed_rules:
                invalids += number
    return invalids


def parse_rules(rules: Sequence[str]) -> set[int]:
    parsed = set()
    for rule in rules:
        _, conditions = rule.split(": ")
        ranges = conditions.split(" or ")
        for range_ in ranges:
            start, stop = range_.split("-")
            start = int(start)
            stop = int(stop)
            for member in range(start, stop + 1):
                parsed.add(member)
    return parsed


"""
--- Part Two ---

Now that you've identified which tickets contain invalid values, discard those tickets entirely. Use the remaining valid tickets to determine which field is which.

Using the valid ranges for each field, determine what order the fields appear on the tickets. The order is consistent between all tickets: if seat is the third field, it is the third field on every ticket, including your ticket.

For example, suppose you have the following notes:

class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9

Based on the nearby tickets in the above example, the first position must be row, the second position must be class, and the third position must be seat; you can conclude that in your ticket, class is 12, row is 11, and seat is 13.

Once you work out which field is which, look for the six fields on your ticket that start with the word departure. What do you get if you multiply those six values together?
"""

# This sounds like it'll require recursive decent with backtracking.
# Nope. It works for the small input, but it's way too slow for the
# larger input.
# It's fast enough if the rules with the most constraints are placed first.


def part_two(rules: Sequence[str], tickets: Sequence[str], your_ticket: str) -> int:
    """
    Identify the order of the named ticket components and return the product of your ticket's departure components.
    """
    mapped = map_rules_to_valid_columns(rules, tickets)
    rule_order = _determine_rule_order(mapped)
    ticket_components = [int(component) for component in your_ticket.split(",")]
    indexes = (idx for (idx, name) in enumerate(rule_order) if "departure " in name)
    return math.prod(ticket_components[idx] for idx in indexes)


def map_rules_to_valid_value_sets(rules: Sequence[str]) -> dict[str, set[int]]:
    """
    Return a map of rule names to sets of valid values.
    """
    parsed_rules = {}
    for rule in rules:
        valids = set()
        name, conditions = rule.split(": ")
        ranges = conditions.split(" or ")
        for range_ in ranges:
            start, stop = range_.split("-")
            start = int(start)
            stop = int(stop)
            valids.update(range(start, stop + 1))
        parsed_rules[name] = valids
    return parsed_rules


def filter_tickets(
    mapped_rules: dict[str, set[int]], parsed_tickets: list[list[int]]
) -> list[list[int]]:
    """
    Return parsed tickets filtered to tickets that contain components that are valid for at least one rule.
    """
    valids = set()
    for rule_valids in mapped_rules.values():
        valids.update(rule_valids)
    return [
        ticket
        for ticket in parsed_tickets
        if all(component in valids for component in ticket)
    ]


def map_rules_to_valid_columns(
    rules: Sequence[str], tickets: Sequence[str]
) -> dict[str, list[int]]:
    """
    Return a map of rule names to a list values that indicate whether all ticket values at that position are valid for that rule.
    """
    mapped_rules = map_rules_to_valid_value_sets(rules)
    parsed_tickets = [[int(pos) for pos in ticket.split(",")] for ticket in tickets]
    valid_tickets = filter_tickets(mapped_rules, parsed_tickets)
    map_ = {}
    ticket_length = len(parsed_tickets[0])
    for rule, valids in mapped_rules.items():
        tracker = []
        for idx in range(ticket_length):
            tracker.append(int(all(ticket[idx] in valids for ticket in valid_tickets)))
        map_[rule] = tracker
    return map_


def _determine_rule_order(
    mapped: dict[str, list[int]], order: Optional[list[str]] = None
) -> list[str]:
    if order is None:
        order = []
    if len(order) == len(mapped):
        return order
    to_place = mapped.keys() - set(order)
    idx = len(order)
    # Reduce the number of iterations by sorting prospective rules by
    # the number of valid positions they can occupy.
    to_place = sorted(to_place, key=lambda x: sum(mapped[x]))
    for rule in to_place:
        if mapped[rule][idx]:
            order.append(rule)
            if _determine_rule_order(mapped, order):
                return order
            order.pop()
    return []


if __name__ == "__main__":

    def verify(expected: Any, actual: Any) -> None:
        assert expected == actual, f"{expected} != {actual}"

    rules = [
        "class: 1-3 or 5-7",
        "row: 6-11 or 33-44",
        "seat: 13-40 or 45-50",
    ]
    your_ticket = "7,1,14"
    nearby_tickets = [
        "7,3,47",
        "40,4,50",
        "55,2,20",
        "38,6,12",
    ]
    verify(71, calculate_error_rate(rules, nearby_tickets))

    from input_sixteen import rules, your_ticket, nearby_tickets

    print("Part one: ", calculate_error_rate(rules, nearby_tickets))
    print("Part two: ", part_two(rules, nearby_tickets, your_ticket))