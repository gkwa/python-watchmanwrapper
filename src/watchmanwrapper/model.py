import dataclasses
import pathlib
import typing

import pydantic
import yaml


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


@dataclasses.dataclass
class ManifestCollection:
    data: typing.List[ManifestEntry]

    def __getitem__(self, index):
        return self.data[index]

    @classmethod
    def from_file(cls, path: pathlib.Path):
        with open(path, "r") as stream:
            try:
                manifest = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                raise exc

        entries = []
        for dct in manifest["list"]:
            dest = Destination(**dct["dst"])
            x1 = {**dct, "dst": dest}
            man = ManifestEntry(**x1)
            entries.append(man)

        return cls(entries)

    def append(self, entry: ManifestEntry):
        self.data.append(entry)

    def validate(self):
        seen = {}
        # FIXME: you should make sure that all destination directories do not have tilde
        """
        python loop over all properties of object
        """

        for entry in self.data:
            if seen.get(entry.data.name, None):
                # FIXME: use more appropriate exception here
                raise BaseException
            seen[entry.data.name] = 1

        seen = {}
        for entry in self.data:
            if seen.get(entry.data.src, None):
                # FIXME: use more appropriate exception here
                raise BaseException
            seen[entry.data.src] = 1

    def __iter__(self):
        return iter(self.data)
