import logging
from pathlib import Path
from typing import Dict, Iterable, Set

from PIL import Image

logger = logging.getLogger(__name__)

_UNCONVERTED_IMAGE_EXTENSIONS = (".avif", ".jpg", ".jpeg", ".png")


def filter_image_files(files: Iterable[Path]) -> Set[Path]:
    return set(
        filter(lambda path: path.suffix.lower() in _UNCONVERTED_IMAGE_EXTENSIONS, files)
    )


def convert_images(
    images: Iterable[Path],
    quality: int,
) -> Dict[Path, Path]:
    path_map = {}

    for path in images:
        output_path = _convert_to_webp(path, quality)
        path_map[path] = output_path

    return path_map


def _convert_to_webp(
    image_path: Path,
    quality: int,
) -> Path:
    """

    :param image_path:
    :param quality:
    :return:
    """
    assert 0 <= quality <= 100, "Only 0<=quality<=100 is allowed."

    logger.info(f"Converting {image_path} to webp")

    output_path = image_path.with_suffix(".webp")

    image = Image.open(image_path)
    image.save(
        output_path,
        format="webp",
        optimize=True,
        quality=quality,
    )

    return output_path
