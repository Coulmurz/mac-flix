"""
Pytest fixtures for testing the Mac Flix application.
"""
import pytest
from fastapi.testclient import TestClient
import yaml
import json
import os
from pathlib import Path

# Import app to be tested
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app, Content, Season, Episode, Category, Secrets

@pytest.fixture
def test_client():
    """
    Create a test client for the FastAPI application.
    """
    with TestClient(app) as client:
        yield client

@pytest.fixture
def sample_content_yaml():
    """
    Sample content YAML data for testing.
    """
    return """
movies:
  - id: "tt0111161"
    title: "The Shawshank Redemption"
    type: "movie"
    year: 1994
    genres: ["Drama", "Crime"]
    description: "Two imprisoned men bond over a number of years."
    rating: 9.3
    poster_url: "https://example.com/posters/shawshank.jpg"
    trailer_url: "https://youtube.com/watch?v=6hB3S9bIaco"
    cast: ["Tim Robbins", "Morgan Freeman"]
    director: "Frank Darabont"
    duration: 142
    language: "English"
    video_url: "https://example.com/videos/shawshank.mp4"
    download_url: "https://example.com/downloads/shawshank.mp4"

  - id: "tt0944947"
    title: "Game of Thrones"
    type: "tv"
    year: 2011
    genres: ["Drama", "Fantasy", "Adventure"]
    description: "Nine noble families fight for control over the lands of Westeros."
    rating: 9.2
    poster_url: "https://example.com/posters/got.jpg"
    trailer_url: "https://youtube.com/watch?v=KPLWWIOCOOQ"
    cast: ["Emilia Clarke", "Kit Harington"]
    director: "Various"
    duration: 60
    language: "English"
    video_url: "https://example.com/videos/got.mp4"
    download_url: "https://example.com/downloads/got.mp4"
    seasons:
      - season_number: 1
        episodes:
          - episode_number: 1
            title: "Winter Is Coming"
            description: "Lord Eddard Stark is torn between his family and his duty when asked to serve at King Robert's side as Hand of the King."
            poster_url: "https://example.com/posters/got_s1e1.jpg"
          - episode_number: 2
            title: "The Kingsroad"
            description: "While Bran recovers from his fall, Ned travels to King's Landing with his daughters."
            poster_url: "https://example.com/posters/got_s1e2.jpg"
"""

@pytest.fixture
def sample_categories_yaml():
    """
    Sample categories YAML data for testing.
    """
    return """
categories:
  - name: "Action"
    filters:
      - name: "Genre: Action"
        type: "genre"
        value: "Action"
  - name: "Drama"
    filters:
      - name: "Genre: Drama"
        type: "genre"
        value: "Drama"
  - name: "Fantasy"
    filters:
      - name: "Genre: Fantasy"
        type: "genre"
        value: "Fantasy"
"""

@pytest.fixture
def sample_secrets_yaml():
    """
    Sample secrets YAML data for testing.
    """
    return """
tmdb_api_key: "test_tmdb_key_12345"
other_api_keys:
  omdb: "test_omdb_key_67890"
  imdb: "test_imdb_key_abcde"
"""

@pytest.fixture
def sample_content_objects():
    """
    Sample Content objects for testing.
    """
    movie = Content(
        id="tt0111161",
        title="The Shawshank Redemption",
        type="movie",
        year=1994,
        genres=["Drama", "Crime"],
        description="Two imprisoned men bond over a number of years.",
        rating=9.3,
        poster_url="https://example.com/posters/shawshank.jpg",
        trailer_url="https://youtube.com/watch?v=6hB3S9bIaco",
        cast=["Tim Robbins", "Morgan Freeman"],
        director="Frank Darabont",
        duration=142,
        language="English",
        video_url="https://example.com/videos/shawshank.mp4",
        download_url="https://example.com/downloads/shawshank.mp4",
    )
    
    episodes_s1 = [
        Episode(
            episode_number=1,
            title="Winter Is Coming",
            description="Lord Eddard Stark is torn between his family and his duty when asked to serve at King Robert's side as Hand of the King.",
            poster_url="https://example.com/posters/got_s1e1.jpg"
        ),
        Episode(
            episode_number=2,
            title="The Kingsroad",
            description="While Bran recovers from his fall, Ned travels to King's Landing with his daughters.",
            poster_url="https://example.com/posters/got_s1e2.jpg"
        )
    ]
    
    season1 = Season(season_number=1, episodes=episodes_s1)
    
    tv_show = Content(
        id="tt0944947",
        title="Game of Thrones",
        type="tv",
        year=2011,
        genres=["Drama", "Fantasy", "Adventure"],
        description="Nine noble families fight for control over the lands of Westeros.",
        rating=9.2,
        poster_url="https://example.com/posters/got.jpg",
        trailer_url="https://youtube.com/watch?v=KPLWWIOCOOQ",
        cast=["Emilia Clarke", "Kit Harington"],
        director="Various",
        duration=60,
        language="English",
        video_url="https://example.com/videos/got.mp4",
        download_url="https://example.com/downloads/got.mp4",
        seasons=[season1]
    )
    
    return [movie, tv_show]

@pytest.fixture
def mock_config_files(tmp_path, sample_content_yaml, sample_categories_yaml, sample_secrets_yaml):
    """
    Create mock config files in a temporary directory.
    """
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    content_path = config_dir / "content.yaml"
    content_path.write_text(sample_content_yaml)
    
    categories_path = config_dir / "categories.yaml"
    categories_path.write_text(sample_categories_yaml)
    
    secrets_path = config_dir / "secrets.yaml"
    secrets_path.write_text(sample_secrets_yaml)
    
    return {
        "dir": config_dir,
        "content": content_path,
        "categories": categories_path,
        "secrets": secrets_path
    }

@pytest.fixture
def mock_video_file(tmp_path):
    """
    Create a mock video file for testing streaming functionality.
    """
    videos_dir = tmp_path / "videos"
    videos_dir.mkdir()
    
    # Create a small dummy MP4 file
    video_path = videos_dir / "test_video.mp4"
    with open(video_path, 'wb') as f:
        f.write(b'\x00' * 1024)  # 1KB dummy file
    
    return str(video_path)
