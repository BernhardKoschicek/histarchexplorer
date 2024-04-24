from typing import Optional

from flask import redirect, render_template, request, session
from werkzeug import Response

from histarchexplorer import app
from histarchexplorer.api.parser import Parser
from histarchexplorer.model.entity import Entity


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/entities')
def entities() -> str:
    return render_template('entities.html')


@app.route('/search')
def search() -> str:
    return render_template('search.html')


@app.route('/about')
def about() -> str:
    return render_template('about.html')


@app.route('/test')
def test() -> str:
    return render_template('test/test.html')


@app.route('/test/entity/<int:id_>')
def test_entity(id_: int) -> str:
    parser = Parser()
    entity = Entity.get_entity(id_, parser)
    return render_template('test/entity.html', entity=entity)


@app.route('/test/system_class/<class_>')
def test_system_class(class_: str) -> str:
    parser = Parser(limit=500, show=['none'], sort='desc')
    return render_template(
        'test/system_class.html',
        entities=Entity.get_by_system_class(class_, parser))


@app.route('/language=<language>')
def set_language(language: Optional[str] = None) -> Response:
    session['language'] = language
    return redirect(request.referrer)
