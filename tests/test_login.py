from flask.testing import FlaskClient


def test_login_page(client: FlaskClient) -> None:
    rv = client.get('/login')
    assert rv.status_code == 200


def test_login_invalid_credentials(client: FlaskClient) -> None:
    rv = client.post('/login', data={
        'username': 'invalid',
        'password': 'invalid',
        'save': 'login'})
    assert rv.status_code == 200


def test_logout_redirects(client: FlaskClient) -> None:
    rv = client.get('/logout', follow_redirects=False)
    assert rv.status_code in (302, 401)
