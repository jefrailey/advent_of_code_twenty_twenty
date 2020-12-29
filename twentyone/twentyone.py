"""
--- Day 21: Allergen Assessment ---

You reach the train's last stop and the closest you can get to your vacation island without getting wet. There aren't even any boats here, but nothing can stop you now: you build a raft. You just need a few days' worth of food for your journey.

You don't speak the local language, so you can't read any ingredients lists. However, sometimes, allergens are listed in a language you do understand. You should be able to use this information to determine which ingredient contains which allergen and work out which foods are safe to take with you on your trip.

You start by compiling a list of foods (your puzzle input), one food per line. Each line includes that food's ingredients list followed by some or all of the allergens the food contains.

Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen. Allergens aren't always marked; when they're listed (as in (contains nuts, shellfish) after an ingredients list), the ingredient that contains each listed allergen will be somewhere in the corresponding ingredients list. However, even if an allergen isn't listed, the ingredient that contains that allergen could still be present: maybe they forgot to label it, or maybe it was labeled in a language you don't know.

For example, consider the following list of foods:

mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)

The first food in the list has four ingredients (written in a language you don't understand): mxmxvkd, kfcds, sqjhc, and nhms. While the food might contain other allergens, a few allergens the food definitely contains are listed afterward: dairy and fish.

The first step is to determine which ingredients can't possibly contain any of the allergens in any food in your list. In the above example, none of the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen. Counting the number of times any of these ingredients appear in any ingredients list produces 5: they all appear once each except sbzzf, which appears twice.

Determine which ingredients cannot possibly contain any of the allergens in your list. How many times do any of those ingredients appear?
"""

from typing import Any, Counter, NamedTuple


class IngredientsList(NamedTuple):
    ingredients: list[str]
    allergens: list[str]


def parse_ingredient_lists(ingredient_lists: list[str]) -> list[IngredientsList]:
    lists = []
    for ingredient_list in ingredient_lists:
        ingredients, allergens = ingredient_list.split(" (contains ")
        allergens = allergens[:-1]  # Remove ')'
        lists.append(IngredientsList(ingredients.split(" "), allergens.split(", ")))
    return lists


def identify_allergens(ingredient_lists: list[str]) -> dict[str, str]:
    parsed_lists = parse_ingredient_lists(ingredient_lists)
    allergen_candidates = {}
    for parsed in parsed_lists:
        for allergen in parsed.allergens:
            if allergen not in allergen_candidates:
                allergen_candidates[allergen] = set(parsed.ingredients)
            else:
                allergen_candidates[allergen].intersection_update(parsed.ingredients)
    # If we're lucky, then there's at least one allergen mapped to a single ingredient.
    # For each allergen that is mapped to exactly one ingredient, we can add it to the
    # final map.
    # We can then remove its mapped word from the candidate set of every other allergen.
    # Proceed in this manner until all allergens have been added to mapped
    # then reverse mapped
    mapped = {}
    while allergen_candidates.keys() != mapped.keys():
        # look for allergens that have exactly one mapped word
        for allergen in allergen_candidates.keys() - mapped.keys():
            candidates = allergen_candidates[allergen]
            if len(candidates) == 1:
                candidate = candidates.pop()
                mapped[allergen] = candidate
                for other, other_candidates in allergen_candidates.items():
                    if other == allergen:
                        continue
                    if candidate in other_candidates:
                        other_candidates.remove(candidate)
    return {ingredient: allergen for (allergen, ingredient) in mapped.items()}


def part_one(ingredients_list: list[str]):
    """
    Return the appearance count of ingredients that cannot be allergens.
    """
    allergens = identify_allergens(ingredients_list)
    parsed_lists = parse_ingredient_lists(ingredients_list)
    ingredients: set[str] = set()
    for ingredient_list in parsed_lists:
        ingredients.update(ingredient_list.ingredients)
    not_allergens = ingredients - allergens.keys()
    counts: Counter[str] = Counter()
    for ingredient_list in parsed_lists:
        counts.update(ingredient_list.ingredients)
    return sum(
        count for (ingredient, count) in counts.items() if ingredient in not_allergens
    )


"""
--- Part Two ---

Now that you've isolated the inert ingredients, you should have enough information to figure out which ingredient contains which allergen.

In the above example:

    mxmxvkd contains dairy.
    sqjhc contains fish.
    fvjkl contains soy.

Arrange the ingredients alphabetically by their allergen and separate them by commas to produce your canonical dangerous ingredient list. (There should not be any spaces in your canonical dangerous ingredient list.) In the above example, this would be mxmxvkd,sqjhc,fvjkl.

Time to stock your raft with supplies. What is your canonical dangerous ingredient list?
"""


def part_two(ingredients_list: list[str]) -> str:
    """
    Return a comma separated sequence of ingredients sorted alphabetically by allergen.
    """
    allergens = identify_allergens(ingredients_list)

    return ",".join(
        ingredient for (ingredient, _) in sorted(allergens.items(), key=lambda x: x[1])
    )


if __name__ == "__main__":

    def verify(expected: Any, actual: Any) -> None:
        assert expected == actual, f"{expected} != {actual}"

    diagnostic = [
        "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
        "trh fvjkl sbzzf mxmxvkd (contains dairy)",
        "sqjhc fvjkl (contains soy)",
        "sqjhc mxmxvkd sbzzf (contains fish)",
    ]

    verify(
        {"mxmxvkd": "dairy", "sqjhc": "fish", "fvjkl": "soy"},
        identify_allergens(diagnostic),
    )

    verify(5, part_one(diagnostic))

    verify("mxmxvkd,sqjhc,fvjkl", part_two(diagnostic))

    from twentyone_input import ingredient_lists

    print("Part one: ", part_one(ingredient_lists))
    print("Part two: ", part_two(ingredient_lists))