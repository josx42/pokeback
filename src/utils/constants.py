BASE_URL = 'https://pokeapi.co/api/v2/'

TYPES = [
    'normal', 'fighting', 'flying', 'poison', 'ground', 'rock',
    'bug', 'ghost', 'steel', 'fire', 'water', 'grass',
    'electric', 'psychic', 'ice', 'dragon', 'dark', 'fairy',
    'unknown', 'stellar'
]

# See METHODS.md for info about the next constants
TEMPORARY = {
    'golbat': 2,
    'primeape': 9,
    'magneton': 4,
    'onix': 2,
    'lickytung': 4,
    'rhydon': 4,
    'chansey': 2,
    'tangela': 4,
    'seadra': 2,
    'scyther': 2,
    'electabuzz': 4,
    'magmar': 4,
    'porygon': 2,
    'togetic': 4,
    'aipom': 4,
    'yanma': 4,
    'murkrow': 4,
    'misdreavus': 4,
    'girafarig': 9,
    'dunsparce': 9,
    'gligar': 4,
    'sneasel': 4,
    'piloswine': 4,
    'porygon2': 4,
    'nosepass': 4,
    'roselia': 4,
    'dusclops': 4,
    'bisharp': 9
} # Pokémon que acaban por evolucionar en generaciones posteriores, y la generación en la que lo hacen.

REGION_ONLY = [
    'perrserker',
    'sirfetchd',
    'mr-rime',
    'cursola',
    'obstagoon',
    'runerigus',
    'overqwil',
    'sneasler',
    'clodsire',
    'basculegion',
    'ursaluna',
    'wyrdeer',
    'kleavor'
    ]

SPECIALS = ['mr-mime', 'farfetchd', 'corsola', 'ursaring', 'linoone', 'qwilfish', 'basculin', 'stantler']

NO_DEFAULT_FORM = ['wormadam', 'oricorio', 'ursaluna', 'urshifu']