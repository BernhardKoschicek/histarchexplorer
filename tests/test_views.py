from flask.testing import FlaskClient


def test_index(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get('/')
    assert rv.status_code == 200


def test_index_redirects_unauthenticated(
        client: FlaskClient) -> None:
    rv = client.get('/')
    assert rv.status_code == 302


def test_set_language(client: FlaskClient) -> None:
    rv = client.get('/language=de')
    assert rv.status_code in (200, 302)


def test_set_language_en(
        client: FlaskClient) -> None:
    rv = client.get('/language=en')
    assert rv.status_code in (200, 302)


def test_type_tree(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get('/type-tree')
    assert rv.status_code == 200


def test_files_of_entities(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get('/files-of-entities')
    assert rv.status_code == 200


def test_entities_count(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get('/entities-count')
    assert rv.status_code == 200
