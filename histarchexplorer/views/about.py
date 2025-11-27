from typing import Optional

from flask import g, render_template

from histarchexplorer import app
from histarchexplorer.models.config import ConfigEntity


@app.route('/about', strict_slashes=False)
@app.route('/about/<int:id_>')
def about(id_: Optional[int] = None):
    grouped = ConfigEntity.group_by_class_name(g.config_entities)
    main_project = grouped.get('main-project', [None])[0]
    sub_projects = grouped.get('project', [])

    config_entities_mapped = {e.id: e for e in g.config_entities}

    active = main_project
    project_choices = []
    if id_:
        active = config_entities_mapped[id_]
        for p in [main_project] + sub_projects:
            if p.id != id_:
                project_choices.append(p)

    people_map = {}
    institutions_map = {}

    for link in active.links:
        target = next((
            e for e in g.config_entities if e.id == link.end_id), None)
        if not target:
            continue

        role = None
        if link.role and link.role['display']:
            role = link.role['display']['label']

        if target.class_name == "person":
            if target.id not in people_map:
                people_map[target.id] = {"entity": target, "roles": []}
            if role:
                people_map[target.id]["roles"].append(role)

        elif target.class_name == "institution":
            if target.id not in institutions_map:
                institutions_map[target.id] = {"entity": target, "roles": []}
            if role:
                institutions_map[target.id]["roles"].append(role)

    return render_template(
        "about.html",
        active=active,
        main_project=main_project,
        sub_projects=project_choices or sub_projects,
        config_entities_mapped=config_entities_mapped,
        people=list(people_map.values()),
        institutions=list(institutions_map.values()))
