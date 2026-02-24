# pylint: disable=redefined-outer-name
import os
import subprocess
from typing import Any, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from histarchexplorer import app as flask_app_instance


@pytest.fixture(scope='session')
def flask_app() -> Flask:
    app = flask_app_instance
    app.config.from_object('config.default')

    try:
        app.config.from_pyfile('testing.py', silent=False)
    except FileNotFoundError:
        pytest.exit(
            "CRITICAL: 'instance/testing.py' not found! \n"
            "Please copy 'testing.py.example' to 'instance/testing.py' "
            "and configure your test database."
        )

    if not app.config.get('TESTING'):
        pytest.exit("CRITICAL: The application is not in TESTING mode!")

    app.config['SERVER_NAME'] = 'localhost.localdomain'
    app.config['PREFERRED_URL_SCHEME'] = 'http'

    _reset_test_database(app)

    return app


def _reset_test_database(app: Flask) -> None:
    db_name = app.config['DATABASE_NAME']
    db_user = app.config['DATABASE_USER']
    db_pass = app.config['DATABASE_PASS']
    db_host = app.config['DATABASE_HOST']
    db_port = str(app.config['DATABASE_PORT'])

    print(f"\nResetting test database: {db_name}...")

    env = os.environ.copy()
    env['PGPASSWORD'] = db_pass

    psql_command_schema = [
        'psql',
        '-U', db_user,
        '-h', db_host,
        '-p', db_port,
        '-d', db_name,
        '-c', 'DROP SCHEMA IF EXISTS tng CASCADE;',
        '-c', 'CREATE SCHEMA tng;',
        '-c', f'ALTER SCHEMA tng OWNER TO {db_user};'
    ]

    try:
        subprocess.run(psql_command_schema, env=env, check=True,
                       capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.exit(f"Failed to reset schema: {e.stderr}")

    reset_sql_path = os.path.join(app.root_path, 'sql', 'reset.sql')
    if not os.path.exists(reset_sql_path):
        pytest.exit(f"SQL file not found: {reset_sql_path}")

    with open(reset_sql_path, 'r') as f:
        try:
            subprocess.run(
                ['psql', '-U', db_user, '-h', db_host, '-p', db_port, '-d',
                 db_name],
                stdin=f,
                env=env,
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            pytest.exit(f"Failed to load reset.sql: {e.stderr}")

    test_user_sql_path = os.path.join(
        os.path.dirname(__file__),
        'sql',
        'add_test_user.sql')

    if not os.path.exists(test_user_sql_path):
        test_user_sql_path = os.path.join(
            app.root_path,
            'sql',

            'add_test_user.sql')

    if os.path.exists(test_user_sql_path):
        with open(test_user_sql_path, 'r') as f:
            try:
                subprocess.run(
                    ['psql', '-U', db_user, '-h', db_host, '-p', db_port, '-d',
                     db_name],
                    stdin=f,
                    env=env,
                    check=True,
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError as e:
                pytest.exit(f"Failed to load add_test_user.sql: {e.stderr}")
    else:
        print(
            f"Warning: Test user SQL script not found at {test_user_sql_path}")

    print("Test database reset complete.")


@pytest.fixture
def client(flask_app: Flask) -> Generator[FlaskClient, Any, None]:
    with flask_app.test_client() as test_client:
        # Establish an application context before running the tests.
        with flask_app.app_context():
            yield test_client
