from itertools import combinations
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.utils.paths import DATA, GENERATIONS, TYPES
from src.utils.manage_json import read_json, write_json
from src.resources.fetcher import call, get_data

types_data = call('type').get('results')
types = [result['name'] for result in types_data]
types.remove('unknown'); types.remove('stellar')

gens = call('generation').get('count', 9)

# source = read_json(DATA / 'source.json')

def count_types(data: dict, types: list, gen_num: int, accumulated = False):
    """Takes a `data` dictionary to count how many Pokémon of the passed type are there in the
    generation of the corresponding `gen_num`. `types` is a list of one or two types in the form of
    strings. If `accumulated` is set to `True`, it also counts Pokémon from past generations."""

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


def create_source_file(data):
    write_json(data, DATA / 'source.json')
    print('Results successfully fetched and written to JSON format.')


def create_gen_monotypes(data: dict, gen_num: int, accumulated = False):
    count = {'generation': gen_num}
    for type in types:
        count[type] = count_types(data, [type], gen_num, accumulated)

    suffix = '_accumulated' if accumulated else ''
    write_json(count, GENERATIONS / f'gen_{gen_num}_monotypes{suffix}.json')
    print(f'Data for generation {gen_num} monotypes successfully writen to JSON file.')


def create_gen_combinations(data: dict, gen_num: int, accumulated = False):
    count = {'generation': gen_num, 'combinations': []}
    duals = [list(dual) for dual in combinations(types, 2)]
    for dual in duals:
        own_counter = {'types': dual}
        own_counter['count'] = count_types(data, dual, gen_num, accumulated)
        count['combinations'].append(own_counter)

    suffix = '_accumulated' if accumulated else ''
    write_json(count, GENERATIONS / f'gen_{gen_num}_duals{suffix}.json')
    print(f'Data for generation {gen_num} types combinations successfully writen to JSON file.')


def create_type_graphs(data: dict, type: str, accumulated = False):
    count = {'type': type}
    suffix = '_accumulated' if accumulated else ''
    for gen_num in range(1, gens + 1):
        count[f'gen_{gen_num}'] = count_types(data, [type], gen_num, accumulated)

    write_json(count, TYPES / f'{type}{suffix}.json')
    print(f'Data for type {type} at every generation successfully writen to JSON file.')





def update():
    source = get_data(9999)

    create_source_file(source)

    for gen in range(1, gens + 1):
        create_gen_monotypes(source, gen)
        create_gen_monotypes(source, gen, accumulated=True)

        create_gen_combinations(source, gen)
        create_gen_combinations(source, gen, accumulated=True)

    for type in types:
        create_type_graphs(source, type)
        create_type_graphs(source, type, accumulated=True)

    print('Resources successfully updated.')

def auto_update():
    scheduler = BackgroundScheduler()
    date_to_run = CronTrigger(month=2, day=1, hour=0, minute=0)

    scheduler.add_job(update, date_to_run)
    scheduler.start()


if __name__ == '__main__':
    update()