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
        data = f.read()

    for needle, replace in url_map.items():
        data = data.replace(
            f'"{needle}"',
            f'"{replace}"',
        )
        data = data.replace(
            f'"{parse.quote(needle)}"',
            f'"{parse.quote(replace)}"',
        )

    with db_file.open("w") as f:
        f.write(data)
