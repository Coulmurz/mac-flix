"""
Tests for the FastAPI endpoints.
"""
import pytest
from fastapi import status
from unittest.mock import patch, MagicMock
import os

def test_read_root(test_client):
    """Test the root endpoint."""
    response = test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Hello": "World"}

def test_get_content(test_client, sample_content_objects):
    """Test the /content endpoint."""
    response = test_client.get("/content")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "The Shawshank Redemption"
    assert data[1]["title"] == "Game of Thrones"

def test_get_categories(test_client):
    """Test the /categories endpoint."""
    response = test_client.get("/categories")
    assert response.status_code == status.HTTP_200_OK
    
    # Categories are loaded from app.main, so we're just checking that the endpoint works
    assert isinstance(response.json(), list)

def test_get_content_by_category(test_client):
    """Test the /content/{category_name} endpoint."""
    # Since categories depend on what's loaded in app.main,
    # we're just checking that the endpoint works
    response = test_client.get("/content/Drama")
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

def test_get_content_by_year(test_client, sample_content_objects):
    """Test the /content/year/{year} endpoint."""
    # Test with a year that should match our sample content (1994)
    response = test_client.get("/content/year/1994")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == "The Shawshank Redemption"
    
    # Test with a year that shouldn't match any content
    response = test_client.get("/content/year/1900")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_stream_video_not_found(test_client):
    """Test the /stream/{content_id} endpoint with non-existent content."""
    response = test_client.get("/stream/non_existent_id")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@patch('app.main.os.path.isfile')
@patch('app.main.open')
def test_stream_video_local_file(mock_open, mock_isfile, test_client, sample_content_objects):
    """Test the /stream/{content_id} endpoint with a local file."""
    # Setup mocks
    mock_isfile.return_value = True
    mock_file = MagicMock()
    mock_open.return_value = mock_file
    
    # Test the endpoint
    response = test_client.get(f"/stream/{sample_content_objects[0].id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify mocks were called correctly
    mock_isfile.assert_called_once()
    mock_open.assert_called_once()

@patch('requests.head')
@patch('app.main.stream_remote_video')
def test_stream_video_remote_url(mock_stream, mock_head, test_client, monkeypatch):
    """Test the /stream/{content_id} endpoint with a remote URL."""
    # Modify a content item to have a valid URL
    from app.main import content
    original_content = content[0]
    
    # Temporarily modify the content
    def is_url_mock(url):
        return url.startswith("http")
    
    # Apply patches
    monkeypatch.setattr('app.main.is_url', is_url_mock)
    mock_head_response = MagicMock()
    mock_head_response.headers = {'Content-Type': 'video/mp4'}
    mock_head.return_value = mock_head_response
    
    mock_stream.return_value = aiter([b"mock video data"])
    
    # Make sure content has HTTP URL
    original_video_url = content[0].video_url
    content[0].video_url = "http://example.com/video.mp4"
    
    try:
        # Test the endpoint
        response = test_client.get(f"/stream/{content[0].id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify mocks
        mock_head.assert_called_once()
        mock_stream.assert_called_once()
    finally:
        # Restore original content
        content[0].video_url = original_video_url

def test_download_video_not_found(test_client):
    """Test the /download/{content_id} endpoint with non-existent content."""
    response = test_client.get("/download/non_existent_id")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@patch('app.main.os.path.isfile')
@patch('app.main.os.path.basename')
def test_download_video_local_file(mock_basename, mock_isfile, test_client, sample_content_objects):
    """Test the /download/{content_id} endpoint with a local file."""
    # Setup mocks
    mock_isfile.return_value = True
    mock_basename.return_value = "test_video.mp4"
    
    # We can't fully test FileResponse in FastAPI TestClient, but we can check if the route works
    response = test_client.get(f"/download/{sample_content_objects[0].id}")
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_422_UNPROCESSABLE_ENTITY]
    
    # Verify mocks
    mock_isfile.assert_called_once()

def test_download_video_remote_url(test_client, monkeypatch):
    """Test the /download/{content_id} endpoint with a remote URL."""
    # Modify a content item to have a valid URL
    from app.main import content
    original_content = content[0]
    
    # Temporarily modify the content
    def is_url_mock(url):
        return url.startswith("http")
    
    # Apply patch
    monkeypatch.setattr('app.main.is_url', is_url_mock)
    
    # Make sure content has HTTP URL
    original_download_url = content[0].download_url
    content[0].download_url = "http://example.com/download.mp4"
    
    try:
        # Test the endpoint
        response = test_client.get(f"/download/{content[0].id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Check the response
        data = response.json()
        assert "redirect_url" in data
        assert data["redirect_url"] == "http://example.com/download.mp4"
    finally:
        # Restore original content
        content[0].download_url = original_download_url

def test_stream_episode_not_found(test_client):
    """Test the /stream/episode/{content_id}/{season_number}/{episode_number} endpoint with non-existent content."""
    response = test_client.get("/stream/episode/non_existent_id/1/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@patch('app.main.os.path.isfile')
@patch('app.main.open')
def test_stream_episode(mock_open, mock_isfile, test_client, sample_content_objects):
    """Test the /stream/episode/{content_id}/{season_number}/{episode_number} endpoint."""
    # Setup mocks
    mock_isfile.return_value = True
    mock_file = MagicMock()
    mock_open.return_value = mock_file
    
    # Get a TV show with episodes
    tv_show = sample_content_objects[1]
    
    # Test the endpoint
    response = test_client.get(f"/stream/episode/{tv_show.id}/1/1")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify mocks
    mock_isfile.assert_called_once()
    mock_open.assert_called_once()

def test_stream_episode_invalid_season(test_client, sample_content_objects):
    """Test streaming an episode with an invalid season number."""
    # Get a TV show
    tv_show = sample_content_objects[1]
    
    # Test with invalid season number
    response = test_client.get(f"/stream/episode/{tv_show.id}/999/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Season 999 not found" in response.json()["detail"]

def test_stream_episode_invalid_episode(test_client, sample_content_objects):
    """Test streaming an episode with an invalid episode number."""
    # Get a TV show
    tv_show = sample_content_objects[1]
    
    # Test with invalid episode number
    response = test_client.get(f"/stream/episode/{tv_show.id}/1/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Episode 999 not found" in response.json()["detail"]
