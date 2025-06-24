from histarchexplorer.database.config_classes import get_config_classes_sql


def get_config_classes() -> dict[str, int]:
    data = {}
    for config_class in get_config_classes_sql():
        data[config_class.name] = config_class.id
    return data
