from dataclasses import dataclass
from typing import Optional

from flask import g

from histarchexplorer.database.about import get_projects


@dataclass
class Project:
    id_: int
    name: str
    description: Optional[str]
    website: Optional[str]
    legal_notice: Optional[str]
    imprint: Optional[str]
    main_project: bool

    @classmethod
    def get_all_localized(cls) -> list['Project']:
        results = get_projects()
        projects = []

        for entry in results:
            projects.append(Project(
                id_=entry.id,
                name=cls._localize(entry.name, g.language),
                description=cls._localize(entry.description, g.language),
                website=entry.website,
                legal_notice=cls._localize(entry.legal_notice, g.language),
                imprint=cls._localize(entry.imprint, g.language),
                main_project=(entry.class_name == 'main-project')))

        return projects

    @staticmethod
    def _localize(data: dict | None, preferred_lang: str) -> Optional[str]:
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
