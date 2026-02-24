from flask import url_for
from flask.testing import FlaskClient


def test_view_media_image(client: FlaskClient):
    """Test the media view for an image."""
    response = client.get(url_for('view_media', render_type='image', id_=1))
    assert response.status_code == 200
    assert b"IIIF" in response.data  # Check for content from the iiif.html template


def test_view_media_3d_model(client: FlaskClient):
    """Test the media view for a 3D model."""
    response = client.get(url_for('view_media', render_type='3d_model', id_=1))
    assert response.status_code == 200
    assert b"3D Model Viewer" in response.data # Placeholder, adjust to actual content


def test_view_media_video(client: FlaskClient):
    """Test the media view for a video."""
    response = client.get(url_for('view_media', render_type='video', id_=1))
    assert response.status_code == 200
    assert b"Video Player" in response.data # Placeholder, adjust to actual content


def test_view_media_pdf(client: FlaskClient):
    """Test the media view for a PDF."""
    response = client.get(url_for('view_media', render_type='pdf', id_=1))
    assert response.status_code == 200
    assert b"PDF Viewer" in response.data # Placeholder, adjust to actual content


def test_view_media_svg(client: FlaskClient):
    """Test the media view for an SVG."""
    response = client.get(url_for('view_media', render_type='svg', id_=1))
    assert response.status_code == 200
    assert b"SVG Viewer" in response.data # Placeholder, adjust to actual content


def test_view_media_unsupported(client: FlaskClient):
    """Test the media view for an unsupported type."""
    response = client.get(url_for('view_media', render_type='unsupported_type', id_=1))
    assert response.status_code == 200
    assert b"Unsupported render type" in response.data
