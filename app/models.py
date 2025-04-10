"""Pydantic models for Mac Flix configs and API."""

from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Union, Literal

class ContentItem(BaseModel):
    """A movie or TV show item."""
    id: str
    title: str
    type: Literal["movie", "tv"]
    year: int
    genres: List[str]
    description: str
    rating: Optional[float] = None
    poster_url: HttpUrl
    trailer_url: Optional[HttpUrl] = None
    cast: Optional[List[str]] = None
    director: Optional[str] = None
    duration: Optional[int] = None  # minutes
    language: Optional[str] = None
    video_url: HttpUrl
    download_url: Optional[HttpUrl] = None

class Filter(BaseModel):
    """A filter within a category."""
    name: str
    type: Literal["genre", "year", "rating"]
    value: Union[str, int, float]

class Category(BaseModel):
    """A UI category with optional filters."""
    name: str
    filters: Optional[List[Filter]] = None

class CategoryConfig(BaseModel):
    """Categories and filters config."""
    categories: List[Category]

class SecretsConfig(BaseModel):
    """API keys and secrets."""
    tmdb_api_key: str
    other_api_keys: Optional[Dict[str, str]] = None
