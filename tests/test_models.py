"""
Tests for the model classes and YAML loading functionality.
"""
import pytest
import yaml
from pydantic import ValidationError

from app.main import Content, Season, Episode, Category, Secrets, load_config, create_content_objects

def test_load_config(mock_config_files):
    """Test loading configuration from YAML files."""
    # Test loading content config
    content_config = load_config(mock_config_files["content"])
    assert "movies" in content_config
    assert len(content_config["movies"]) == 2
    assert content_config["movies"][0]["title"] == "The Shawshank Redemption"
    
    # Test loading categories config
    categories_config = load_config(mock_config_files["categories"])
    assert "categories" in categories_config
    assert len(categories_config["categories"]) == 3
    assert categories_config["categories"][0]["name"] == "Action"
    
    # Test loading secrets config
    secrets_config = load_config(mock_config_files["secrets"])
    assert "tmdb_api_key" in secrets_config
    assert secrets_config["tmdb_api_key"] == "test_tmdb_key_12345"

def test_content_model_movie():
    """Test creating a movie Content object."""
    movie_data = {
        "id": "tt0111161",
        "title": "The Shawshank Redemption",
        "type": "movie",
        "year": 1994,
        "genres": ["Drama", "Crime"],
        "description": "Two imprisoned men bond over a number of years.",
        "rating": 9.3,
        "poster_url": "https://example.com/posters/shawshank.jpg",
        "trailer_url": "https://youtube.com/watch?v=6hB3S9bIaco",
        "cast": ["Tim Robbins", "Morgan Freeman"],
        "director": "Frank Darabont",
        "duration": 142,
        "language": "English",
        "video_url": "https://example.com/videos/shawshank.mp4",
        "download_url": "https://example.com/downloads/shawshank.mp4"
    }
    
    content = Content(**movie_data)
    assert content.id == movie_data["id"]
    assert content.title == movie_data["title"]
    assert content.type == movie_data["type"]
    assert content.year == movie_data["year"]
    assert content.genres == movie_data["genres"]
    assert content.rating == movie_data["rating"]
    assert content.seasons == []  # Empty seasons for movies

def test_content_model_tv_show():
    """Test creating a TV show Content object with seasons and episodes."""
    tv_data = {
        "id": "tt0944947",
        "title": "Game of Thrones",
        "type": "tv",
        "year": 2011,
        "genres": ["Drama", "Fantasy", "Adventure"],
        "description": "Nine noble families fight for control over the lands of Westeros.",
        "rating": 9.2,
        "poster_url": "https://example.com/posters/got.jpg",
        "trailer_url": "https://youtube.com/watch?v=KPLWWIOCOOQ",
        "cast": ["Emilia Clarke", "Kit Harington"],
        "director": "Various",
        "duration": 60,
        "language": "English",
        "video_url": "https://example.com/videos/got.mp4",
        "download_url": "https://example.com/downloads/got.mp4",
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {
                        "episode_number": 1,
                        "title": "Winter Is Coming",
                        "description": "Lord Eddard Stark is torn between his family and his duty.",
                        "poster_url": "https://example.com/posters/got_s1e1.jpg"
                    }
                ]
            }
        ]
    }
    
    content = Content(**tv_data)
    assert content.id == tv_data["id"]
    assert content.title == tv_data["title"]
    assert content.type == tv_data["type"]
    assert len(content.seasons) == 1
    assert content.seasons[0].season_number == 1
    assert len(content.seasons[0].episodes) == 1
    assert content.seasons[0].episodes[0].episode_number == 1
    assert content.seasons[0].episodes[0].title == "Winter Is Coming"

def test_content_invalid_type():
    """Test validation error for invalid content type."""
    invalid_data = {
        "id": "tt0111161",
        "title": "The Shawshank Redemption",
        "type": "invalid_type",  # Should be 'movie' or 'tv'
        "year": 1994,
        "genres": ["Drama", "Crime"],
        "description": "Two imprisoned men bond over a number of years.",
        "rating": 9.3,
        "poster_url": "https://example.com/posters/shawshank.jpg",
        "trailer_url": "https://youtube.com/watch?v=6hB3S9bIaco",
        "cast": ["Tim Robbins", "Morgan Freeman"],
        "director": "Frank Darabont",
        "duration": 142,
        "language": "English",
        "video_url": "https://example.com/videos/shawshank.mp4",
        "download_url": "https://example.com/downloads/shawshank.mp4"
    }
    
    # This should raise a validation error because 'type' is not 'movie' or 'tv'
    with pytest.raises(ValidationError):
        Content(**invalid_data)

def test_category_model():
    """Test creating a Category object with filters."""
    category_data = {
        "name": "Action",
        "filters": [
            {
                "name": "Genre: Action",
                "type": "genre",
                "value": "Action"
            },
            {
                "name": "Rating: 8+",
                "type": "rating",
                "value": 8.0
            }
        ]
    }
    
    category = Category(**category_data)
    assert category.name == category_data["name"]
    assert len(category.filters) == 2
    assert category.filters[0].name == "Genre: Action"
    assert category.filters[1].type == "rating"
    assert category.filters[1].value == 8.0

def test_secrets_model():
    """Test creating a Secrets object."""
    secrets_data = {
        "tmdb_api_key": "test_tmdb_key_12345",
        "other_api_keys": {
            "omdb": "test_omdb_key_67890",
            "imdb": "test_imdb_key_abcde"
        }
    }
    
    secrets = Secrets(**secrets_data)
    assert secrets.tmdb_api_key == secrets_data["tmdb_api_key"]
    assert secrets.other_api_keys["omdb"] == "test_omdb_key_67890"
    assert secrets.other_api_keys["imdb"] == "test_imdb_key_abcde"

def test_create_content_objects(sample_content_yaml):
    """Test the create_content_objects function."""
    content_config = yaml.safe_load(sample_content_yaml)
    content_objects = create_content_objects(content_config)
    
    assert len(content_objects) == 2
    
    # Check first object (movie)
    movie = content_objects[0]
    assert movie.id == "tt0111161"
    assert movie.title == "The Shawshank Redemption"
    assert movie.type == "movie"
    assert len(movie.seasons) == 0
    
    # Check second object (TV show)
    tv_show = content_objects[1]
    assert tv_show.id == "tt0944947"
    assert tv_show.title == "Game of Thrones"
    assert tv_show.type == "tv"
    assert len(tv_show.seasons) == 1
    assert tv_show.seasons[0].season_number == 1
    assert len(tv_show.seasons[0].episodes) == 2
