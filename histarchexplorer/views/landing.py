from flask import render_template, g

from histarchexplorer import app
from histarchexplorer.api.parser import Parser
from histarchexplorer.models.entity import Entity


@app.route('/entity/<id_>')
def landing(id_: int) -> str:
    parser = Parser()
    entity = Entity.get_entity(id_, parser)
    print(entity.types)
    print(entity.begin)
    print(entity.end)
    print(entity.relations)
    print(entity.relation_class)

    return render_template('landing.html', entity=entity, relations=entity.relations)