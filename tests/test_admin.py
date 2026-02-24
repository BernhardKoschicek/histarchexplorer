from flask import url_for
from flask.testing import FlaskClient


def login(client: FlaskClient, username, password):
    """Helper function to log in a user."""
    return client.post(
        url_for('login'),
        data={'username': username, 'password': password},
        follow_redirects=True)


def test_admin_unauthorized_access(client: FlaskClient):
    """Test that unauthorized users are redirected to the login page."""
    response = client.get(url_for('admin'), follow_redirects=True)
    assert response.status_code == 200
    assert b"Username" in response.data


def test_admin_login_and_main_page_access(client: FlaskClient):
    """Test login and access to the main admin page."""
    login(client, 'testuser', 'testpassword')
    response = client.get(url_for('admin'))
    assert response.status_code == 200
    assert b"TOOLS" in response.data


def test_admin_cache_clearing(client: FlaskClient):
    """Test the cache clearing functionality."""
    login(client, 'testuser', 'testpassword')
    response = client.get(url_for('clear_cache'), follow_redirects=True)
    assert response.status_code == 200
    assert b"cache cleared" in response.data


def test_admin_cache_warmup(client: FlaskClient):
    """Test the cache warmup functionality."""
    login(client, 'testuser', 'testpassword')
    # Testing refresh_entity_cache route which triggers warmup
    response = client.get(url_for('refresh_entity_cache'), follow_redirects=True)
    assert response.status_code == 200
    assert b"Cache warmup started" in response.data


def test_admin_database_reset(client: FlaskClient):
    """Test the database reset functionality."""
    login(client, 'testuser', 'testpassword')
    response = client.get(url_for('reset'), follow_redirects=True)
    assert response.status_code == 200
    assert b"reset database" in response.data


def test_admin_selection_settings(client: FlaskClient):
    """Test selecting and deselecting entities in settings."""
    login(client, 'testuser', 'testpassword')

    # Deselect
    response = client.post(
        url_for('deselect_entities'),
        data={'selected_entities': ['source', 'external_reference']},
        follow_redirects=True)
    assert b"set hidden entities" in response.data

    # Select
    response = client.post(
        url_for('select_entities'),
        data={'selected_entities': ['source', 'external_reference']},
        follow_redirects=True)
    assert b"set shown entities" in response.data


def test_admin_update_general_settings(client: FlaskClient):
    """Test updating general settings and AJAX check."""
    login(client, 'testuser', 'testpassword')

    # AJAX check
    response = client.get(
        url_for('check_case_study_id_ajax', entity_id=2),
        follow_redirects=True)
    assert response.status_code == 200

    # Valid Update
    response = client.post(
        url_for('update_general_settings', id_=8240),
        data={'darkMode': 'on', 'languageSelection': 'on'},
        follow_redirects=True)
    assert b"updated case study id successfully" in response.data

    # Invalid Update
    response = client.post(
        url_for('update_general_settings', id_=999999),
        data={},
        follow_redirects=True)
    assert b"Invalid Case Study ID" in response.data


def test_admin_add_and_delete_link(client: FlaskClient):
    """Test adding and deleting a link."""
    login(client, 'testuser', 'testpassword')

    add_url = url_for(
        'add_link',
        domain=1,
        range=2,
        property=1,
        role=1)
    add_response = client.get(add_url, follow_redirects=True)
    assert b"Link added successfully" in add_response.data

    delete_response = client.get(
        url_for(
            'delete_link',
            link_id=1,
            tab='nav-main-project',
            entry='nav-main-project1'),
        follow_redirects=True)
    assert b"Link deleted successfully" in delete_response.data


def test_admin_add_entry(client: FlaskClient):
    """Test adding a new entry."""
    login(client, 'testuser', 'testpassword')
    response = client.post(url_for('add_entry'), data={
        'category': 'persons',
        'name': 'Test Person',
        'email': 'test@example.com'
    }, follow_redirects=True)
    assert b"Entry added successfully!" in response.data


def test_admin_delete_entry(client: FlaskClient):
    """Test deleting an entry."""
    login(client, 'testuser', 'testpassword')
    # Assuming ID 2 exists in test data and is not a main project
    response = client.get(
        url_for('delete_entry', id_=2, tab='nav-persons'),
        follow_redirects=True)
    assert b"Entry deleted successfully!" in response.data


def test_admin_logout(client: FlaskClient):
    """Test the logout functionality."""
    login(client, 'testuser', 'testpassword')
    response = client.get(url_for('logout'), follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data or b"Username" in response.data
