from flask.testing import FlaskClient


def test_about(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get('/about')
    assert rv.status_code == 200


def test_about_with_slug(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get(
        '/about/thanados-netzwerk')
    assert rv.status_code in (200, 404)


def test_publications(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get('/publications')
    assert rv.status_code == 200


def test_about_redirects_unauthenticated(
        client: FlaskClient) -> None:
    rv = client.get('/about')
    assert rv.status_code == 302
