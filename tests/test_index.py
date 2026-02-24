from flask import url_for
from flask.testing import FlaskClient


def test_index_page(client: FlaskClient) -> None:
    """
    Test the index page for a successful response and content.
    """
    response = client.get(url_for('index'))
    assert response.status_code == 200
    assert b"HistArchExplorer" in response.data


def test_set_language_view(client: FlaskClient) -> None:
    """
    Test the language setting functionality.
    """
    test_language = 'de'
    # The 'set_language' view redirects to the referrer, so we set one.
    response = client.get(url_for('set_language', language=test_language), headers={'Referer': '/'})

    # Check that it redirects
    assert response.status_code == 302
    assert response.location == "/"

    # Follow the redirect and check the session
    with client.session_transaction() as session:
        assert session['language'] == test_language
