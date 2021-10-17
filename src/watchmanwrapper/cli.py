"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mwatchmanwrapper` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``watchmanwrapper.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``watchmanwrapper.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import sys


def main(argv=sys.argv):
    manifest_path = pathlib.Path("manifest.yml")
    col = ManifestCollection.from_file(manifest_path)
    man = col[0]
    print(man.dict())

    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Does stuff.
    """
    print(argv)
    return 0
