from dataclasses import dataclass


@dataclass
class Parser:
    search: list[str] = None
    entities: list[str] = None
    linked_entities: list[str] = None
    cidoc_classes: list[str] = None
    view_classes: list[str] = None
    system_classes: list[str] = None
    type_id: list[int] = None
    show: list[str] = None
    download: bool = None
    count: bool = None
    locale: str = None
    sort: str = None
    column: str = None
    limit: int = None
    first: int = None
    last: int = None
    page: int = None
    export: str = None
    format: str = None
    relation_type: int = None
    centroid: bool = None
    geometry: list[str] = None
    image_size: str = None
    file_id: int = None
