import pathlib
from typing import Any, Dict

from setuptools import find_namespace_packages, setup


PROJECT_DIR = pathlib.Path(__file__).resolve().parent
SRC_DIR_NAME = "src"


def load_about() -> Dict[str, Any]:
    module_path = (
        PROJECT_DIR / SRC_DIR_NAME / "foundryvtt_asset_optimizer" / "__about__.py"
    )
    module_globals: Dict[str, Any] = {}
    exec(module_path.read_text("utf-8"), module_globals)
    # Remove private/magick global variables of the module
    unwanted_names = module_globals.keys() - set(module_globals["__all__"])
    for name in unwanted_names:
        del module_globals[name]
    return module_globals


ABOUT = load_about()


if __name__ == "__main__":
    setup(
        name="foundryvtt_asset_optimizer",
        version=ABOUT["__version__"],
        packages=find_namespace_packages(SRC_DIR_NAME),
        package_dir={"": SRC_DIR_NAME},
        python_requires="~=3.8",
        entry_points={
            "console_scripts": [
                "foundryvtt-asset-optimizer=foundryvtt_asset_optimizer.cli:main",
            ],
        },
        install_requires=[
            "click",
            "Pillow",
        ],
        extras_require={
            "dev": [
                "pytest",
                "black",
                "isort",
            ]
        },
        # Optional
        author=ABOUT["__author__"],
        author_email=ABOUT["__email__"],
        url=ABOUT["__url__"],
    )
