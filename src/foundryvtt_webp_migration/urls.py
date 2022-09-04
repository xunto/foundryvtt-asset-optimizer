from pathlib import Path
from typing import Dict


def convert_path_map_to_url_map(root_path: Path, path_map: Dict[Path, Path]) -> Dict[str, str]:
    url_map = {}

    for key, value in path_map.items():
        new_key = convert_path_to_url(root_path, key)
        new_value = convert_path_to_url(root_path, value)
        url_map[new_key] = new_value

    return url_map


def convert_path_to_url(root_path: Path, path: Path) -> str:
    return "/".join(path.relative_to(root_path).parts)
