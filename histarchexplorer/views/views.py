from typing import Optional

from flask import redirect, render_template, request, session
from werkzeug import Response
from flask import Response, redirect, render_template, request, session, g

from histarchexplorer import app


@app.route('/')
def index():
    g.cursor.execute('SELECT index_img, index_map, img_map, greyscale FROM tng.settings LIMIT 1')
    data = g.cursor.fetchone()

    g.cursor.execute(f'SELECT tilestring FROM tng.maps WHERE id={data.index_map}')
    map = g.cursor.fetchone()

    return render_template('index.html', map=map.tilestring, img=data.index_img, img_map=data.img_map, greyscale=data.greyscale)

@app.route('/entities')
def entities() -> str:
    g.cursor.execute('''
        SELECT openatlas_class_name, COUNT(*) as count
        FROM tng.entity
        GROUP BY openatlas_class_name
        ORDER BY count DESC
    ''')

    entities = g.cursor.fetchall()
    # list of tuples to dictionary (entities_dict); keys = entities; values = associated IDs.
    entities_dict = {entity[0]: entity[1] for entity in entities}

    return render_template('entities.html', entities=entities_dict)


@app.route('/search')
def search() -> str:
    return render_template('search.html')


@app.route('/language=<language>')
def set_language(language: Optional[str] = None) -> Response:
    session['language'] = language
    return redirect(request.referrer)
