from math import log10

def get_types_count(source: dict, gen_num: int, *types: str, partial = False, accumulated = False):
    """Counts how many Pokémon in the `source` dictionary have the specified types. The dict should
    be a "gen" resource.

    If `partial` is set to `True`, `types` should be a single string value and Pokémon whose typing
    contains that type will be counted. Otherwise, `types` should be 1 or 2 string arguments and
    only Pokémon of such combination of types will be counted.

    If `accumulated` is set to `False`, Pokémon are counted only if they belong to the generation of
    the specified `gen_num`. Otherwise, they are also counted if they existed prior to that gen."""

    if (partial and len(types) != 1) or (not partial and len(types) > 2):
        raise ValueError(f'Wrong number of arguments for the "types" parameter. Expected {1 if partial else 2}, received {len(types)}.')

    gen_name = f'gen_{gen_num}'

    count = 0
    for pokemon in source:
        if partial:
            counted = types[0] in pokemon['types'][gen_name]
        else:
            counted = sorted(pokemon['types'][gen_name]) == sorted(types) # This line also allows for tuple usage when passing types, since sorted() returns lists

        if counted:
            exists = pokemon['gen'] <= gen_num
            from_this_gen = pokemon['gen'] == gen_num
            region_only = pokemon['region_only']
            available = (exists and not region_only) or from_this_gen # If Pokémon is region-only (Perrserker, for example), it's only available in case we are "playing" in the generation it's from. See METHODS.md for more info.

            if not accumulated and from_this_gen:
                count += 1
            if accumulated and available:
                count += 1

    return count


def get_total_type_weight(source: dict, gen_num: int, type: str, accumulated = False):
    """Returns the total weight of a `type` in the generation of the given `gen_num`, by reading a
    `source` dictionary obtained from a generation JSON resource. Each available Pokémon of said
    type has a weight of 1 if it's mono-type or 0,5 if it has two types. This function returns the
    sum of all weights.

    If `accumulated` is set to `False`, Pokémon are counted only if they belong to the generation of
    the specified `gen_num`. Otherwise, they are also counted if they existed prior to that gen."""

    gen_name = f'gen_{gen_num}'
    weight = 0.0
    for pokemon in source:
        typing = pokemon['types'][gen_name]
        if type in typing:
            exists = pokemon['gen'] <= gen_num
            from_this_gen = pokemon['gen'] == gen_num
            region_only = pokemon['region_only']
            available = (exists and not region_only) or from_this_gen # If Pokémon is region-only (Perrserker, for example), it's only available in case we are "playing" in the generation it's from. See METHODS.md for more info.

            if (accumulated and available) or from_this_gen:
                fraction = 1.0 if len(typing) == 1 else 0.5
                weight += fraction

    return weight


def get_balance(data: list[float]):
    """Returns the "balance" of the `data` as a number from 0 to 100 (a percentage). This is an
    adaptation of the Gini coefficient used in economics."""
    sorted_data = sorted(data)
    n = len(data)
    cumulative_diffs = 0

    for i, xi in enumerate(sorted_data, start=1):
        cumulative_diffs += (2 * i - n - 1) * xi

    gini_index = cumulative_diffs / (n * sum(data))
    percentage = (1 - gini_index) * 100

    return percentage


def get_diversity(data: list[float]):
    """Returns the diversity of the `data` sample, adapted from the Shannon index used in ecology,
    as a percentage (a float from 0 to 100)."""
    S = len(data)
    N = sum(data)
    max_index = log10(S)

    summation_components = []
    for weight in data:
        if weight > 0:
            relative_weight = weight / N
            component = relative_weight * log10(relative_weight)
            summation_components.append(component)

    shannon_index = -sum(summation_components)
    equity = shannon_index / max_index
    percentage = equity * 100

    return percentage