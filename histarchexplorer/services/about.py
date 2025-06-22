from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from flask import g
from flask_babel import lazy_gettext as _

from histarchexplorer.database.about import (
    get_affiliations, get_config_entities, get_project_roles_sql)


@dataclass()
class ConfigEntities:
    id_: int
    name: str
    description: str
    website: str
    legal_notice: str
    imprint: str
    config_class: int
    address: str
    email: str
    image: str
    orcid_id: str
    class_name: str
    roles: dict[int, list[str]] | None
    main_project: bool
    affiliations: list[dict[str, Any]] | None

    @classmethod
    def get_all_localized(cls) -> list['ConfigEntities']:
        entities = []

        for entry in get_config_entities():
            entities.append(ConfigEntities(
                id_=entry.id,
                name=localize(entry.name),
                description=localize(entry.description),
                website=entry.website,
                legal_notice=localize(entry.legal_notice),
                imprint=localize(entry.imprint),
                config_class=entry.config_class,
                address=localize(entry.address),
                email=entry.email,
                image=entry.image,
                orcid_id=entry.orcid_id,
                class_name=entry.class_name,
                main_project=(entry.class_name == 'main-project'),
                roles=get_project_roles(
                    entry.id,
                    entry.config_class),
                affiliations=get_person_affiliations(entry.id)
                if entry.class_name == 'person' else None
            ))

        return entities
    @classmethod
    def group_by_class_name(
            cls,
            entities: list['ConfigEntities']) \
            -> dict[str, list['ConfigEntities']]:
        grouped = {}
        for entity in entities:
            grouped.setdefault(entity.class_name, []).append(entity)
        return grouped


def get_project_roles(
        id_: int,
        config_class_id: int) -> dict[int, list]:
    result = defaultdict(list)
    for domain_id, role in get_project_roles_sql(id_, config_class_id):
        if role:
            result[domain_id].append(localize(role))
        else:
            result[domain_id].append(_('no role'))
    return dict(result)


def get_person_affiliations(id_: int) -> list[dict[str, Any]]:
    grouped = defaultdict(lambda: {"roles": []})
    for record in get_affiliations(id_):
        rid = record.range_id
        if "id" not in grouped[rid]:
            grouped[rid]["institute_id"] = rid
            grouped[rid]["affiliation"] = localize(record.affiliation)
        grouped[rid]["roles"].append(localize(record.role))
    return list(grouped.values())


def localize(data: dict[str, str] | None) -> str | None:
    preferred_lang = g.language
    if not isinstance(data, dict):
        return data

    # Try preferred language
    if preferred_lang in data and data[preferred_lang]:
        return data[preferred_lang]

    # Fallback to English
    if 'en' in data and data['en']:
        return data['en']

    # Fallback to any filled value
    for value in data.values():
        if value:
            return value

    return None
