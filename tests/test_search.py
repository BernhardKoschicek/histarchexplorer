from flask import url_for
from flask.testing import FlaskClient


def test_search_page_loads(client: FlaskClient):
    """Test that the search page loads correctly."""
    response = client.get(url_for('search'))
    assert response.status_code == 200
    assert b"Search" in response.data


def test_perform_search(client: FlaskClient):
    """Test performing a search via POST request."""
    # Searching for 'Stefan' which should find 'Stefan Eichert' (ID 2)
    response = client.post(url_for('search'), data={
        'query': 'Stefan',
        'category': 'all'
    })
    assert response.status_code == 200
    # Note: The actual search logic depends on external API calls or DB queries.
    # If it uses the local DB, it should find Stefan. If it uses an external API,
    # we might need to mock it or just check that the page renders without error.
    # Assuming it renders the search results page:
    assert b"Stefan" in response.data


def test_search_live(client: FlaskClient):
    """Test the live search AJAX endpoint."""
    response = client.get(url_for('search_live', q='Stefan'))
    assert response.status_code == 200
    assert response.is_json
    # Again, results depend on the backend implementation.
    # We check if we get a valid JSON response.
    data = response.get_json()
    assert isinstance(data, list)
