"""
--- Day 19: Monster Messages ---

You land in an airport surrounded by dense forest. As you walk to your high-speed train, the Elves at the Mythical Information Bureau contact you again. They think their satellite has collected an image of a sea monster! Unfortunately, the connection to the satellite is having problems, and many of the messages sent back from the satellite have been corrupted.

They sent you a list of the rules valid messages should obey and a list of received messages they've collected so far (your puzzle input).

The rules for valid messages (the top part of your puzzle input) are numbered and build upon each other. For example:

0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

Some rules, like 3: "b", simply match a single character (in this case, b).

The remaining rules list the sub-rules that must be followed; for example, the rule 0: 1 2 means that to match rule 0, the text being checked must match rule 1, and the text after the part that matched rule 1 must then match rule 2.

Some of the rules have multiple lists of sub-rules separated by a pipe (|). This means that at least one list of sub-rules must match. (The ones that match might be different each time the rule is encountered.) For example, the rule 2: 1 3 | 3 1 means that to match rule 2, the text being checked must match rule 1 followed by rule 3 or it must match rule 3 followed by rule 1.

Fortunately, there are no loops in the rules, so the list of possible matches will be finite. Since rule 1 matches a and rule 3 matches b, rule 2 matches either ab or ba. Therefore, rule 0 matches aab or aba.

Here's a more interesting example:

0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

Here, because rule 4 matches a and rule 5 matches b, rule 2 matches two letters that are the same (aa or bb), and rule 3 matches two letters that are different (ab or ba).

Since rule 1 matches rules 2 and 3 once each in either order, it must match two pairs of letters, one pair with matching letters and one pair with different letters. This leaves eight possibilities: aaab, aaba, bbab, bbba, abaa, abbb, baaa, or babb.

Rule 0, therefore, matches a (rule 4), then any of the eight options from rule 1, then b (rule 5): aaaabb, aaabab, abbabb, abbbab, aabaab, aabbbb, abaaab, or ababbb.

The received messages (the bottom part of your puzzle input) need to be checked against the rules so you can determine which are valid and which are corrupted. Including the rules and the messages together, this might look like:

0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb

Your goal is to determine the number of messages that completely match rule 0. In the above example, ababbb and abbbab match, but bababa, aaabbb, and aaaabbb do not, producing the answer 2. The whole message must match all of rule 0; there can't be extra unmatched characters in the message. (For example, aaaabbb might appear to match rule 0 above, but it has an extra unmatched b on the end.)

How many messages completely match rule 0?

"""
from typing import Any, Sequence, Union

import re


def parse_rules(rules: Sequence[str]) -> dict[int, Union[str, list[Union[int, str]]]]:
    rule_map = {}
    for rule in rules:
        key, value = rule.split(": ")
        if not value.isalpha():
            val = []
            for char in value.split(" "):
                if char.isnumeric():
                    val.append(int(char))
                else:
                    val.append(char)
            value = val
        rule_map[int(key)] = value
    return rule_map


def graph_dependencies(
    rules: dict[int, Union[str, list[Union[int, str]]]]
) -> dict[int, set[int]]:
    """
    Return a map of rule ids to the rules they depend on.
    """
    rv = {}
    for rule_id, rule in rules.items():
        if isinstance(rule, str):
            continue
        for dep in rule:
            if dep == "|":
                continue
            rv.setdefault(rule_id, set()).add(dep)
    return rv


def resolve_rule(
    graph: dict[int, set[int]],
    rules: dict[int, Union[str, list[Union[int, str]]]],
    idx: int = 0,
) -> str:
    current = rules[idx]
    if isinstance(current, str):
        return current
    deps = graph[idx]
    for dep in deps:
        resolve_rule(graph, rules, dep)
    rule = rules[idx]
    if "|" in rule:
        split_idx = rule.index("|")
        left, right = rule[:split_idx], rule[split_idx + 1 :]
        left_rv = "".join(rules[clause] for clause in left)
        right_rv = "".join(rules[clause] for clause in right)
        rules[idx] = f"({left_rv}|{right_rv})"
    else:
        rules[idx] = "".join(rules[clause] for clause in rule)
    return rules[idx]


def part_one(rules: Sequence[str], messages: Sequence[str]) -> int:
    parsed_rules = parse_rules(rules)
    dependencies = graph_dependencies(parsed_rules)
    pattern = resolve_rule(dependencies, parsed_rules)
    return sum(re.fullmatch(pattern, message) is not None for message in messages)


