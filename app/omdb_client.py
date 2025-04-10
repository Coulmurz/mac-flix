"""OMDB API client for Mac Flix."""

import os
import requests

OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")
OMDB_BASE_URL = "http://www.omdbapi.com/"

class OMDBClient:
    def __init__(self, api_key: str = OMDB_API_KEY):
        self.api_key = api_key

    def search(self, title: str):
        """Search OMDB for movies by title."""
        params = {"apikey": self.api_key, "s": title}
        resp = requests.get(OMDB_BASE_URL, params=params)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            try:
                print(f"OMDB API error (search): {resp.json().get('Error')}")
            except Exception:
                print(f"OMDB API error (search): {resp.text}")
            raise e
        data = resp.json()
        if data.get("Response") == "False":
            print(f"OMDB API error (search): {data.get('Error')}")
            return []
        return data.get("Search", [])

    def get_details(self, imdb_id: str):
        """Get OMDB details by IMDb ID."""
        params = {"apikey": self.api_key, "i": imdb_id, "plot": "full"}
        resp = requests.get(OMDB_BASE_URL, params=params)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            try:
                print(f"OMDB API error (get_details): {resp.json().get('Error')}")
            except Exception:
                print(f"OMDB API error (get_details): {resp.text}")
            raise e
        data = resp.json()
        if data.get("Response") == "False":
            print(f"OMDB API error (get_details): {data.get('Error')}")
            return {}
        return data
