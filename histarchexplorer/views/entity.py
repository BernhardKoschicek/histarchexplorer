import json

from histarchexplorer import app
from flask import render_template, abort

from histarchexplorer.api.parser import Parser
from histarchexplorer.models.entity import Entity
from histarchexplorer.utils.helpers import to_serializable

sidebarelements = app.config['SIDEBAR_OPTIONS']
valid_routes = {item['route'] for item in sidebarelements}


@app.route('/entity/<int:id_>/')
@app.route('/entity/<int:id_>/<tab_name>')
def entity(id_: int, tab_name="overview") -> str:
    if tab_name not in valid_routes:
        abort(404)

    entity = Entity.get_entity(id_, Parser())

    entity_data = {'entity': json.dumps(entity.to_serializable(), ensure_ascii=False, indent=4)}

    return render_template('entity.html', sidebarelements=sidebarelements, page_name="landing", active_tab=tab_name,
                           entity_data=entity_data)


@app.route('/getentity/<int:id_>/<tab_name>')
def getentity(id_: int, tab_name=None, json_serializable=None) -> str:
    mapdata = {}

    def get_general_data():
        # here we get data that needs to be loaded anyway
        general_data = {}
        return general_data

    def get_map_data():

        entties = Entity.get_linked_entities_by_properties_recursive(
            id_, Parser(show='geometry', properties='P46'))
        features = {'type': 'FeatureCollection', 'features': []}
        for ent in entties:
            if ent.system_class == 'Feature':
                features['features'].append(
                    {'type': 'Feature', 'geometry': ent.geometry, 'properties': {'id': ent.id, 'label': ent.name}})
        return features

    def get_file_data():
        file_data = {}
        return file_data

    if tab_name == 'map':
        mapdata['features'] = get_map_data()
        print(mapdata)

    if tab_name not in valid_routes:
        print('notvalid')
        abort(404)

    return render_template(f'tabs/{tab_name}.html', mapData=json.dumps(mapdata))
