import json
from pathlib import Path


def read_json(path_to_file: Path) -> dict:
    """Shortcut function to open JSON files."""

    with open(path_to_file) as file:
        data = json.load(file)

    return data


def write_json(data: dict, path_to_file: Path):
    """Shortcut function to write JSON files."""

    with open(path_to_file, 'w') as file:
        json.dump(data, file, indent=2, sort_keys=True)