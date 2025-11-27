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

    return render_template(
        "about.html",
        active=active,
        main_project=main_project,
        sub_projects=project_choices or sub_projects,
        config_entities_mapped=config_entities_mapped)
