# Imports from built-in modules
from itertools import combinations
# Imports from installed modules
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
# Imports from own modules
from src.utils.paths import DATA, GENERATIONS, TYPES
from src.utils.manage_json import read_json, write_json
from src.resources.fetcher import call, get_data
from src.resources.calculations import get_balance, get_diversity, get_total_type_weight, get_types_count


def update(from_scratch = False):
    """Updates all resources. If `from_scratch` is `True`, it performs all the logic pertaining
    PokéAPI, including many requests, and creates the main resource. Otherwise, it works locally
    from the preexistent file."""

    if from_scratch:
        source = get_data(9999)
        write_json(source, DATA / 'source.json')
        print('Main data successfully fetched and written to JSON format.')
    else:
        source = read_json(DATA / 'source.json')

    gens = call('generation').get('count', 9)

    types_data = call('type').get('results')
    types = [result['name'] for result in types_data]
    types.remove('unknown'); types.remove('stellar')


    def create_gen_resource(gen_num: int, partial: bool, accumulated: bool):
        """It creates a resource for the generation of the given `gen_num`, including a count of Pokémon of every type and statistic indexes for them, writing it all to a JSON file.

        All of this function's parameters are passed to functions `get_types_count` and `get_total_type_weight` from the `calculations` module. Refer to said module for more info."""

        result = {'generation': gen_num, 'counters': []}
        weights = []

        adjusted_types = types.copy()
        if gen_num < 6:
            adjusted_types.remove('fairy')
        if gen_num < 2:
            adjusted_types.remove('steel')
            adjusted_types.remove('dark')

        duals = list(combinations(adjusted_types, 2))
        all_typings = duals + [(type, ) for type in adjusted_types] # Normalize typing format
        typings = [(type, ) for type in adjusted_types] if partial else all_typings
        for typing in typings:
            count = get_types_count(source, gen_num, *typing, partial = partial, accumulated = accumulated)
            counter = {'types': [typing] if partial else list(typing), 'count': count}
            result['counters'].append(counter)

            if partial:
                weight = get_total_type_weight(source, gen_num, typing[0], accumulated = accumulated)
            else:
                weight = count # For strict counts, weight = count
            weights.append(weight)

        result['diversity'] = get_diversity(weights)
        result['balance'] = get_balance(weights)

        mode = 'partial' if partial else 'strict'
        suffix = '_accumulated' if accumulated else ''
        write_json(result, GENERATIONS / f'gen_{gen_num}_{mode}{suffix}.json')
        prefix = '' if accumulated else 'non-'
        print(f'Data for generation {gen_num} ({prefix}accumulated) successfully writen to JSON file.')


    def create_type_resource(type: str, accumulated: bool):
        result = {'type': type, 'counters': []}
        suffix = '_accumulated' if accumulated else ''

        for gen_num in range(1, gens + 1):
            count = get_types_count(source, gen_num, type, partial = True, accumulated = accumulated)
            counter = {'generation': gen_num, 'count': count}
            result['counters'].append(counter)

        write_json(result, TYPES / f'{type}{suffix}.json')
        print(f'Data for {type} type at every generation successfully writen to JSON file.')


    for gen in range(1, gens + 1):
        for mode in [(True, True), (True, False), (False, False), (False, True)]:
            create_gen_resource(gen, mode[0], mode[1])

    for type in types:
        create_type_resource(type, False)
        create_type_resource(type, True)

    print('Resources successfully updated.')


def auto_update():
    scheduler = BackgroundScheduler()
    date_to_run = CronTrigger(month=2, day=1, hour=0, minute=0)

    scheduler.add_job(update, date_to_run)
    scheduler.start()


if __name__ == '__main__':
    update()