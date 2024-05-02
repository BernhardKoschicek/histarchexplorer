import numpy
from flask import render_template

from histarchexplorer import app
from histarchexplorer.api.api_access import ApiAccess
from histarchexplorer.api.parser import Parser
from histarchexplorer.models.entity import Entity
from histarchexplorer.models.util import get_types_sorted


@app.route('/test')
def test() -> str:
    return render_template('test/test.html')


@app.route('/test/entity/<int:id_>')
def test_entity(id_: int) -> str:
    parser = Parser()
    entity = Entity.get_entity(id_, parser)
    return render_template('test/entity.html', entity=entity)


@app.route('/test/subunit/<int:id_>')
def test_subunit(id_: int) -> str:
    parser = Parser()
    entity = ApiAccess.get_subunits(id_, parser)
    return render_template('test/entity.html', entity=entity)


@app.route('/test/view/entity/<int:id_>')
def test_entity_view(id_: int) -> str:
    parser = Parser()
    entity = Entity.get_entity(id_, parser)
    return render_template(
        'test/entity_view.html',
        entity=entity,
        type_hierarchy=get_types_sorted(entity.types)
        if entity.types else None,
        images=numpy.array_split(entity.depictions, 4)
        if entity.depictions else None)


@app.route('/test/system_class/<class_>')
def test_system_class(class_: str) -> str:
    parser = Parser(limit=0, show=['none'],  sort='desc')
    return render_template(
        'test/system_class.html',
        entities=Entity.get_by_system_class(class_, parser))
