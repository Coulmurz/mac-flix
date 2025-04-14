"""
Tests for Streamlit utilities and helper functions.
"""
import pytest
import json
from unittest.mock import patch, MagicMock

# We can't directly test Streamlit UI components, but we can test any helper functions
# or utilities that the app might use. This file serves as a placeholder for such tests.

def test_filter_content_by_type():
    """Test filtering content by type."""
    # Sample data
    sample_data = [
        {"title": "Movie 1", "type": "movie"},
        {"title": "TV Show 1", "type": "tv"},
        {"title": "Movie 2", "type": "movie"}
    ]
    
    # Test filtering for movies
    filtered_movies = [item for item in sample_data if item["type"] == "movie"]
    assert len(filtered_movies) == 2
    assert filtered_movies[0]["title"] == "Movie 1"
    assert filtered_movies[1]["title"] == "Movie 2"
    
    # Test filtering for TV shows
    filtered_tv_shows = [item for item in sample_data if item["type"] == "tv"]
    assert len(filtered_tv_shows) == 1
    assert filtered_tv_shows[0]["title"] == "TV Show 1"

@patch('requests.get')
def test_fetch_data_success(mock_get):
    """Test successful data fetching."""
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"title": "Test Movie"}]
    mock_get.return_value = mock_response
    
    # Test function
    import requests
    
    def fetch_data(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    result = fetch_data("http://test-api.com/content")
    assert result == [{"title": "Test Movie"}]
    mock_get.assert_called_once_with("http://test-api.com/content")

@patch('requests.get')
def test_fetch_data_failure(mock_get):
    """Test failed data fetching."""
    # Mock response for a 404 error
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_get.return_value = mock_response
    
    # Test function
    import requests
    
    def fetch_data(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return []
    
    result = fetch_data("http://test-api.com/content")
    assert result == []
    mock_get.assert_called_once_with("http://test-api.com/content")

def test_create_content_dict():
    """Test creating a dictionary of content items."""
    # Sample data
    sample_data = [
        {"title": "Movie 1", "id": "m1"},
        {"title": "TV Show 1", "id": "tv1"}
    ]
    
    # Create a dictionary using titles as keys
    content_dict = {}
    for item in sample_data:
        content_dict[item["title"]] = item
    
    assert len(content_dict) == 2
    assert "Movie 1" in content_dict
    assert "TV Show 1" in content_dict
    assert content_dict["Movie 1"]["id"] == "m1"
    assert content_dict["TV Show 1"]["id"] == "tv1"

def test_build_stream_url():
    """Test building a streaming URL."""
    # Test for a movie
    movie_id = "tt0111161"
    stream_url = f"http://localhost:8000/stream/{movie_id}"
    assert stream_url == "http://localhost:8000/stream/tt0111161"
    
    # Test for a TV episode
    content_id = "tt0944947"
    season_num = 1
    episode_num = 2
    episode_stream_url = f"http://localhost:8000/stream/episode/{content_id}/{season_num}/{episode_num}"
    assert episode_stream_url == "http://localhost:8000/stream/episode/tt0944947/1/2"

def test_build_download_url():
    """Test building a download URL."""
    content_id = "tt0111161"
    download_url = f"http://localhost:8000/download/{content_id}"
    assert download_url == "http://localhost:8000/download/tt0111161"
