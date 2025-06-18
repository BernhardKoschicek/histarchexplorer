import json
import os
from typing import Optional

from flask import (
    abort, current_app, flash, g, redirect, render_template,
    request, session, url_for)
from flask_babel import lazy_gettext as _
from flask_login import current_user, login_required
from werkzeug import Response

from histarchexplorer import app
from histarchexplorer.api.helpers import get_entities_count_by_case_study
from histarchexplorer.database.config import (
    check_if_config_entry_exist, get_config_data, update_jsonb_column)
from histarchexplorer.database.admin import get_config_properties
from histarchexplorer.database.map import (check_if_map_id_exist,
                                           get_base_map, \
                                           get_base_map_by_id)
from histarchexplorer.database.settings import (
    get_hidden_entities, get_map_settings, get_shown_entities)
from histarchexplorer.services.admin import Admin, EntryNotFound, \
    set_hidden_entities
from histarchexplorer.utils import helpers


@app.route('/admin/')
@app.route('/admin/<tab>')
@app.route('/admin/<tab>/<entry>')
@login_required
def admin(tab: Optional[str] = None, entry: Optional[str] = None) -> str:
    check_manager_user()

    # todo: this will be obsolete if we change to dict instead to named tuples
    language = session.get(
        'language',
        request.accept_languages.best_match(app.config['LANGUAGES'].keys()))

    entities = []
    for item in get_config_data(language):
        entity = {'id': item.id, 'config_class': item.config_class,
                  'website': item.website, 'email': item.email,
                  'orcid_id': item.orcid_id, 'image': item.image}

        for column in ['name', 'description', 'imprint', 'address',
                       'legal_notice']:
            entity[column] = {}
            if getattr(item, column):
                for key, value in getattr(item, column).items():
                    entity[column][key] = value
                entity[column]['display'] = helpers.get_translation(
                    entity[column])

        entities.append(entity)

    # todo: this will be obsolete if we change to dict instead to named tuples
    config_properties = get_config_properties()
    colnames = [desc[0] for desc in g.cursor.description]
    config_list = [dict(zip(colnames, row)) for row in config_properties]

    for row in config_list:
        row['name'] = helpers.get_translation(row['name'])

    tabs = [
        {
            'label': _('main-project'),
            'target': 'nav-main-project',
            'id': g.config_classes['main-project']
        }, {
            'label': _('projects'),
            'target': 'nav-projects',
            'id': g.config_classes['project']
        }, {
            'label': _('persons'),
            'target': 'nav-persons',
            'id': g.config_classes['person']
        }, {
            'label': _('institutions'),
            'target': 'nav-institutions',
            'id': g.config_classes['institution']
        }, {
            'label': _('attributes'),
            'target': 'nav-attributes',
            'id': g.config_classes['role']}]

    g.cursor.execute("""
                     SELECT l.id        AS link_id,
                            l.sortorder AS sortorder,
                            s.id        AS start_id,
                            s.name      AS start_name,
                            cp.name     AS config_property,
                            cp.id       AS property_id,
                            'direct'    AS direction,
                            e.name      AS end_name,
                            e.id        AS end_id,
                            r.name      AS role,
                            r.id        AS role_id
                     FROM tng.links l
                              JOIN tng.config s ON l.domain_id = s.id
                              JOIN tng.config e ON l.range_id = e.id
                              JOIN tng.config_properties cp ON l.property =
                                                               cp.id
                              LEFT JOIN tng.config r ON l.attribute = r.id
                     UNION ALL
                     SELECT l.id        AS link_id,
                            l.sortorder AS sortorder,
                            s.id        AS start_id,
                            s.name      AS start_name,
                            cp.name_inv AS config_property,
                            cp.id       AS property_id,
                            'inverse'   AS direction,
                            e.name      AS end_name,
                            e.id        AS end_id,
                            r.name      AS role,
                            r.id        AS role_id
                     FROM tng.links l
                              JOIN tng.config s ON l.range_id = s.id
                              JOIN tng.config e ON l.domain_id = e.id
                              JOIN tng.config_properties cp ON l.property =
                                                               cp.id
                              LEFT JOIN tng.config r ON l.attribute = r.id
                     ORDER BY sortorder
                     """)

    links_data = g.cursor.fetchall()

    colnames = [desc[0] for desc in g.cursor.description]

    links_list = [dict(zip(colnames, row)) for row in links_data]

    for row in links_list:
        row['start_name'] = helpers.get_translation(row['start_name'])
        row['end_name'] = helpers.get_translation(row['end_name'])
        row['config_property'] = helpers.get_translation(
            row['config_property'])
        row['role'] = helpers.get_translation(row['role'])

    map_data = get_base_map()
    if map_id := request.args.get('map_id'):
        # Todo: int(map_id) can create problems. Find use case.
        map_data = get_base_map_by_id(int(map_id))

    map_settings = get_map_settings()
    settings = {
        'img': map_settings.index_img,
        'map': map_settings.index_map,
        'img_map': map_settings.img_map,
        'greyscale': map_settings.greyscale,
        'not_sel': 'map' if map_settings.img_map == 'image' else 'image'}

    class_items = get_entities_count_by_case_study()
    entities_dict = {k: v for k, v in class_items.items() if
                     k not in app.config['CLASSES_TO_SKIP']}

    shown_entities = get_shown_entities()
    hidden_entities = get_hidden_entities()
    print(shown_entities)
    print(hidden_entities)
    view_classes = app.config['VIEW_CLASSES']

    return render_template(
        "admin.html",
        config_data=entities,
        entities=entities,
        tabs=tabs,
        activetab=tab,
        activeentry=entry,
        links_data=links_list,
        config_properties=config_list,
        maps=map_data,
        settings=settings,
        class_items=entities_dict,
        shown_entities=shown_entities,
        hidden_entities=hidden_entities,
        view_classes=view_classes)



