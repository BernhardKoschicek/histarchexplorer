import json
from flask import render_template, g
from histarchexplorer import app
from histarchexplorer.database.about import *
from histarchexplorer.utils import helpers






@app.route('/about')
def about() -> str:

    def build_object(id_: int) -> None:
        g.cursor.execute('SELECT * FROM tng.config WHERE id = %s', (id_,))
    def build_object(id):

        g.cursor.execute('SELECT * FROM tng.config WHERE id = %s', (id,))
        object_data = g.cursor.fetchone()
        if not object_data:
            return {}

        object = {}
        column_names = [description[0] for description in g.cursor.description]
        for column_name, column_value in zip(column_names, object_data):
            if column_value:
                object[column_name] = column_value

        # Integrate connections
        object['connections'] = build_connections(object['id'])['properties']
        return object

    def build_connections(id):
        g.cursor.execute(build_connections_sql, (id,))
        rows = g.cursor.fetchall()

        result = {'properties': []}
        property_map = {}

        for row in rows:
            property_id = row[1]
            if property_id not in property_map:
                property_obj = {'id': property_id, 'name': row[0], 'targets': []}
                property_map[property_id] = property_obj
                result['properties'].append(property_obj)

        for row in rows:
            property_id = row[1]
            target_id = row[5]
            target_obj = build_object(target_id)
            if target_obj and target_obj not in property_map[property_id]['targets']:
                property_map[property_id]['targets'].append(target_obj)

            role = row[3]
            if role and 'roles' not in target_obj:
                target_obj['roles'] = []
            if role and role not in target_obj['roles']:
                target_obj['roles'].append(role)

        return result

    # Example usage
    print(json.dumps(build_object(1), ensure_ascii=False, indent=4))

    g.cursor.execute('SELECT name, description, legal_notice, imprint FROM tng.config WHERE id = 1')
    project_result = g.cursor.fetchone()

    project = {
        'name': (helpers.get_translation(project_result[0]))['label'],
        'description': (helpers.get_translation(project_result[1]))['label'],
        'legal_notice': (helpers.get_translation(project_result[2]))['label'],
        'imprint': (helpers.get_translation(project_result[3]))['label']
    }


    institutions_result = get_institutions()


    institutions = []
    for row in institutions_result:
        institutions.append({
            'name': (helpers.get_translation(row[0]))['label'],
            'address': (helpers.get_translation(row[1]))['label'] if row[1] else " ",
            'website': row[2],
            'role': (helpers.get_translation(row[4]))['label'] if row[4] else "No role",
            'image': row[3]
        })



    persons_result = get_persons()


    persons = {}
    for row in persons_result:
        person_name = (helpers.get_translation(row[0]))['label']

        if person_name not in persons:
            persons[person_name] = {
                'name': (helpers.get_translation(row[0]))['label'],
                'roles': [] ,
                'image': row[1],
                'affiliation': (helpers.get_translation(row[3]))['label'],
                'website': row[4],
                'email': row[5]
            }
        persons[person_name]['roles'].append((helpers.get_translation(row[2]))['label'])

    persons_list = list(persons.values())

    return render_template(
        'about.html',
        project=project,
        institutions=institutions,
        persons=persons_list)
