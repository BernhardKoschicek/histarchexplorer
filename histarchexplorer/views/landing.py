from collections import defaultdict

from flask import render_template, g

from histarchexplorer import app
from histarchexplorer.api.parser import Parser
from histarchexplorer.models.entity import Entity


@app.route('/entity/<id_>')
def landing(id_: int) -> str:
    parser = Parser()
    entity = Entity.get_entity(id_, parser)
    subunits_dict = defaultdict(list)
    if entity.system_class.lower() in [
            "artifact",
            "feature",
            "human_remains",
            "place",
            "stratigraphic_unit"]:
        subunit_parser = Parser(
            properties=['P46'],
            limit=0,
            format='lpx',
            show=['types'])
        subunits = Entity.get_linked_entities_by_properties_recursive(entity.id, subunit_parser)

        for subunit in subunits:
            for type_ in subunit.types:
                subunits_dict[type_.type_hierarchy[0]['label']].append(subunit)



    # print("Types:", entity.types)
    # print("Begin:", entity.begin)
    # print("End:", entity.end)
    # print("Relations:", entity.relations)
    # print("Relation Class:", entity.relation_class)

    if entity.depictions is None:
        entity.depictions = []
    return render_template(
        'landing.html',
        entity=entity,
        relations=entity.relations,
        subunits=subunits_dict or None)
