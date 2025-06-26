from histarchexplorer.database.config_classes import get_config_classes_sql


def get_config_classes() -> dict[str, int]:
    data = {}
    for config_type in get_config_classes_sql():
        data[config_type.name] = config_type.id
    return data

