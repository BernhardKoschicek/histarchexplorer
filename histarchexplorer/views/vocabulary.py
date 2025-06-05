from flask import Blueprint, render_template

vocabulary_bp = Blueprint("vocabulary", __name__)

@vocabulary_bp.route("/vocabulary")
def vocabulary():
    return render_template("vocabulary.html")
