"""YAML config loader and validator for Mac Flix."""

import yaml
from pathlib import Path
from typing import List
from app.models import ContentItem, CategoryConfig, SecretsConfig

CONFIG_DIR = Path(__file__).parent / "config"

def load_yaml(path: Path) -> dict:
    """Load a YAML file and return as dict."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_content_config() -> List[ContentItem]:
    """Load and validate content catalog."""
    path = CONFIG_DIR / "content.yaml"
    data = load_yaml(path)
    return [ContentItem(**item) for item in data.get("movies", [])]

def load_categories_config() -> CategoryConfig:
    """Load and validate categories and filters."""
    path = CONFIG_DIR / "categories.yaml"
    data = load_yaml(path)
    return CategoryConfig(**data)

def load_secrets_config() -> SecretsConfig:
    """Load and validate API keys and secrets."""
    path = CONFIG_DIR / "secrets.yaml"
    data = load_yaml(path)
    return SecretsConfig(**data)
