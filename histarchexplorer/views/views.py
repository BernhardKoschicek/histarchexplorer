from typing import Optional

from flask import redirect, render_template, request, session
from werkzeug import Response

from histarchexplorer import app


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/entities')
def entities() -> str:
    return render_template('entities.html')


@app.route('/search')
def search() -> str:
    return render_template('search.html')


@app.route('/about')
def about() -> str:
    return render_template('about.html')


@app.route('/language=<language>')
def set_language(language: Optional[str] = None) -> Response:
    session['language'] = language
    return redirect(request.referrer)
