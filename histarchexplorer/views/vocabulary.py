from histarchexplorer import app
from flask import render_template, current_app
import requests

from histarchexplorer.api.parser import Parser
from histarchexplorer.models.entity import Entity
from histarchexplorer.utils.view_util import get_cite_button
from histarchexplorer.views.views import type_tree


@app.route("/vocabulary")
def vocabulary():
    type_filters = current_app.config.get("TYPE_FILTERS", {})
    type_tree_ = type_tree()
    print(type_tree_.json)

    return render_template(
        "vocabulary.html",
        type_tree=type_tree_,
        type_filters=type_filters)


@app.route("/vocabulary/<int:type_id>")
def vocabulary_detail(type_id: int):
    entity = Entity.get_entity(type_id, Parser())
    # Type Tree laden
    res = requests.get("https://thanados.openatlas.eu/api/0.4/type_tree/")
    res.raise_for_status()
    type_tree = res.json().get("typeTree", {})

    # Aktuellen Typ abrufen
    type_ = type_tree.get(str(type_id))
    if not type_:
        return f"Type with ID {type_id} not found.", 404

    # Eltern- und Kindtypen auflösen
    parents = [type_tree.get(str(pid)) for pid in type_.get("root", [])]
    children = [type_tree.get(str(cid)) for cid in type_.get("subs", [])]

    # --------------------------
    # Exact Matches (nur dieser Typ)
    # --------------------------
    exact_res = requests.get(f"https://thanados.openatlas.eu/api/0.4/type_entities/{type_id}")
    exact_res.raise_for_status()
    exact_entities = exact_res.json().get("features", [])

    # --------------------------
    # Subcategory Matches (Kinder und tiefer)
    # --------------------------
    all_res = requests.get(f"https://thanados.openatlas.eu/api/0.4/type_entities_all/{type_id}")
    all_res.raise_for_status()
    raw_results = all_res.json().get("results", [])

    # Alle Features extrahieren
    all_entities = [feature for group in raw_results for feature in group.get("features", [])]

    # Nur Subcategory Matches (exklusive exact matches)
    subcategory_entities = [
        entity for entity in all_entities
        if entity not in exact_entities
    ]

    return render_template(
        "vocabulary_detail.html",
        entity=entity,
        type=type_,
        parents=parents,
        children=children,
        exact_entities=exact_entities,
        subcategory_entities=subcategory_entities,
        cite_button=get_cite_button(entity)
    )

