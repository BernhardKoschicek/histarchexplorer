from flask.testing import FlaskClient


def test_admin_requires_login(client: FlaskClient) -> None:
    rv = client.get('/admin/')
    assert rv.status_code in (302, 401)


def test_admin_page(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get('/admin/')
    assert rv.status_code == 200


def test_admin_tab_general(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get('/admin/general')
    assert rv.status_code == 200


def test_admin_tab_team(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get('/admin/team')
    assert rv.status_code == 200


def test_admin_tab_projects(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get('/admin/projects')
    assert rv.status_code == 200


def test_admin_tab_maps(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get('/admin/maps')
    assert rv.status_code == 200


def test_admin_clear_cache(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get(
        '/admin/clear-cache',
        follow_redirects=False)
    assert rv.status_code in (302, 200)


def test_admin_refresh_system_cache(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get(
        '/admin/refresh-system-cache',
        follow_redirects=False)
    assert rv.status_code in (302, 200)


def test_admin_backup_db(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.get(
        '/admin/backup_db',
        follow_redirects=False)
    assert rv.status_code in (302, 200)


def test_admin_update_menu(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.post(
        '/admin/update_menu_management',
        data={'menu_data': '{}'},
        follow_redirects=False)
    assert rv.status_code in (302, 200, 400)


def test_admin_update_legal_notice(
        authenticated_client: FlaskClient) -> None:
    rv = authenticated_client.post(
        '/admin/update_legal_notice',
        data={
            'legal_notice_de': '<p>Test</p>',
            'legal_notice_en': '<p>Test</p>'},
        follow_redirects=False)
    assert rv.status_code in (302, 200)
