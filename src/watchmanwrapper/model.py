import dataclasses
import pprint
import sys
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
