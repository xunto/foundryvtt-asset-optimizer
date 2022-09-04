import logging
from pathlib import Path

import click as click

from foundryvtt_webp_migration.db import filter_db_files, migrate_databases
from foundryvtt_webp_migration.files import get_file_paths
from foundryvtt_webp_migration.urls import convert_path_map_to_url_map
from .image import convert_images, filter_image_files


def _configure_logging():
    FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel(logging.INFO)


@click.command()
@click.argument(
    "DATA_PATH",
    type=click.Path(
        exists=True,
        file_okay=False,
        path_type=Path,
    ),
)
@click.option(
    "--quality",
    "-q",
    type=click.IntRange(0, 100),
    default=80,
)
def main(
    data_path: Path,
    quality: int,
):
    _configure_logging()

    files = get_file_paths(
        data_path,
        ignored_sub_dir_names={"modules", "systems"},
    )

    image_files = filter_image_files(files)
    path_map = convert_images(image_files, quality)

    url_map = convert_path_map_to_url_map(data_path, path_map)

    db_files = filter_db_files(files)
    migrate_databases(
        db_files,
        url_map,
    )


if __name__ == "__main__":
    main()
