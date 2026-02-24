from flask import url_for
from flask.testing import FlaskClient


def test_browse_page_loads(client: FlaskClient):
    """Test that the main browse page loads correctly."""
    response = client.get(url_for('entities'))
    assert response.status_code == 200
    assert b"Browse Entities" in response.data  # A placeholder for a title on the browse page


def test_get_entities_for_tab(client: FlaskClient):
    """Test the 'get_entities' endpoint for a specific tab."""
    # This tests the AJAX-like endpoint that would load entities for a category
    response = client.get(url_for('get_entities', tab_name='place'))
    assert response.status_code == 200
    # The response should be a rendered template snippet, let's check for some expected content
    assert b"Name" in response.data
    assert b"Description" in response.data
