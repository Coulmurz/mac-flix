"""TMDB API client for Mac Flix."""

import os
import requests

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

class TMDBClient:
    def __init__(self, api_key: str = TMDB_API_KEY):
        self.api_key = api_key

    def search(self, query: str, media_type: str = "movie"):
        """Search TMDB for movies or TV shows."""
        url = f"{TMDB_BASE_URL}/search/{media_type}"
        params = {"api_key": self.api_key, "query": query}
        resp = requests.get(url, params=params)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            try:
                error_json = resp.json()
                print(f"TMDB API error (search): {error_json.get('status_message')}")
            except Exception:
                print(f"TMDB API error (search): {resp.text}")
            raise e
        return resp.json().get("results", [])

    def get_details(self, tmdb_id: int, media_type: str = "movie"):
        """Get details for a movie or TV show by TMDB ID."""
        url = f"{TMDB_BASE_URL}/{media_type}/{tmdb_id}"
        params = {"api_key": self.api_key, "append_to_response": "videos,images"}
        resp = requests.get(url, params=params)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            try:
                error_json = resp.json()
                print(f"TMDB API error (get_details): {error_json.get('status_message')}")
            except Exception:
                print(f"TMDB API error (get_details): {resp.text}")
            raise e
        return resp.json()

    def get_poster_url(self, poster_path: str) -> str:
        """Get full URL for a poster image."""
        if poster_path:
            return f"{TMDB_IMAGE_BASE}{poster_path}"
        return ""

    def get_trailer_url(self, details: dict) -> str:
        """Extract YouTube trailer URL from details."""
        videos = details.get("videos", {}).get("results", [])
        for video in videos:
            if video.get("site") == "YouTube" and video.get("type") == "Trailer":
                return f"https://www.youtube.com/watch?v={video.get('key')}"
        return ""
