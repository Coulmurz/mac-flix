from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import StreamingResponse, FileResponse
import yaml
from pydantic import BaseModel
from typing import List, Dict
import logging
import os
import mimetypes
import requests
from urllib.parse import urlparse

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
    seasons: List["Season"] = []

class Season(BaseModel):
    season_number: int
    episodes: List["Episode"]

class Episode(BaseModel):
    episode_number: int
    title: str
    description: str
    poster_url: str

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

def create_content_objects(content_config):
    content_objects = []
    for key in ["movies", "tv_shows"]:
        if key in content_config:
            for item in content_config[key]:
                if "seasons" in item:
                    seasons = []
                    for season_data in item["seasons"]:
                        episodes = [Episode(**episode_data) for episode_data in season_data["episodes"]]
                        season = Season(season_number=season_data["season_number"], episodes=episodes)
                        seasons.append(season)
                    item["seasons"] = seasons
                content_objects.append(Content(**item))
    return content_objects

content = create_content_objects(content_config)
print(content)
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

def get_content_by_id(content_id: str):
    """Helper function to find content by ID"""
    for content_item in content:
        if content_item.id == content_id:
            return content_item
    return None

def is_url(url: str) -> bool:
    """Check if a string is a URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

async def stream_remote_video(url: str):
    """Stream a video from a remote URL"""
    async def iterfile():
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=8192):
                    yield chunk
        except Exception as e:
            logging.error(f"Error streaming from URL {url}: {e}")
            raise HTTPException(status_code=500, detail=f"Error streaming video: {str(e)}")
    
    return iterfile()

@app.get("/stream/{content_id}")
async def stream_video(content_id: str):
    """Stream a video by content ID"""
    content_item = get_content_by_id(content_id)
    if not content_item:
        raise HTTPException(status_code=404, detail="Content not found")
    
    video_url = content_item.video_url
    
    if not video_url:
        raise HTTPException(status_code=404, detail="Video URL not found for this content")
    
    # Handle remote URLs (http, https)
    if is_url(video_url):
        try:
            # Get content type for remote URL
            head_response = requests.head(video_url)
            content_type = head_response.headers.get('Content-Type', 'video/mp4')
            
            # Stream the remote video
            iterator = await stream_remote_video(video_url)
            return StreamingResponse(iterator, media_type=content_type)
        except Exception as e:
            logging.error(f"Error processing remote video URL {video_url}: {e}")
            raise HTTPException(status_code=500, detail=f"Error streaming video: {str(e)}")
    
    # Handle local files
    else:
        # Check if the file exists
        if not os.path.isfile(video_url):
            raise HTTPException(status_code=404, detail="Video file not found")
        
        # Get content type based on file extension
        content_type, _ = mimetypes.guess_type(video_url)
        if not content_type:
            content_type = 'video/mp4'  # Default to mp4 if type can't be determined
        
        # Return the file as a streaming response
        return StreamingResponse(open(video_url, mode="rb"), media_type=content_type)

@app.get("/download/{content_id}")
async def download_video(content_id: str):
    """Download a video by content ID"""
    content_item = get_content_by_id(content_id)
    if not content_item:
        raise HTTPException(status_code=404, detail="Content not found")
    
    download_url = content_item.download_url
    
    if not download_url:
        raise HTTPException(status_code=404, detail="Download URL not found for this content")
    
    # Handle remote URLs (http, https)
    if is_url(download_url):
        try:
            # For external URLs, we'll create a redirect response
            return {"redirect_url": download_url}
        except Exception as e:
            logging.error(f"Error processing remote download URL {download_url}: {e}")
            raise HTTPException(status_code=500, detail=f"Error setting up download: {str(e)}")
    
    # Handle local files
    else:
        # Check if the file exists
        if not os.path.isfile(download_url):
            raise HTTPException(status_code=404, detail="Download file not found")
        
        # Get the filename from the path
        filename = os.path.basename(download_url)
        
        # Return the file as a download
        return FileResponse(
            path=download_url,
            filename=filename,
            media_type='application/octet-stream'
        )

@app.get("/stream/episode/{content_id}/{season_number}/{episode_number}")
async def stream_episode(content_id: str, season_number: int, episode_number: int):
    """Stream a specific episode of a TV series"""
    content_item = get_content_by_id(content_id)
    if not content_item or content_item.type != "tv":
        raise HTTPException(status_code=404, detail="TV content not found")
    
    # Find the specified season
    season = None
    for s in content_item.seasons:
        if s.season_number == season_number:
            season = s
            break
    
    if not season:
        raise HTTPException(status_code=404, detail=f"Season {season_number} not found")
    
    # Find the specified episode
    episode = None
    for e in season.episodes:
        if e.episode_number == episode_number:
            episode = e
            break
    
    if not episode:
        raise HTTPException(status_code=404, detail=f"Episode {episode_number} not found in Season {season_number}")
    
    # If episode has video_url attribute, use it; otherwise use series video_url
    video_url = getattr(episode, 'video_url', content_item.video_url)
    
    if not video_url:
        raise HTTPException(status_code=404, detail="Video URL not found for this episode")
    
    # Handle streaming similar to the main stream_video function
    if is_url(video_url):
        try:
            head_response = requests.head(video_url)
            content_type = head_response.headers.get('Content-Type', 'video/mp4')
            iterator = await stream_remote_video(video_url)
            return StreamingResponse(iterator, media_type=content_type)
        except Exception as e:
            logging.error(f"Error processing remote video URL {video_url}: {e}")
            raise HTTPException(status_code=500, detail=f"Error streaming video: {str(e)}")
    else:
        if not os.path.isfile(video_url):
            raise HTTPException(status_code=404, detail="Video file not found")
        content_type, _ = mimetypes.guess_type(video_url)
        if not content_type:
            content_type = 'video/mp4'
        return StreamingResponse(open(video_url, mode="rb"), media_type=content_type)
