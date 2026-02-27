import json
from pydantic import BaseModel

from histarchexplorer.database.settings import (
    create_settings_table, get_settings, save_settings)


class Settings(BaseModel):
    index_img: str = \
        '/static/images/index_map_bg/Blank_map_of_Europe_central_network.png'
    index_map: int = 1
    img_map: str = 'map'
    preferred_language: str = 'en'
    greyscale: bool = False
    darkmode: bool = False
    language_selector: bool = False
    access_restriction: bool = False
    shown_classes: list[str] = [
        'place', 'feature', 'stratigraphic_unit',
        'artifact', 'human_remains', 'person', 'group',
        'acquisition', 'event', 'activity', 'creation',
        'move', 'production', 'modification']
    shown_types: list[str] = []
    hidden_classes: list[str] = ['group']
    hidden_types: list[str] = []
    shown_ids: list[int] = []
    hidden_ids: list[int] = []
    case_study_type_id: int = 8240
    nav_logo: str = 'thanados_light.svg'
    footer_logos: list[int] = []
    legal_notice: dict[str, str] = {}
    menu_management: dict = {
        'start_page': {'show': True, 'page_type': 'default'},
        'legal_notice': {'show': True, 'page_type': 'default'},
        'about': {'show': True, 'page_type': 'default'},
        'publications': {'show': True, 'page_type': 'default'},
        'outcome': {'show': True, 'page_type': 'default'},
        'search': {'show': True, 'page_type': 'default'},
        'footer': {'show': True, 'page_type': 'default'},
        }

    @classmethod
    def load_from_db(cls) -> 'Settings':
        create_settings_table()

        default_settings = cls().model_dump()
        db_settings_raw = {row.key: row.value for row in get_settings()}

        default_menu = default_settings.get('menu_management', {})
        db_menu_raw = db_settings_raw.get('menu_management')
        db_menu = {}
        if isinstance(db_menu_raw, str):
            try:
                loaded_json = json.loads(db_menu_raw)
                if isinstance(loaded_json, dict):
                    db_menu = loaded_json
            except json.JSONDecodeError:
                pass
        elif isinstance(db_menu_raw, dict):
            db_menu = db_menu_raw

        merged_menu = {**default_menu, **db_menu}

        merged_settings_data = {**default_settings, **db_settings_raw}
        merged_settings_data['menu_management'] = merged_menu

        instance = cls(**merged_settings_data)
        instance.save_to_db()

        return instance

    def save_to_db(self):
        for key, value in self.model_dump().items():
            save_settings(key, value)

    def get_map_settings(self) -> dict:
        return {
            'img': self.index_img,
            'map': self.index_map,
            'img_map': self.img_map,
            'greyscale': self.greyscale}
