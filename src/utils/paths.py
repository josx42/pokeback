"""A collection of paths for other modules to import and use."""


from pathlib import Path

ROOT = Path(__file__).parents[2].resolve()
SRC = ROOT / 'src'
DATA = SRC / 'resources' / 'data'
SOURCEFILE = DATA / 'source.json'
GENERATIONS = DATA / 'generations'
TYPES = DATA / 'types'