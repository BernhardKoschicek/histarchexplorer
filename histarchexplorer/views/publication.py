from histarchexplorer import app
from histarchexplorer.utils.view_util import render_page_template


@app.route('/publication')
def publication() -> str:
    return render_page_template('publication')
