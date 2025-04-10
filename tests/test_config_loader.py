"""Pytest unit tests for Mac Flix config loader."""

import pytest
from app.config_loader import load_content_config, load_categories_config, load_secrets_config
from app.models import ContentItem, CategoryConfig, SecretsConfig

def test_load_content_config_valid():
    """Test loading valid content config."""
    content = load_content_config()
    assert isinstance(content, list)
    assert all(isinstance(item, ContentItem) for item in content)

def test_load_categories_config_valid():
    """Test loading valid categories config."""
    categories = load_categories_config()
    assert isinstance(categories, CategoryConfig)
    assert isinstance(categories.categories, list)

def test_load_secrets_config_valid():
    """Test loading valid secrets config."""
    secrets = load_secrets_config()
    assert isinstance(secrets, SecretsConfig)
    assert isinstance(secrets.tmdb_api_key, str)
    assert secrets.tmdb_api_key != ""

def test_load_content_config_failure(tmp_path, monkeypatch):
    """Test failure on invalid content config."""
    # Point to a bad YAML file
    bad_yaml = tmp_path / "bad_content.yaml"
    bad_yaml.write_text("invalid: [unclosed_list")
    monkeypatch.setattr("app.config_loader.CONFIG_DIR", tmp_path)
    with pytest.raises(Exception):
        _ = load_content_config()
