import requests, roman, json
from time import sleep
from utils.paths import DATA
from utils.constants import BASE_URL, REGION_ONLY, SPECIALS, NO_DEFAULT_FORM

def call(endpoint: str) -> dict:
    """
    Manages requests to PokéAPI, including checking response status, spacing requests in time and
    extracting JSON.\n
    It also works with partial URLs. For example: passing the string `"pokemon"`
    calls the `https://pokeapi.co/api/v2/pokemon` endpoint.
    """

    url = endpoint if endpoint.startswith(BASE_URL) else BASE_URL + endpoint

    response = requests.get(url)
    response.raise_for_status()
    print(f'Successful call to {url}')
    sleep(0.2) # Spacing requests to avoid 429
    return response.json()


def get_chain_members(chain: dict) -> list[str]:
    """Returns the names of all Pokémon in the `evolution-chain`."""

    chain_link = chain['chain']
    members = []

    def parse(chain_link: dict): # Recursive function, complex behavior
        members.append(chain_link['species']['name'])
        for evolution in chain_link['evolves_to']:
            parse(evolution)

    parse(chain_link)
    return members


def get_last_evols(chain: dict) -> list[str]:
    """Returns the names of all Pokémon in the `evolution-chain` that don't evolve any further."""

    chain_link = chain['chain']
    last_evols = []

    def parse(chain_link): # Recursive function, complex behavior
        if not chain_link['evolves_to']:
            last_evols.append(chain_link['species']['name'])
        else:
            for evolution in chain_link['evolves_to']:
                parse(evolution)

    parse(chain_link)
    return last_evols


def find_default_form(species: dict) -> dict:
    """Finds out which of the varieties listed in `pokemon-species` is marked as default, and returns
    it."""

    varieties = species.get('varieties')
    default_varieties = [variety['pokemon'] for variety in varieties if variety['is_default']]
    if len(default_varieties) == 1:
        return default_varieties[0]
    else:
        raise Exception(f'ERROR: multiple default forms found for {species.get('name', 'this Pokemon')}.')


def find_national_dex_num(species: dict) -> int:
    """Finds out which of the Pokedex numbers listed in `pokemon-species` is the one that
    corresponds to the National Pokedex."""

    numbers = species.get('pokedex_numbers')
    national = [item['entry_number'] for item in numbers if item['pokedex']['name'] == "national"]
    if len(national) == 1:
        return national[0]
    else:
        raise Exception(f'ERROR: multiple national pokedex entries found for {species.get('name', 'this Pokemon')}.')


def get_types(pokemon: dict, max_gen: int) -> dict:
    """Receives a JSON object from the PokéAPI's `pokemon` endpoint, and returns a dictionary with a
    `generation: types` key/value pair for each generation up to `max_gen` (included). `types` is a
    list containing the types at the corresponding gen."""

    types = {}
    last_gen_num = 1

    for entry in pokemon['past_types']:
        gen_name = entry['generation']['name']
        gen_num_roman = gen_name.split('-')[-1] # Gen names are in the form "generation-iv"
        gen_num = roman.fromRoman(gen_num_roman)
        types_in_this_entry = [slot['type']['name'] for slot in entry['types']]

        while last_gen_num <= gen_num:
            types[f'gen_{last_gen_num}'] = types_in_this_entry
            last_gen_num += 1

    current_types = [slot['type']['name'] for slot in pokemon['types']]
    while last_gen_num <= max_gen:
        types[f'gen_{last_gen_num}'] = current_types
        last_gen_num += 1

    return types


def get_data(limit = 10) -> list[dict]:
    """
    Accesses PokéAPI, returning a list of every Pokémon that doesn't evolve (i.e., every *"last
    evolution"*) in the form of a dict with the next keys:

    - `name`: The name of the Pokémon, as given by the API.
    - `gen`: The generation it was born into.
    - `national_dex_num`: Its number in the National Pokédex.
    - `region_only`: If it only evolves from a regional form.
    - `types`: The types it had on every generation.

    To prevent excessive requests during development, a `limit` is set to 10. For usage, call the
    function with a high enough number, like 9999.
    """

    data = call(f'pokemon-species?limit={limit}').get('results')
    if not data:
        raise Exception('ERROR: No data found.')

    gens = call('generation').get('count', 9) # Obtain current number of generations and last gen number (same)

    results = []

    names_cache = []
    species_cache = {}

    for pokemon in data:

        name = pokemon['name']
        if name not in names_cache:
            species_data = call(pokemon['url'])
            species_cache[name] = species_data # Caching species data for later
            chain_data = call(species_data['evolution_chain']['url'])

            chain_members = get_chain_members(chain_data)
            names_cache.extend(chain_members) # Caching all evolutions

            last_evols = get_last_evols(chain_data)
            specials_in_chain = set(chain_members).intersection(SPECIALS)
            last_evols.extend(specials_in_chain) # Processing specials when they're part of chain

            for evolution in last_evols:
                if evolution in species_cache: # Caching in line 136 avoids repetitive calls for single-member evolution chains
                    evolution_species_data = species_cache[evolution]
                else:
                    evolution_species_data = call('pokemon-species/' + evolution)

                default_form = find_default_form(evolution_species_data)
                pokemon_data = call(default_form['url'])

                gen = evolution_species_data['generation']['name']
                gen_num_roman = gen.split('-')[-1]
                gen_num = roman.fromRoman(gen_num_roman)

                national_dex_num = find_national_dex_num(evolution_species_data)
                types = get_types(pokemon_data, gens)

                full_json = {'name': evolution,
                             'gen': gen_num,
                             'national_dex_num': national_dex_num,
                             'types': types,
                             'region_only': evolution in REGION_ONLY}
                results.append(full_json)

    # To Do: Replace Pokémon with no default form
    return results

def main():
    result = get_data(9999)

    with open(DATA / 'source.json', 'w') as file:
        json.dump(result, file, indent=2)

    print(f'Results successfully fetched and written to JSON format.')

if __name__ == '__main__':
    main()