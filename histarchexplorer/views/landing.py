from collections import defaultdict

from flask import render_template

from histarchexplorer import app
from histarchexplorer.api.parser import Parser
from histarchexplorer.models.entity import Entity


@app.route('/entity/<int:id_>')
def landing(id_: int) -> str:
    parser = Parser(
        properties=['P46', 'P67'],
        limit=0,
        format='lpx')

    entities = Entity.get_linked_entities_by_properties_recursive(
        id_,
        parser)
#remove types, adminitrative units, appelations etc.


    main_entity = None
    for entity in entities:
        if entity.id == id_:
            main_entity = entity


    for relation in main_entity.relations.values():
        for rel in relation:
            for relation_entity in entities:
                if int(relation_entity.id) == int(rel.relation_to_id):
                    rel.related_entity = relation_entity

    subunits_dict = defaultdict(list)
    related_entities = {
        'Place' : defaultdict(list),
        'Feature': defaultdict(list),
        'Stratigraphic unit': defaultdict(list),
        'Human remains': defaultdict(list),
        'Artifact': defaultdict(list)
    }

    super_entity = None
    if main_entity.system_class.lower() in [
        "artifact",
        "feature",
        "human remains",
        "place",
        "stratigraphic unit"]:

        for subunit in entities:
            if not subunit.types:
                continue #macht mit nächster entity weiter; check also break
            for type_ in subunit.types:
                subunits_dict[type_.type_hierarchy[0]['label']].append(subunit)

                match label := type_.type_hierarchy[0]['label']:
                    case 'Feature':
                        related_entities[label][type_.label].append(subunit)
                    case 'Stratigraphic unit':
                        related_entities[label][type_.label].append(subunit)
                    case 'Artifact':
                        related_entities[label][type_.label].append(subunit)
                    case 'Human remains':
                        related_entities[label][type_.label].append(subunit)
                    case 'Place':
                        related_entities[label][type_.label].append(subunit)

                        #check if entity = super_entity
                        if subunit.id != main_entity.id:
                            super_entity = subunit

        # print(subunits_dict['Feature'])

    # print(entity.view_class)
    # print("Types:", entity.types)
    # print("Begin:", entity.begin)
    # print("End:", entity.end)
    # print("Relations:", entity.relations)
    # print("Relation Class:", entity.relation_class)
    #print(main_entity.geometry)
    print(type(super_entity))
    print(main_entity.system_class)
    #print(subunit)

    main_image= None
    images=[]

    for image in main_entity.depictions:
        if image.main_image:
            main_image =image
            continue
        images.append(image)
    if not main_image and images:
        main_image = images[0]
        del images[0]

    if not main_entity.geometry and super_entity and super_entity.geometry:
        main_entity.geometry = super_entity.geometry

    # Description 2/3 column or 1/3 column
    if main_entity.description and len(main_entity.description) > 500:
        main_entity.description_class = "item-middle"
    else:
        main_entity.description_class = "item"

    case_study = []
    for type_ in main_entity.types:
        if type_.root == "Case Study":
            case_study.append(type_)
    if not case_study:
        for type_ in super_entity.types:
            if type_.root == "Case Study":
                case_study.append(type_)

    return render_template(
        'landing.html',
        entity=main_entity,
        view_class=main_entity.view_class,
        system_class=main_entity.system_class,
        relations=main_entity.relations,
        subunits=subunits_dict or {},
        related_entities=related_entities,
        main_image=main_image,
        images=images,
        super_entity=super_entity,
        case_study=case_study
    )