@app.route('/admin/delete_entry/<id>/<tab>')
@login_required
def delete_entry(tab: str, id_: int) -> Response:
    if current_user.group not in ['admin', 'manager']:
        abort(403)

    g.cursor.execute(f'SELECT config_class FROM tng.config WHERE id = {id_}')
    result = g.cursor.fetchone()
    if result.config_class == 5:
        flash('Main Project cannot be deleted', 'danger')
        return redirect(url_for('admin') + tab)

    g.cursor.execute('DELETE FROM tng.config WHERE id = %(id)s',
                     {'id': int(id_)})
    flash('Entry deleted successfully!', 'success')
    return redirect(url_for('admin') + tab)


@app.route('/admin/delete_link/<link_id>/<tab>/<entry>')
@login_required
def delete_link(link_id: int, tab: str, entry: str) -> Response:
    check_manager_user()

    g.cursor.execute('DELETE FROM tng.links WHERE id = %(link_id)s',
                     {'link_id': int(link_id)})
    flash('Link deleted successfully!', 'success')
    return redirect(url_for('admin') + tab + '/' + entry)


@app.route('/admin/add_link/<domain>/<range_>/<prop>/<role>/<tab>/<entry>',
           methods=['GET', 'POST'])
@login_required
def add_link(
        domain: int,
        range_: int,
        prop: int,
        role: int,
        tab: str,
        entry: str) -> Response:
    if current_user.group not in ['admin', 'manager']:
        abort(403)
    g.cursor.execute(
        f'INSERT INTO tng.links (domain_id, range_id, property, attribute, '
        f'sortorder) '
        f'VALUES ({domain}, {range_}, {prop}, NULLIF({role}, 0), COALESCE(('
        f'SELECT (sortorder + 1) FROM tng.links WHERE sortorder IS NOT NULL '
        f'ORDER BY sortorder DESC LIMIT 1),1))')
    flash('Link added successfully', 'success')
    return redirect(url_for('admin') + tab + '/' + entry)


@app.route('/admin/add_entry', methods=['POST'])
@login_required
def add_entry() -> Response:
    check_manager_user()
    language = session.get(
        'language',
        request.accept_languages.best_match(app.config['LANGUAGES'].keys()))
    category = request.form.get('category') or ''
    current_tab = 'nav-' + category
    description = request.form.get('description') or ''
    name = request.form.get('name') or ''
    address = request.form.get('address') or ''
    mail = request.form.get('mail') or ''
    website = request.form.get('website') or ''
    orcid = request.form.get('orcid') or ''
    legal_notice = request.form.get('legalnotice') or ''
    imprint = request.form.get('imprint') or ''
    image = request.form.get('image') or ''

    try:
        tab_config_class = g.config_classes.get(category)
        if tab_config_class == 5:
            flash(f'Error adding entry {name}: Only one main project allowed',
                  'danger')
            return redirect(url_for('admin') + current_tab)

        g.cursor.execute('''
                         INSERT INTO tng.config (name, email, website,
                                                 orcid_id,
                                                 image, config_class)
                         VALUES ('{"de": "Stefan Eichert", "en": "Stefan 
                         Eichert"}'::jsonb,
                                 NULLIF(%s, ''),
                                 NULLIF(%s, ''),
                                 NULLIF(%s, ''),
                                 NULLIF(%s, ''),
                                 %s)
                         RETURNING id
                         ''', (mail, website, orcid, image, tab_config_class))

        new_entry_id = g.cursor.fetchone()[0]
        config_id = new_entry_id

        update_jsonb_column('name', name, language, config_id)
        update_jsonb_column('address', address, language, config_id)
        update_jsonb_column('description', description, language, config_id)
        update_jsonb_column('imprint', imprint, language, config_id)
        update_jsonb_column('legal_notice', legal_notice, language, config_id)

        flash('Entry added successfully!', 'success')
        return redirect(
            url_for('admin') + current_tab + '/' + current_tab + str(
                new_entry_id))

    except Exception as e:
        flash(f'Error adding entry {name}: {str(e)}', 'danger')
        return redirect(url_for('admin') + current_tab)

    # return redirect(url_for('admin') + current_tab)

