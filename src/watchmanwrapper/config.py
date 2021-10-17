# -*- python -*-
import dataclasses
import logging
import pathlib

import appdirs
import jinja2
import monacelli_pylog_prefs.logger
import pkg_resources

appname = "watchmanwrapper"
appauthor = "taylormonacelli"

package = __name__.split(".")[0]
TEMPLATES_PATH = pathlib.Path(pkg_resources.resource_filename(package, "templates/"))


@dataclasses.dataclass
class Config:
    dir: str = appdirs.user_config_dir(appname, appauthor)
    path: pathlib.Path = None
    config: str = None

    def __post_init__(self):
        self.path = pathlib.Path(self.dir) / "manifest.yml"
        template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
        template_env = jinja2.Environment(loader=template_loader)
        TEMPLATE_FILE = "manifest.yaml.j2"
        template = template_env.get_template(TEMPLATE_FILE)
        outputText = template.render()
        self.config = outputText

    def write(self):
        pathlib.Path.mkdir(self.path.parent, parents=True, exist_ok=True)
        logging.warning(f"creating file {self.path}")
        self.path.write_text(self.config)


def main():
    monacelli_pylog_prefs.logger.setup(
        filename=f"{pathlib.Path(__file__).stem}.log", stream_level=logging.DEBUG
    )
    config = Config()
    if not config.path.exists():
        config.write()


if __name__ == "__main__":
    main()
