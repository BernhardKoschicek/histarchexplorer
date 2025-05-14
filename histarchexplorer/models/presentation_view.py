import json
from dataclasses import asdict, dataclass, field
from typing import Any, List, Optional

import requests

from histarchexplorer import app
from histarchexplorer.api.api_access import PROXIES


@dataclass
class GeometryModel:
    id: int
    type: str
    coordinates: Any


@dataclass
class TimePointModel:
    earliest: Optional[str] = None
    latest: Optional[str] = None
    comment: Optional[str] = None


@dataclass
class TimeRangeModel:
    start: Optional[TimePointModel] = None
    end: Optional[TimePointModel] = None


@dataclass
class TypeHierarchyEntry:
    label: str
    descriptions: Optional[str]
    identifier: str


@dataclass
class EntityTypeModel:
    id: int
    title: str
    descriptions: Optional[str]
    is_standard: Optional[bool]
    type_hierarchy: Optional[List[TypeHierarchyEntry]]
    value: Optional[str]
    unit: Optional[str]


@dataclass
class ExternalReferenceModel:
    id: int
    type: str
    identifier: str
    reference_system: str
    resolver_url: Optional[str]
    reference_url: Optional[str]

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            type=data.get("type"),
            identifier=data.get("identifier"),
            reference_system=data.get("referenceSystem"),
            resolver_url=data.get("resolverURL"),
            reference_url=data.get("referenceURL"))

@dataclass
class Reference:
    id: int
    title: str
    system_class: str
    type: Optional[str] = None
    type_id: Optional[int] = None
    citation: Optional[str] = None
    pages: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data.get("title"),
            system_class=data.get("systemClass"),
            type=data.get("type"),
            type_id=data.get("typeId"),
            citation=data.get("citation"),
            pages=data.get("pages"))


@dataclass
class File:
    id: int
    title: str
    license: Optional[str] = None
    creator: Optional[str] = None
    license_holder: Optional[str] = None
    public: bool = False
    url: Optional[str] = None
    mime_type: Optional[str] = None
    iiif_manifest: Optional[str] = None
    iiif_base_path: Optional[str] = None


@dataclass
class Relation:
    id: int
    name: str
    system_class: str
    relation_types: Optional[list[dict[str, Any]]] = None
    description: Optional[str] = None
    aliases: Optional[list[str]] = None
    time_range: Optional[TimeRangeModel] = None
    geometries: List[GeometryModel] = field(default_factory=list)
    types: List[EntityTypeModel] = field(default_factory=list)


@dataclass
class PresentationView:
    id: int
    systemClass: str
    title: str
    description: str
    aliases: List[str]
    geometries: List[GeometryModel] = field(default_factory=list)
    when: Optional[TimeRangeModel] = None
    types: List[EntityTypeModel] = field(default_factory=list)
    externalReferenceSystems: List[ExternalReferenceModel] = field(
        default_factory=list)
    references: List[Reference] = field(default_factory=list)
    files: List[File] = field(default_factory=list)
    relations: dict[str, List[Relation]] = field(default_factory=dict)


    def to_json(self, *, indent: Optional[int] = 2) -> str:
        return json.dumps(asdict(self), indent=indent, ensure_ascii=False)

    @staticmethod
    def parse_geometries(
            geometry_data: Any,
            relation_id: int = 0) -> List[GeometryModel]:
        geometries = []
        if isinstance(geometry_data, dict):
            geometries.append(GeometryModel(
                id=relation_id,
                type=geometry_data["type"],
                coordinates=geometry_data["geometry"]["coordinates"]))
        elif isinstance(geometry_data, list):
            for g in geometry_data:
                if isinstance(g, dict):
                    geometries.append(GeometryModel(**g))
        return geometries

    @staticmethod
    def parse_time_range(when: dict) -> Optional[TimeRangeModel]:
        if not when:
            return None
        return TimeRangeModel(
            start=TimePointModel(**when.get("start", {}))
            if when.get("start") else None,
            end=TimePointModel(**when.get("end", {}))
            if when.get("end") else None)

    @staticmethod
    def parse_types(types_data: List[dict]) -> List[EntityTypeModel]:
        types = []
        for type_ in types_data:
            hierarchy = []
            if type_.get("typeHierarchy"):
                hierarchy = [
                    TypeHierarchyEntry(**th)
                    for th in type_.get("typeHierarchy", [])]
            types.append(EntityTypeModel(
                id=type_["id"],
                title=type_.get("title", ""),
                descriptions=type_.get("descriptions"),
                is_standard=type_.get("isStandard"),
                type_hierarchy=hierarchy,
                value=type_.get("value"),
                unit=type_.get("unit")))
        return types

    @staticmethod
    def parse_relations(raw_relations: dict) -> dict[str, List[Relation]]:
        grouped_relations: dict[str, List[Relation]] = {}
        for system_class, relation_list in raw_relations.items():
            relations = []
            for rel in relation_list:
                if not isinstance(rel, dict):
                    continue

                rel_geometries = PresentationView.parse_geometries(
                    rel.get("geometries"), rel.get("id", 0))
                time_range = PresentationView.parse_time_range(rel.get("when"))
                rel_types = []

                standard_type = rel.get("standardType")
                if isinstance(standard_type, dict):
                    rel_types.append(EntityTypeModel(
                        id=standard_type.get("id", 0),
                        title=standard_type.get("title", ""),
                        descriptions=None,
                        is_standard=True,
                        type_hierarchy=[],
                        value=None,
                        unit=None))

                relation = Relation(
                    id=rel["id"],
                    name=rel.get("title"),
                    system_class=rel.get("systemClass", system_class),
                    relation_types=rel.get("relationTypes"),
                    description=rel.get("description"),
                    aliases=rel.get("aliases", []),
                    time_range=time_range,
                    geometries=rel_geometries,
                    types=rel_types)

                relations.append(relation)

            if relations:
                grouped_relations[system_class] = relations

        return grouped_relations

    @staticmethod
    def parse_file(raw_file: dict) -> List[File]:
        files = []
        for f in raw_file:
            if isinstance(f, dict):
                files.append(File(
                    id=f["id"],
                    title=f["title"],
                    license=f.get("license"),
                    creator=f.get("creator"),
                    license_holder=f.get("licenseHolder"),
                    public=f["publicShareable"],
                    url=f.get("url"),
                    mime_type=f.get("mimetype"),
                    iiif_manifest=f.get("iiifManifest"),
                    iiif_base_path=f.get("iiifBasePath")))
        return files

    @classmethod
    def from_api(cls, entity_id: int) -> 'PresentationView':
        url = f"{app.config['API_URL']}entity_presentation_view/{entity_id}"
        response = requests.get(
            url,
            proxies=PROXIES,
            timeout=30)
        response.raise_for_status()
        data = response.json()

        return cls(
            id=data["id"],
            systemClass=data.get("systemClass", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            aliases=data.get("aliases", []),
            geometries=cls.parse_geometries(data.get("geometries", [])),
            when=cls.parse_time_range(data.get("when")),
            types=cls.parse_types(data.get("types", [])),
            externalReferenceSystems=[
                ExternalReferenceModel.from_dict(er)
                for er in data.get("externalReferenceSystems", [])
                if isinstance(er, dict)],
            references=[
                Reference.from_dict(ref)
                for ref in data.get("references", [])
                if isinstance(ref, dict)],
            files=cls.parse_file(data.get('files', [])),
            relations=cls.parse_relations(data.get("relations", {})))
