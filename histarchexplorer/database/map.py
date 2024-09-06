from flask import g


def get_map_server(data):
    g.cursor.execute(
        f'SELECT tilestring '
        f'FROM tng.maps '
        f'WHERE id={data.index_map}')
    return g.cursor.fetchone()