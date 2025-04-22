import json
from itertools import combinations
from utils.paths import DATA
from fetcher import call

with open(DATA / 'source.json', 'r') as file:
    data = json.load(file)


def count_types(data: dict, types: list, gen_num: int, accumulated = False):

    gen = f'gen_{gen_num}'

    count = 0
    for pokemon in data:
        counted = sorted(pokemon['types'][gen]) == sorted(types)

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


types_data = call('type').get('results')
types = [result['name'] for result in types_data]
types.remove('unknown'); types.remove('stellar')


def create_gen_monotypes(gen_num: int, accumulated = False):
    count = {'generation': gen_num}
    suffix = 'accumulated' if accumulated else ''

    for type in types:
        count[type] = count_types(data, [type], gen_num, accumulated)

        with open(DATA / f'gen_{gen_num}_monotypes{suffix}', 'w') as file:
            json.dump(count, file, indent=2)


def create_gen_combinations(gen_num: int, accumulated = False):
    count = {'generation': gen_num}
    duals = [list(dual) for dual in combinations(types, 2)]
    suffix = 'accumulated' if accumulated else ''

    for dual in duals:
        count[str(dual)] = count_types(data, dual, gen_num, accumulated)

        with open(DATA / f'gen_{gen_num}_duals{suffix}') as file:
            json.dump(count, file, indent=2)


def create_type_graph(type: str, accumulated = False):
    count = {}
    suffix = 'accumulated' if accumulated else ''
    for gen in range(1, 10):
        count[type] = count_types(data, [type], gen, accumulated)

    with open(DATA / f'{type}_{suffix}') as file:
        json.dump(count, file, indent=2)


def main():
    poison = count_types(data, ['poison', 'fighting'], 9, accumulated=True)
    print(poison)

if __name__ == '__main__':
    main()