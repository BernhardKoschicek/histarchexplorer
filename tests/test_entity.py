import pytest
from flask.testing import FlaskClient
from requests.exceptions import HTTPError


def test_entity_nonexistent(
        authenticated_client: FlaskClient) -> None:
    with pytest.raises(HTTPError):
        authenticated_client.get('/entity/999999')


def test_entity_valid(
        authenticated_client: FlaskClient) -> None:
    with pytest.raises(HTTPError):
        authenticated_client.get('/entity/1')


def test_entity_redirects_unauthenticated(
        client: FlaskClient) -> None:
    rv = client.get('/entity/1')
    assert rv.status_code == 302
