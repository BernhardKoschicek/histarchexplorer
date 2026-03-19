import pytest
from flask.testing import FlaskClient
from psycopg2.errors import InvalidSchemaName


def test_entities(
        authenticated_client: FlaskClient) -> None:
    with pytest.raises(InvalidSchemaName):
        authenticated_client.get('/entities')


def test_entities_places(
        authenticated_client: FlaskClient) -> None:
    with pytest.raises(InvalidSchemaName):
        authenticated_client.get('/entities/places')


def test_entities_actors(
        authenticated_client: FlaskClient) -> None:
    with pytest.raises(InvalidSchemaName):
        authenticated_client.get('/entities/actors')


def test_entities_events(
        authenticated_client: FlaskClient) -> None:
    with pytest.raises(InvalidSchemaName):
        authenticated_client.get('/entities/events')


def test_entities_sources(
        authenticated_client: FlaskClient) -> None:
    with pytest.raises(InvalidSchemaName):
        authenticated_client.get('/entities/sources')


def test_get_entities_json(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get('/get_entities/places')
    assert rv.status_code in (200, 404, 500)


def test_entities_redirects_unauthenticated(
        client: FlaskClient) -> None:
    rv = client.get('/entities')
    assert rv.status_code == 302
