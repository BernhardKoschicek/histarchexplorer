from flask import g


def get_map_data():
    g.cursor.execute(
        'SELECT index_img, index_map, img_map, greyscale '
        'FROM tng.settings '
        'LIMIT 1')
    return g.cursor.fetchone()

def get_shown_entities():
    g.cursor.execute(
        'SELECT shown_entities '
        'FROM tng.settings '
        'LIMIT 1')
    return g.cursor.fetchone().shown_entities