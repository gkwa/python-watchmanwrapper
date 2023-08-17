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
import argparse
import logging
import pathlib
import re
import sys

import jinja2
import monacelli_pylog_prefs.logger
import pkg_resources

import watchmanwrapper.config
import watchmanwrapper.manifest

parser = argparse.ArgumentParser()
parser.add_argument(
    "--log",
    dest="logLevel",
    default="INFO",
    choices=[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ],
    help="Set the logging level",
)

parser.add_argument(
    "-l",
    "--limit",
    dest="filter",
    default=".",
    help="Filter by string",
)


parser.add_argument(
    "--no-autorun",
    action="store_true",
    default=False,
    help="Dont automatically run",
)


package = __name__.split(".")[0]
TEMPLATES_PATH = pathlib.Path(pkg_resources.resource_filename(package, "templates/"))


# Custom filter method
def regex_replace(s, find, replace):
    """A non-optimal implementation of a regex filter"""
    return re.sub(find, replace, s)


outdir = pathlib.Path("/tmp/watchman")


def main(argv=sys.argv):
    args = parser.parse_args()
    monacelli_pylog_prefs.logger.setup(
        filename=f"{pathlib.Path(__file__).stem}.log",
        stream_level=args.logLevel.upper(),
    )
    config = watchmanwrapper.config.Config()
    if not config.path.exists():
        config.write()

    logging.debug(f"reading from {config.path}")
    manifest_collection = watchmanwrapper.manifest.ManifestCollection.from_file(
        config.path
    )

    template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
    env = jinja2.Environment(loader=template_loader)
    env.filters["regex_replace"] = regex_replace

    pattern = re.compile(args.filter)

    for entry in manifest_collection:
        template = env.get_template("bash.sh.j2")
        path = outdir / f"{entry.name}.sh"

        if not pattern.search(str(path)):
            continue

        pathlib.Path.mkdir(outdir, parents=True, exist_ok=True)
        out = entry.render(template)
        logging.debug(f"writing to {path}")
        path.write_text(out)

        path = outdir / f"{entry.name}.json"
        man = watchmanwrapper.manifest.Watchman(
            entry=entry, path=path, js=entry.to_json()
        )

        man.write()
        if not args.no_autorun:
            man.run_flow1()

    return 0
