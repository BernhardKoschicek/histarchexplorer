from dataclasses import dataclass
from typing import Optional


@dataclass
class Parser:
    search: list[str]
    entities: list[str]
    linked_entities: list[str]
    cidoc_classes: list[str]
    view_classes: list[str]
    system_classes: list[str]
    type_id: list[int]
    show: list[str]
    first: int
    last: int
    page: int
    export: str
    relation_type: int
    geometry: list[str]
    file_id: int
    properties: list[str]
    download: bool = False
    count: bool = False
    locale: str = 'en'
    sort: str = 'asc'
    column: str = 'name'
    limit: int = 0
    format: str = 'lpx'
    centroid: str = 'false'
    image_size: str = ''

    def __setattr__(
            self,
            name: str,
            value: Optional[str | list[str]] = None) -> None: # pragma: no cover
        if (name in self.__annotations__ and
                isinstance(getattr(self, name), list)):
            if getattr(self, name) is None:
                setattr(self, name, [])
            if isinstance(value, list):
                getattr(self, name).extend(value)
            else:
                getattr(self, name).append(value)
        else:
            super().__setattr__(name, value)

    def __repr__(self) -> str:  # pragma: no cover
        return str(self.__dict__)