"""
--- Part Two ---

As you look over the list of messages, you realize your matching rules aren't quite right. To fix them, completely replace rules 8: 42 and 11: 42 31 with the following:

8: 42 | 42 8
11: 42 31 | 42 11 31

This small change has a big impact: now, the rules do contain loops, and the list of messages they could hypothetically match is infinite. You'll need to determine how these changes affect which messages are valid.

Fortunately, many of the rules are unaffected by this change; it might help to start by looking at which rules always match the same set of values and how those rules (especially rules 42 and 31) are used by the new versions of rules 8 and 11.

(Remember, you only need to handle the rules you have; building a solution that could handle any hypothetical combination of rules would be significantly more difficult.)

For example:

42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba

Without updating rules 8 and 11, these rules only match three messages: bbabbbbaabaabba, ababaaaaaabaaab, and ababaaaaabbbaba.

However, after updating rules 8 and 11, a total of 12 messages match:

    bbabbbbaabaabba
    babbbbaabbbbbabbbbbbaabaaabaaa
    aaabbbbbbaaaabaababaabababbabaaabbababababaaa
    bbbbbbbaaaabbbbaaabbabaaa
    bbbababbbbaaaaaaaabbababaaababaabab
    ababaaaaaabaaab
    ababaaaaabbbaba
    baabbaaaabbaaaababbaababb
    abbbbabbbbaaaababbbbbbaaaababb
    aaaaabbaabaaaaababaa
    aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
    aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba

After updating rules 8 and 11, how many messages completely match rule 0?
"""


def part_two(rules: Sequence[str], messages: Sequence[str]) -> int:
    """
    Return the count of valid messages after changing rule 8 and 11 to recurse.
    """

    """
    Only rule 0 refers to rule 8 or rule 11
    Rule 8 and 11 reference the same rules they did before, but can recurse to themselves.
    The new rule 8 repeats indefinitely to the right, so we can append a "+" to it and let
    the regex engine handle it.
    Rule 11 repeats by appending subrules to each side. E.g. 11 := 42 31 | 42 42 31 31 | 42 42 42 31 31 31 | ...
    Which can be represented as:
        (42{1}31{1} | 42{2}31{2} | ... | 42{n-1}31{n-1} | 42{n}31{n})
    for some value of n that is sufficiently large
    We can identify the largest expansion of 11 that is valid, then for that expansion and each smaller expansion
    prepend rule 8 to it and see if it is a full match for the current message.
    """
    parsed_rules = parse_rules(rules)
    dependencies = graph_dependencies(parsed_rules)
    eight = resolve_rule(dependencies, parsed_rules, idx=8)
    thrity_one = resolve_rule(dependencies, parsed_rules, idx=31)
    fourty_two = resolve_rule(dependencies, parsed_rules, idx=42)
    patterns = [
        re.compile(f"({eight})+{fourty_two}{{{n}}}{thrity_one}{{{n}}}")
        # The upper bound for the range was determined by manually running this
        # starting with 100 then decreasing to the minimum value that
        # produced the same count of valid messages.
        for n in range(1, 6)
    ]
    return sum(
        any(re.fullmatch(pattern, message) is not None for pattern in patterns)
        for message in messages
    )


if __name__ == "__main__":

    def verify(expected: Any, actual: Any) -> None:
        assert expected == actual, f"{expected} != {actual}"

    rules = [
        "0: 1 2",
        "1: a",
        "2: 1 3 | 3 1",
        "3: b",
    ]
    graphed = graph_dependencies(parse_rules(rules))
    expected = {0: {1, 2}, 2: {1, 3}}
    verify(expected, graphed)

    expected = "(ab|ba)"
    rule_zero = resolve_rule(graphed, parse_rules(rules))

    rules = [
        "0: 4 1 5",
        "1: 2 3 | 3 2",
        "2: 4 4 | 5 5",
        "3: 4 5 | 5 4",
        "4: a",
        "5: b",
    ]
    messages = [
        "ababbb",
        "bababa",
        "abbbab",
        "aaabbb",
        "aaaabbb",
    ]
    verify(2, part_one(rules, messages))

    from nineteen_input import rules, messages

    print("Part one: ", part_one(rules, messages))
    print("Part two: ", part_two(rules, messages))