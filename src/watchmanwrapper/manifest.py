import dataclasses
import json
import logging
import os
import pathlib
import re
import textwrap
import typing

import jinja2
import pkg_resources
import pydantic
import pydantic.dataclasses
import yaml

package = __name__.split(".")[0]
TEMPLATES_PATH = pathlib.Path(pkg_resources.resource_filename(package, "templates/"))


class Destination(pydantic.BaseModel):
    dir: str
    user: str
    host: str


class ManifestEntry(pydantic.BaseModel):
    name: str
    status: str
    src: str
    dst: Destination
    sync: str

    def to_json(self):
        dst = self.dst.dir
        dst = str(pathlib.Path(dst).expanduser())
        dst = dst.rstrip("/")
        target = f"{self.dst.user}@{self.dst.host}:{dst}"

        src = self.src
        src = str(pathlib.Path(src).expanduser())
        src = src.rstrip("/")

        sync = self.sync
        sync = sync.replace("SRC", src)
        sync = sync.replace("DST", target)

        stanza = [
            "trigger",
            str(pathlib.Path(src).expanduser()),
            {
                "name": self.name,
                "expression": ["allof", ["type", "f"]],
                "command": sync.split(" "),
            },
        ]
        return json.dumps(stanza, indent=2)

    def render(self, tpl: jinja2.Template):
        out = tpl.render(data=self)
        return out


@pydantic.dataclasses.dataclass
class Watchman:
    entry: ManifestEntry
    path: pathlib.Path
    js: str
    cmd: str = None

    """
    python create event handler
    python call callback automatically
    python access varialbe callback
    """

    def __post_init__(self):
        p1 = self._quote(str(self.entry.src))
        p2 = self._quote(str(self.path.parent.resolve()))
        p3 = self._quote(str(self.path.resolve()))

        username = os.getenv("USER", None)
        x = f"""\
        tail -f /usr/local/var/run/watchman/{username}-state/log &
        watchman watch-list
        cat {p3}
        watchman watch {p1}
        watchman --json-command <{p3}
        watchman trigger-list {p1}
        watchman watch-del {p1}
        watchman watch-del-all
        """
        self.cmd = textwrap.dedent(x)

    def write(self):
        logging.debug(f"writing to {self.path}")
        self.path.write_text(self.js)

    def _quote(self, s: str):
        if re.search(" ", s):
            s = f'"{s}"'
        return s


@dataclasses.dataclass
class ManifestCollection:
    data: typing.List[ManifestEntry]

    def __getitem__(self, index):
        return self.data[index]

    @classmethod
    def create_entries(cls, manifest):
        entries = []
        for dct in manifest["list"]:
            dest = Destination(**dct["dst"])
            x1 = {**dct, "dst": dest}
            man = ManifestEntry(**x1)
            entries.append(man)

        return entries

    @classmethod
    def from_file(cls, path: pathlib.Path):
        with open(path, "r") as stream:
            try:
                manifest = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                raise exc

        entries = cls.create_entries(manifest)
        return cls(entries)

    def __iter__(self):
        return iter(self.data)
