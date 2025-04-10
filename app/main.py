"""Main FastAPI application for Mac Flix backend MVP."""

from fastapi import FastAPI, HTTPException
from app.models import ContentItem, CategoryConfig, SecretsConfig
from app.config_loader import load_content_config, load_categories_config, load_secrets_config
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
    secrets = load_secrets_config()

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
