from typing import Any, Optional

from histarchexplorer.model.types import Types


def uc_first(string: str) -> str:
    return str(string)[0].upper() + str(string)[1:] if string else ''


def split_date_string(data: Optional[str]) -> Optional[str]:
    return '.'.join(map(str, data.split('T')[0].split('-')[::-1])) \
        if data else ''


def format_date(
        date_from: Optional[str],
        date_to: Optional[str]) -> Optional[str]:
    return f'between {date_from} and {date_to}' if date_to else date_from


def flatten_list_and_remove_duplicates(list_: list[Any]) -> list[Any]:
    return [item for sublist in list_ for item in sublist if item not in list_]


def get_types_sorted(types: list[Types]) -> Optional[dict[str, Any]]:
    if not types:
        return None
    type_hierarchy: dict[str, Any] = {}
    for type_ in types:
        type_hierarchy.setdefault(type_.root, []).append(type_)
    return type_hierarchy
