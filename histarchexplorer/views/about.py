from flask import g, render_template

from histarchexplorer import app
from histarchexplorer.services.about import ConfigEntities

@app.route('/about')
def about() -> str:
    grouped = ConfigEntities.group_by_class_name(g.config_entities)
    return render_template(
        'about.html',
        project=grouped.get('main-project', [None])[0],
        sub_projects=grouped.get('project', []),
        institutions=grouped.get('institution', []),
        persons=grouped.get('person', []))
