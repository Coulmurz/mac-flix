"""Main FastAPI application for Mac Flix backend MVP."""

import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from app.models import ContentItem, CategoryConfig, SecretsConfig
from app.config_loader import load_content_config, load_categories_config
from app.tmdb_client import TMDBClient
from typing import List

app = FastAPI(
    title="Mac Flix Backend API",
    description="FastAPI backend for Mac Flix MVP. Serves metadata, streaming, and download endpoints.",
    version="0.1.0"
)

# Load configs at startup
content_items: List[ContentItem] = []
categories: CategoryConfig | None = None
secrets: SecretsConfig | None = None

@app.on_event("startup")
def startup_event():
    global content_items, categories, secrets
    content_items = load_content_config()
    categories = load_categories_config()
    secrets = SecretsConfig(
        tmdb_api_key=os.getenv("TMDB_API_KEY", ""),
        other_api_keys=None
    )

@app.get("/")
def root():
    """Root endpoint with welcome message."""
    return {"message": "Welcome to Mac Flix Backend API"}

@app.get("/content", response_model=List[ContentItem])
def get_all_content():
    """Get all content items."""
    return content_items

@app.get("/content/{item_id}", response_model=ContentItem)
def get_content_item(item_id: str):
    """Get a content item by ID."""
    for item in content_items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Content item not found")

@app.get("/categories", response_model=CategoryConfig)
def get_categories():
    """Get categories and filters."""
    return categories


@app.get("/stream/{item_id}")
def stream_content(item_id: str):
    """Redirect to the streaming video URL for the content item."""
    for item in content_items:
        if item.id == item_id:
            return RedirectResponse(item.video_url)
    raise HTTPException(status_code=404, detail="Content item not found")


@app.get("/download/{item_id}")
def download_content(item_id: str):
    """Redirect to the download URL or fallback to video URL."""
    for item in content_items:
        if item.id == item_id:
            if item.download_url:
                return RedirectResponse(item.download_url)
            else:
                return RedirectResponse(item.video_url)
    raise HTTPException(status_code=404, detail="Content item not found")


@app.get("/tmdb/search")
def tmdb_search(query: str, media_type: str = "movie"):
    """Search TMDB for movies or TV shows."""
    client = TMDBClient()
    try:
        results = client.search(query, media_type)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/omdb/search")
def omdb_search(title: str):
    """Search OMDB for movies by title."""
    from app.omdb_client import OMDBClient
    client = OMDBClient()
    try:
        results = client.search(title)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
