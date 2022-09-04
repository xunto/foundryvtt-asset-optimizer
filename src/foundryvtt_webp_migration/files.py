import os
from pathlib import Path
from typing import Iterator, List, Set


def get_file_paths(
    root_dir: Path,
    ignored_sub_dir_names: Set[str],
) -> Set[Path]:
    ignored_dirs = {root_dir / name for name in ignored_sub_dir_names}

    paths = set()
    for path in root_dir.rglob("*"):
        if _check_ignored_dir(path, ignored_dirs):
            continue

        paths.add(path)

    return paths


def _check_ignored_dir(
    path: Path,
    ignored_dirs: Set[Path],
) -> bool:
    for ignored_dir in ignored_dirs:
        try:
            path.relative_to(ignored_dir)
            return True
        except ValueError:
            pass

    return False
