from flask import url_for
from flask.testing import FlaskClient


def test_entity_view_main_page(client: FlaskClient):
    """Test the main entity view page."""
    # Using ID 2 (Stefan Eichert) which is known to exist in reset.sql
    response = client.get(url_for('entity_view', id_=2))
    assert response.status_code == 200
    assert b"Stefan Eichert" in response.data


def test_get_entity_overview(client: FlaskClient):
    """Test the overview tab for an entity."""
    response = client.get(url_for('get_entity', id_=2, tab_name='overview'))
    assert response.status_code == 200
    assert b"Stefan Eichert" in response.data


def test_get_entity_map(client: FlaskClient):
    """Test the map tab for an entity."""
    # This might return empty content if no geo data exists, but should be 200 OK
    response = client.get(url_for('get_entity', id_=2, tab_name='map'))
    assert response.status_code == 200


def test_get_entity_subunits(client: FlaskClient):
    """Test the subunits tab for an entity."""
    response = client.get(url_for('get_entity', id_=2, tab_name='subunits'))
    assert response.status_code == 200


def test_get_entity_media(client: FlaskClient):
    """Test the media tab for an entity."""
    response = client.get(url_for('get_entity', id_=2, tab_name='media'))
    assert response.status_code == 200


def test_entity_view_invalid_tab(client: FlaskClient):
    """Test accessing an invalid tab on the main entity view."""
    response = client.get(url_for('entity_view', id_=2, tab_name='invalid_tab'))
    assert response.status_code == 404


def test_get_entity_invalid_tab(client: FlaskClient):
    """Test accessing an invalid tab via the AJAX endpoint."""
    response = client.get(url_for('get_entity', id_=2, tab_name='invalid_tab'))
    assert response.status_code == 404


def test_presentation_view_api(client: FlaskClient):
    """Test the presentation view API endpoint."""
    response = client.get(url_for('presentation_view', id_=2))
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['id'] == 2
    assert 'Stefan Eichert' in str(data)


def test_entity_data_api(client: FlaskClient):
    """Test the entity data API endpoint."""
    response = client.get(url_for('entity_data', id_=2))
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert 'entity' in data
    assert data['entity']['id'] == 2
