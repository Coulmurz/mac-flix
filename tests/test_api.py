"""Pytest tests for Mac Flix FastAPI backend."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_all_content():
    response = client.get("/content")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_content_item_valid():
    response = client.get("/content")
    items = response.json()
    if items:
        item_id = items[0]["id"]
        resp = client.get(f"/content/{item_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == item_id

def test_get_content_item_invalid():
    response = client.get("/content/nonexistent-id")
    assert response.status_code == 404

def test_get_categories():
    response = client.get("/categories")
    assert response.status_code == 200
    assert "categories" in response.json()

def test_stream_content_valid():
    response = client.get("/content")
    items = response.json()
    if items:
        item_id = items[0]["id"]
        resp = client.get(f"/stream/{item_id}", allow_redirects=False)
        assert resp.status_code in (302, 307)

def test_stream_content_invalid():
    response = client.get("/stream/nonexistent-id", allow_redirects=False)
    assert response.status_code == 404

def test_download_content_valid():
    response = client.get("/content")
    items = response.json()
    if items:
        item_id = items[0]["id"]
        resp = client.get(f"/download/{item_id}", allow_redirects=False)
        assert resp.status_code in (302, 307)

def test_download_content_invalid():
    response = client.get("/download/nonexistent-id", allow_redirects=False)
    assert response.status_code == 404


def test_tmdb_search():
    """Test TMDB search endpoint."""
    response = client.get("/tmdb/search", params={"query": "Inception", "media_type": "movie"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)

def test_omdb_search():
    """Test OMDB search endpoint."""
    response = client.get("/omdb/search", params={"title": "Inception"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
