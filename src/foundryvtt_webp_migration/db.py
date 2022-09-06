import json
import logging
from pathlib import Path
from typing import Dict, Iterable, Set
from urllib import parse


logger = logging.getLogger(__name__)


def filter_db_files(paths: Iterable[Path]) -> Set[Path]:
    return set(filter(lambda path: path.suffix.lower() == ".db", paths))


def migrate_databases(
    db_files: Iterable[Path],
    url_map: Dict[str, str],
) -> None:
    for db_file in db_files:
        migrate_database(
            db_file,
            url_map,
        )


def migrate_database(
    db_file: Path,
    url_map: Dict[str, str],
):
    logger.info(f"Updating database {db_file}")

    with db_file.open() as f:
        db = f.read()

    with db_file.with_suffix(".new").open("w") as f:
        for line in db.split("\n"):
            if not line:
                f.write(line)
            else:
                data = json.loads(line)
                _replace_links_in_dict(data, url_map)
                f.write(json.dumps(data))


def _replace_links_in_dict(
    data: Dict,
    url_map: Dict[str, str],
):
    for needle, replace in url_map.items():
        _replace_value_in_dict(data, needle, replace)
        _replace_value_in_dict(data, parse.quote(needle), parse.quote(replace))


def _replace_value_in_dict(data: Dict, needle: str, replace_with: str) -> None:
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.replace(needle, replace_with)

        if isinstance(value, Dict):
            _replace_value_in_dict(value, needle, replace_with)