@app.route('/edit_entry', methods=['POST', 'GET'])
@login_required
def edit_entry() -> Response:
    check_manager_user()
    form_data = {
        'config_id': request.form.get('config_id', type=int),
        'name': request.form.get('name', ''),
        'email': request.form.get('mail', ''),
        'website': request.form.get('website', ''),
        'orcid_id': request.form.get('orcid', ''),
        'image': request.form.get('image', ''),
        'address': request.form.get('address', ''),
        'description': request.form.get('description', ''),
        'imprint': request.form.get('imprint', ''),
        'legal_notice': request.form.get('legalnotice', '')}
    try:
        Admin.edit_entry(form_data, language=g.language)
        flash(f'"{form_data["name"]}" updated successfully', 'success')
    except EntryNotFound:
        flash(f'No config entry found with ID {form_data["config_id"]}',
              'danger')
    except Exception as e:
        flash(f'Error updating "{form_data["name"]}": {e}', 'danger')

    return redirect(
        url_for(
            'admin',
            entry=request.form.get('current_entry'),
            tab=request.form.get('current_tab')))


@app.route('/admin/edit_map', methods=['POST'])
@login_required
def edit_map() -> Response:
    check_manager_user()
    form_data = {
        'name': request.form.get('name', ''),
        'display_name': request.form.get('displayname', ''),
        'sortorder': request.form.get('inputorder', ''),
        'tilestring': request.form.get('description', ''),
        'map_id': request.form.get('map_id')}

    if not form_data['map_id']:
        flash('Map ID is required', 'map danger')
        return redirect(url_for('admin'))
    if not check_if_map_id_exist(int(form_data['map_id'])):
        flash(f'Map with ID {form_data["map_id"]} not found', 'map danger')
        return redirect(url_for('admin'))

    try:
        Admin.update_map(form_data)
        flash('Map updated successfully', 'map success')
    except Exception as e:
        flash(f'Error updating map {form_data["map_id"]}: {e}', 'map danger')
    return redirect(url_for('admin'))


@app.route('/admin/add_map', methods=['POST'])
@login_required
def add_map() -> Response:
    check_manager_user()
    data = {
        'name': request.form.get('name'),
        'display_name': request.form.get('displayname'),
        'sort_order': request.form.get('inputorder'),
        'tile_string': request.form.get('description')}
    try:
        map_id = Admin.add_new_map(data)
        flash(
            f"Map {data['name']} with ID {map_id} added successfully!",
            'map success')
    except Exception as e:
        flash(f"Error adding map {data['name']}: {e}", 'map danger')
    return redirect(url_for('admin'))


@app.route('/admin/delete_map/<int:map_id>')
@login_required
def delete_map(map_id: int) -> Response:
    check_manager_user()
    try:
        Admin.delete_map(map_id)
        flash('Map deleted successfully!', 'map success')
    except Exception as e:
        flash(f'Error deleting map: {str(e)}', 'map danger')
    return redirect(url_for('admin'))


@app.route('/admin/choose_index_background', methods=['POST'])
def choose_index_background() -> Response:
    settings = {
        'index_map': request.form.get('mapselection'),
        'index_img': request.form.get('default_img'),
        'img_map': request.form.get('imgmap'),
        'greyscale': request.form.get('greyscale') == 'on'}
    Admin.set_index_background(settings)
    return redirect(url_for('admin'))


@app.route('/admin/select_entities', methods=['POST'])
def select_entities() -> Response:
    if request.method == 'POST':
        Admin.set_shown_entities(request.form.getlist('selected_entities'))
        flash(_('set shown entities'), 'info')
    return redirect(url_for('admin'))


@app.route('/admin/deselect_entities', methods=['POST'])
def deselect_entities() -> Response:
    if request.method == 'POST':
        Admin.set_hidden_entities(request.form.getlist('selected_entities'))
        flash(_('set hidden entities'), 'info')
    return redirect(url_for('admin'))


# Todo: This reset button is only here for development purpose.
@app.route('/reset')
@login_required
def reset() -> Response:
    # check_manager_user()
    sql_path = os.path.join(current_app.root_path, 'sql', 'admin_reset.sql')
    with open(sql_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()
    g.cursor.execute(sql_script)
    return redirect(url_for('admin'))


def check_manager_user() -> None:
    if current_user.group not in ['admin', 'manager']:
        abort(403)

# @app.route('/sortlinks', methods=['POST'])
# def sort_links() -> Response:
#     @login_required
#     def reset_():
#         if current_user.group not in ['admin', 'manager']:
#             abort(403)
#
#     data = request.get_json()
#     criteria = data['criteria']
#     table = data['table']
#
#     for row in criteria:
#         g.cursor.execute(
#             f'UPDATE tng.{table} SET sortorder = %(order)s  WHERE id = %(
#             id)s',
#             {'id': row['id'], 'order': row['order'], 'table': table})
#     return jsonify({'status': 'ok'})
