from typing import Any

from flask import g


def get_shown_entities() -> Any:
    g.cursor.execute(
        'SELECT shown_entities '
        'FROM tng.settings '
        'LIMIT 1')
    result = g.cursor.fetchone()
    return result[0] or []


def get_hidden_entities() -> Any:
    g.cursor.execute(
        'SELECT hidden_entities '
        'FROM tng.settings '
        'LIMIT 1')
    result = g.cursor.fetchone()
    return result[0] or []

def get_main_image_table() -> dict[int, int]:
    main_image = {}
    g.cursor.execute(
        'SELECT '
        '   entity_id,'
        '   image_id '
        'FROM web.entity_profile_image')
    for row in g.cursor.fetchall():
        main_image[row[0]] = row[1]
    return main_image


def get_settings():
    g.cursor.execute("SELECT * FROM tng.settings LIMIT 1")
    return g.cursor.fetchone()
