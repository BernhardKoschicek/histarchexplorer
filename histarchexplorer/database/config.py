import json
from typing import Any

from flask import g


def update_jsonb_column(
        column_name: str,
        value: str,
        config_id: str) -> None:
    language = g.language
    if value:
        value_to_be_inserted_json = json.dumps(value)
        update_query = f"""
            UPDATE tng.config
            SET {column_name} = jsonb_set(COALESCE({column_name}, '{{}}'), 
            '{{{language}}}', '{value_to_be_inserted_json}', true)
            WHERE id = {int(config_id)}
        """
    else:
        update_query = f"""
            UPDATE tng.config
            SET {column_name} = COALESCE({column_name}, '{{}}') - '{language}'
            WHERE id = {int(config_id)}
        """
    g.cursor.execute(update_query)


def get_config_data(language: str) -> Any:
    g.cursor.execute(
        f"SELECT * FROM tng.config ORDER BY (name->>'{language}')")
    return g.cursor.fetchall()


def check_if_config_entry_exist(id_: int) -> bool:
    g.cursor.execute(
        'SELECT 1 FROM tng.config WHERE id = %(id)s',
        {'id': id_})
    return g.cursor.fetchone() is not None
