# Pokeback

An API made in Python with [Flask](https://flask.palletsprojects.com/) to serve as backend for my Pokémon type statistics and diversity website project. All data is obtained from the [PokéAPI](https://pokeapi.co/). For detailed info about how this data is collected and processed, see [METHODS.md](./METHODS.md).

## Installation

This project uses Poetry for dependency management. If you'd like to clone it, [install Poetry](https://python-poetry.org/docs/#installation) and run:

```bash
git clone https://github.com/josx42/pokeback.git
cd pokeback
poetry install
```

To run the app, do

```bash
poetry run python -m src.app
```