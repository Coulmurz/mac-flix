from fastapi import FastAPI
import yaml
from pydantic import BaseModel
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

class Content(BaseModel):
    id: str
    title: str
    type: str
    year: int
    genres: List[str]
    description: str
    rating: float
    poster_url: str
    trailer_url: str
    cast: List[str]
    director: str
    duration: int
    language: str
    video_url: str
    download_url: str

from typing import Union

class CategoryFilter(BaseModel):
    name: str
    type: str
    value: Union[str, float]

class Category(BaseModel):
    name: str
    filters: List[CategoryFilter]

class Secrets(BaseModel):
    tmdb_api_key: str
    other_api_keys: Dict[str, str]

def load_config(path: str):
    logging.info(f"Loading config from {path}")
    with open(path, "r") as f:
        config = yaml.safe_load(f)
        logging.info(f"Successfully loaded config from {path}")
        return config

content_config = load_config("app/config/content.yaml")
logging.info("Content config loaded")
categories_config = load_config("app/config/categories.yaml")
logging.info("Categories config loaded")
secrets_config = load_config("app/config/secrets.yaml")
logging.info("Secrets config loaded")

content = [Content(**item) for item in content_config["movies"]]
categories = [Category(**item) for item in categories_config["categories"]]
secrets = Secrets(**secrets_config)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/content")
async def get_content():
    return content

@app.get("/categories")
async def get_categories():
    return categories

@app.get("/secrets")
async def get_secrets():
    return secrets

@app.get("/tmdb_api_key")
async def get_tmdb_api_key():
    return {"tmdb_api_key": secrets.tmdb_api_key}

@app.get("/omdb_api_key")
async def get_omdb_api_key():
    return {"omdb_api_key": secrets.other_api_keys["omdb"]}

@app.get("/categories/{category_name}")
async def get_category(category_name: str):
    for category in categories:
        if category.name == category_name:
            return category
    return {"message": "Category not found"}

@app.get("/content/{category_name}")
async def get_content_by_category(category_name: str):
    filtered_content = []
    for category in categories:
        if category.name == category_name:
            for content_item in content:
                for genre in content_item.genres:
                    if genre in [filter.value for filter in category.filters]:
                        filtered_content.append(content_item)
            return filtered_content
    return {"message": "Category not found"}

@app.get("/content/year/{year}")
async def get_content_by_year(year: int):
    filtered_content = []
    for content_item in content:
        if content_item.year == year:
            filtered_content.append(content_item)
    return filtered_content

@app.get("/secrets/tmdb_api_key")
async def get_secrets_tmdb_api_key():
    return {"tmdb_api_key": secrets.tmdb_api_key}
