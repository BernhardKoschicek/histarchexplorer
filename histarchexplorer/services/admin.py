from histarchexplorer.database.admin import (
    add_new_map, delete_map,  set_hidden_entities,
    set_index_background,
    set_shown_entities, update_config_entry, update_map)

class EntryNotFound(Exception):
    pass

class Admin:

    @staticmethod
    def set_hidden_entities(form: list[str]) -> None:
        return set_hidden_entities(form)

    @staticmethod
    def set_shown_entities(form: list[str]) -> None:
        return set_shown_entities(form)

    @staticmethod
    def set_index_background(settings: dict[str, str]) -> None:
        return set_index_background(settings)

    @staticmethod
    def add_new_map(data: dict[str, str]) -> int:
        return add_new_map(data)

    @staticmethod
    def delete_map(map_id:int) -> None:
        return delete_map(map_id)

    @staticmethod
    def update_map(data: dict[str, str]) -> None:
        return update_map(data)

    @staticmethod
    def edit_entry(data: dict, language: str) -> None:
        update_config_entry(data, language)
