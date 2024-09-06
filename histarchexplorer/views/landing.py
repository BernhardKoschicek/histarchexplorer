from flask import render_template, g

from histarchexplorer import app

from histarchexplorer.utils import cerberos



@app.route('/entities/id')
def landing() -> str:
    return render_template('landing.html')