from flask import url_for
from flask.testing import FlaskClient


def test_about_page(client: FlaskClient) -> None:
    """
    Test the about page for a successful response and content.
    """
    response = client.get(url_for('about'))
    assert response.status_code == 200
    assert b"About" in response.data
