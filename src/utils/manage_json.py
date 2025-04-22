import json
from pathlib import Path


def read_json(path_to_file: Path) -> dict:

    with open(path_to_file) as file:
        data = json.load(file)

    return data


def write_json(data: dict, path_to_file: Path):

    with open(path_to_file) as file:
        json.dump(data, file, indent=2)