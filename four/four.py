"""
--- Day 4: Passport Processing ---

You arrive at the airport only to realize that you grabbed your North Pole Credentials instead of your passport. While these documents are extremely similar, North Pole Credentials aren't issued by a country and therefore aren't actually valid documentation for travel in most of the world.

It seems like you're not the only one having problems, though; a very long line has formed for the automatic passport scanners, and the delay could upset your travel itinerary.

Due to some questionable network security, you realize you might be able to solve both of these problems at the same time.

The automatic passport scanners are slow because they're having trouble detecting which passports have all required fields. The expected fields are as follows:

    byr (Birth Year)
    iyr (Issue Year)
    eyr (Expiration Year)
    hgt (Height)
    hcl (Hair Color)
    ecl (Eye Color)
    pid (Passport ID)
    cid (Country ID)

Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of key:value pairs separated by spaces or newlines. Passports are separated by blank lines.

Here is an example batch file containing four passports:

ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in

The first passport is valid - all eight fields are present. The second passport is invalid - it is missing hgt (the Height field).

The third passport is interesting; the only missing field is cid, so it looks like data from North Pole Credentials, not a passport at all! Surely, nobody would mind if you made the system temporarily ignore missing cid fields. Treat this "passport" as valid.

The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any other field is not, so this passport is invalid.

According to the above rules, your improved system would report 2 valid passports.

Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file, how many passports are valid?
"""

import re
from typing import Sequence


def has_required_fields(passport: dict[str, str]) -> bool:
    required = {
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
    }
    return set(passport.keys()).issuperset(required)


def parse_file(batch_file: str) -> Sequence[dict[str, str]]:
    passports = batch_file.split("\n\n")
    passports = [passport.replace("\n", " ").split(" ") for passport in passports]
    return [dict(pair.split(":") for pair in passport) for passport in passports]


def is_birth_year_valid(candidate: str) -> bool:
    """
    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    """
    return is_between(candidate, 1920, 2002)


def is_between(candidate: str, min_: int, max_: int) -> bool:
    return candidate.isnumeric() and min_ <= int(candidate) <= max_


def is_issue_year_valid(candidate: str) -> bool:
    """
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    """
    return is_between(candidate, 2010, 2020)


def is_expiration_year_valid(candidate: str) -> bool:
    """
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    """
    return is_between(candidate, 2020, 2030)


def is_height_valid(candidate: str) -> bool:
    """
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    """
    allowed = {"cm": [150, 193], "in": [59, 76]}
    units = candidate[-2:]
    if units not in allowed:
        return False
    digits = candidate[:-2]
    range_ = allowed[units]
    return is_between(digits, *range_)


def is_hair_color_valid(candidate: str) -> bool:
    """
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    """
    return re.fullmatch("#[0-9a-f]{6}", candidate) is not None


def is_eye_color_valid(candidate: str) -> bool:
    """
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    """
    allowed = set("amb blu brn gry grn hzl oth".split(" "))
    return candidate in allowed


def is_passport_id_valid(candidate: str) -> bool:
    """
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    """
    return re.fullmatch("[0-9]{9}", candidate) is not None


def is_valid(passport: dict[str, str]) -> bool:
    if not has_required_fields(passport):
        return False

    return all(
        [
            is_birth_year_valid(passport["byr"]),
            is_issue_year_valid(passport["iyr"]),
            is_expiration_year_valid(passport["eyr"]),
            is_height_valid(passport["hgt"]),
            is_hair_color_valid(passport["hcl"]),
            is_eye_color_valid(passport["ecl"]),
            is_passport_id_valid(passport["pid"]),
        ]
    )


"""
--- Part Two ---

The line is moving more quickly now, but you overhear airport security talking about how passports with invalid data are getting through. Better add some data validation, quick!

You can continue to ignore the cid field, but each other field has strict rules about what values are valid for automatic validation:

    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.

Your job is to count the passports where all required fields are both present and valid according to the above rules. Here are some example values:

byr valid:   2002
byr invalid: 2003

hgt valid:   60in
hgt valid:   190cm
hgt invalid: 190in
hgt invalid: 190

hcl valid:   #123abc
hcl invalid: #123abz
hcl invalid: 123abc

ecl valid:   brn
ecl invalid: wat

pid valid:   000000001
pid invalid: 0123456789

Here are some invalid passports:

eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007

Here are some valid passports:

pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719

Count the number of valid passports - those that have all required fields and valid values. Continue to treat cid as optional. In your batch file, how many passports are valid?
"""

if __name__ == "__main__":
    from input_four import input_

    diagnostic = "\n".join(
        [
            "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
            "byr:1937 iyr:2017 cid:147 hgt:183cm",
            "",
            "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
            "hcl:#cfa07d byr:1929",
            "",
            "hcl:#ae17e1 iyr:2013",
            "eyr:2024",
            "ecl:brn pid:760753108 byr:1931",
            "hgt:179cm",
            "",
            "hcl:#cfa07d eyr:2025 pid:166559648",
            "iyr:2011 ecl:brn hgt:59in",
        ]
    )
    assert (
        sum(has_required_fields(passport) for passport in parse_file(diagnostic)) == 2
    )

    assert is_birth_year_valid("2002")
    assert not is_birth_year_valid("2003")

    assert is_height_valid("60in")
    assert is_height_valid("190cm")
    assert is_height_valid("74in")
    assert not is_height_valid("190in")
    assert not is_height_valid("190")

    assert is_hair_color_valid("#123abc")
    assert is_hair_color_valid("#623a2f")
    assert not is_hair_color_valid("#123abz")
    assert not is_hair_color_valid("123abc")

    assert is_eye_color_valid("brn")
    assert is_eye_color_valid("grn")
    assert not is_eye_color_valid("wat")

    assert is_passport_id_valid("000000001")
    assert is_passport_id_valid("087499704")
    assert not is_passport_id_valid("0123456789")

    assert is_issue_year_valid("2012")

    assert is_expiration_year_valid("2030")

    assert is_birth_year_valid("1980")

    invalids_file = "\n".join(
        [
            "eyr:1972 cid:100",
            "hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926",
            "",
            "iyr:2019",
            "hcl:#602927 eyr:1967 hgt:170cm",
            "ecl:grn pid:012533040 byr:1946",
            "",
            "hcl:dab227 iyr:2012",
            "ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277",
            "",
            "hgt:59cm ecl:zzz",
            "eyr:2038 hcl:74454a iyr:2023",
            "pid:3556412378 byr:2007",
        ]
    )

    assert sum(is_valid(passport) for passport in parse_file(invalids_file)) == 0

    valids_file = "\n".join(
        [
            "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980",
            "hcl:#623a2f",
            "",
            "eyr:2029 ecl:blu cid:129 byr:1989",
            "iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm",
            "",
            "hcl:#888785",
            "hgt:164cm byr:2001 iyr:2015 cid:88",
            "pid:545766238 ecl:hzl",
            "eyr:2022",
            "",
            "iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719",
        ]
    )

    assert all(is_valid(passport) for passport in parse_file(valids_file))

    passports = parse_file(input_)
    print(
        "Part one: ",
        sum(has_required_fields(passport) for passport in passports),
    )

    print("Part two: ", sum(is_valid(passport) for passport in passports))
