import json
from pathlib import Path
from src.utils.paths import SOURCEFILE

def read_json(path_to_file: Path) -> dict | list:
    """Shortcut function to open JSON files."""

    with open(path_to_file) as file:
        data = json.load(file)

    return data


def write_json(data, path_to_file: Path):
    """Shortcut function to write JSON files."""

    temp_path = path_to_file.with_suffix('.tmp')
    with open(temp_path, 'w') as file:
        json.dump(data, file, indent=2, sort_keys=True)

    temp_path.replace(path_to_file)


def is_source_ok():
    """Checks if the source file exists and has the correct data inside."""

    if not SOURCEFILE.exists():
        return False

    try:
        content = read_json(SOURCEFILE)

        if not isinstance(content, list):
            return False

        if len(content) == 0:
            return False

        required_keys = {'evolves_at', 'name', 'gen', 'region_only', 'types'}
        for item in content:
            if not required_keys.issubset(item.keys()):
                return False

    except (OSError, json.JSONDecodeError):
        return False

    return True