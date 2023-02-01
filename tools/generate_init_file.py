"""
This script creates the altair/__init__.py
based on the updated Altair schema.
"""
import argparse
from os.path import abspath, dirname, join
import sys

# Import Altair from head
ROOT_DIR = abspath(join(dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)
import altair as alt  # noqa: E402

HEADER = """\
# The contents of this file are automatically written by
# tools/generate_schema_wrapper.py. Do not modify directly.
"""

VERSION = """\
# flake8: noqa
__version__ = "4.3.0.dev0"

from .vegalite import *
"""

INIT_REMAINING = """\
def __dir__():
    return __all__


def load_ipython_extension(ipython):
    from ._magics import vegalite

    ipython.register_magic_function(vegalite, "cell")
"""


def generate_vegalite_init(hide_deprecated):
    contents = [HEADER, VERSION]

    if hide_deprecated is True:
        visible_modules = "\n".join(
            [
                f'"{x}",'
                for x in dir(alt)
                if not getattr(getattr(alt, x), "_deprecated", False)
            ]
        )
        contents.append(f"__all__ = [\n{visible_modules}\n]")
        contents.extend(["\n", INIT_REMAINING])

    return "\n".join(contents)


def write_init_file(hide_deprecated):
    # Generate the __init__ file
    altairdir = abspath(join(dirname(__file__), "..", "altair"))
    outfile = join(altairdir, "__init__.py")
    print("Updating ->{}".format(outfile))

    # collect content to write in __init__.py
    file_contents = generate_vegalite_init(hide_deprecated=hide_deprecated)
    with open(outfile, "w", encoding="utf8") as f:
        f.write(file_contents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="generate_init_file.py",
        description="Generate the init file for the Altair package.",
    )
    parser.add_argument(
        "--hide-deprecated",
        action="store_true",
        help="will populate the __all__ directive, hiding deprecated methods",
    )
    parser.add_argument(
        "--no-hide-deprecated",
        dest="hide_deprecated",
        action="store_false",
        help="include all methods, including deprecated methods",
    )
    parser.set_defaults(hide_deprecated=True)
    args = parser.parse_args()
    write_init_file(args.hide_deprecated)
