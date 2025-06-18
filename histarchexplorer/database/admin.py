import json
from typing import Any

from flask import g

from histarchexplorer.database.config import check_if_config_entry_exist


def get_config_properties() -> Any:
    g.cursor.execute(
        '''
        SELECT id, name, domain, range, 'direct' AS direction
        FROM tng.config_properties
        UNION ALL
        SELECT id, name_inv, range, domain, 'inverse' AS direction
        FROM tng.config_properties''')
    return g.cursor.fetchall()


def set_hidden_entities(entities: list[str]) -> None:
    g.cursor.execute(
        'UPDATE tng.settings SET hidden_entities = %s',
        (entities,))


def set_shown_entities(entities: list[str]) -> None:
    g.cursor.execute(
        'UPDATE tng.settings SET shown_entities = %s',
        (entities,))


def set_index_background(settings: dict[str, str]) -> None:
    g.cursor.execute(
        """
        UPDATE tng.settings
        SET (index_map, index_img, img_map, greyscale) = (%s, %s, %s, %s)""", (
            settings['index_map'],
            settings['index_img'],
            settings['img_map'],
            settings['greyscale']))


def add_new_map(data: dict[str, str]) -> int:
    g.cursor.execute(
        '''
        INSERT INTO tng.maps
            (name, display_name, sortorder, tilestring)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        ''', (
            data['name'],
            data['display_name'],
            data['sort_order'],
            data['tile_string']))
    return g.cursor.fetchone()[0]


def delete_map(map_id: int) -> None:
    g.cursor.execute(
        'DELETE FROM tng.maps WHERE id = %(map_id)s',
        {'map_id': map_id})


def update_map(data: dict[str, str]) -> None:
    g.cursor.execute(
        """
        UPDATE tng.maps
        SET name         = NULLIF(%(name)s, ''),
            display_name = NULLIF(%(display_name)s, ''),
            sortorder    = CASE
                               WHEN %(sortorder)s = '' THEN NULL
                               ELSE CAST(%(sortorder)s AS integer)
                END,
            tilestring   = NULLIF(%(tilestring)s, '')
        WHERE id = %(map_id)s
        """,
        data)


def update_config_entry(data: dict, language: str) -> None:
    cur = g.cursor
    config_id = data['config_id']

    if check_if_config_entry_exist(config_id) is None:
        raise 404

    cur.execute("""
                UPDATE tng.config
                SET email    = NULLIF(%(email)s, ''),
                    website  = NULLIF(%(website)s, ''),
                    orcid_id = NULLIF(%(orcid_id)s, ''),
                    image    = NULLIF(%(image)s, '')
                WHERE id = %(config_id)s
                """, data)

    for col in ['address', 'description', 'imprint', 'legal_notice', 'name']:
        val = data.get(col, '')
        if val:
            cur.execute(
                f"""
                UPDATE tng.config
                   SET {col} = jsonb_set(
                        COALESCE({col}, '{{}}'),
                        %s,
                        %s::jsonb,
                        true)
                 WHERE id = %s
                """,
                ([language], json.dumps(val), config_id))
        else:
            cur.execute(
                f"""
                UPDATE tng.config
                   SET {col} = COALESCE({col}, '{{}}') - %s
                 WHERE id = %s
                """,
                (language, config_id))
