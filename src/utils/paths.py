"""A collection of paths for other modules to import and use."""


from pathlib import Path

ROOT = Path(__file__).parents[2].resolve()
SRC = ROOT / 'src'
RESOURCES = SRC / 'resources'
DATA = RESOURCES / 'data'
UTILS = SRC / 'utils'