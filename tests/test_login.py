from flask import url_for, session
from flask.testing import FlaskClient
from flask_login import current_user


def test_login_page_loads(client: FlaskClient):
    """Test that the login page loads correctly."""
    response = client.get(url_for('login'))
    assert response.status_code == 200
    assert b"Username" in response.data


def test_successful_login(client: FlaskClient):
    """Test a successful login with a valid user."""
    response = client.post(url_for('login'), data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert current_user.is_authenticated
    assert b"Logout" in response.data  # A common indicator of being logged in


def test_login_with_wrong_password(client: FlaskClient):
    """Test login attempt with an incorrect password."""
    response = client.post(url_for('login'), data={
        'username': 'testuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert not current_user.is_authenticated
    assert b"error wrong password" in response.data


def test_login_with_nonexistent_user(client: FlaskClient):
    """Test login attempt with a username that does not exist."""
    response = client.post(url_for('login'), data={
        'username': 'nonexistentuser',
        'password': 'somepassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert not current_user.is_authenticated
    assert b"error username" in response.data


def test_login_with_inactive_user(client: FlaskClient):
    """Test login attempt with an inactive user."""
    # This assumes 'inactiveuser' is set up in your test data (add_test_user.sql)
    response = client.post(url_for('login'), data={
        'username': 'inactiveuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert not current_user.is_authenticated
    assert b"error inactive" in response.data


def test_logout(client: FlaskClient):
    """Test the logout functionality."""
    # First, log in
    client.post(url_for('login'), data={'username': 'testuser', 'password': 'testpassword'}, follow_redirects=True)
    assert current_user.is_authenticated

    # Then, log out
    response = client.get(url_for('logout'), follow_redirects=True)
    assert response.status_code == 200
    assert not current_user.is_authenticated
    assert b"Login" in response.data
