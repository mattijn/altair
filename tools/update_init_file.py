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
"""

INIT_REMAINING = """\
def __dir__():
    return __all__    

from .vegalite import *


def load_ipython_extension(ipython):
    from ._magics import vegalite

    ipython.register_magic_function(vegalite, "cell")
"""

def generate_vegalite_init():

    visible_modules = "\n".join([f'"{x}"' for x in dir(alt) if not getattr(getattr(alt, x), "_deprecated", False)])
    contents = [HEADER, VERSION]
    contents.append(f'__all__ = [\n{visible_modules}\n]')
    contents.extend(['\n',INIT_REMAINING])
    
    return "\n".join(contents)

def write_init_file():

    # Generate the __init__ file
    altairdir = abspath(join(dirname(__file__), "..", "altair"))
    outfile = join(altairdir, "__init__.py")
    print("Updating ->{}".format(outfile))
    file_contents = generate_vegalite_init()
    with open(outfile, "w", encoding="utf8") as f:
        f.write(file_contents)

if __name__ == "__main__":
    write_init_file()