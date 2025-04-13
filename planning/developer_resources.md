# Mac Flix — Developer Resources

---

## Core Libraries & Frameworks

- **FastAPI:** https://fastapi.tiangolo.com/
- **Streamlit:** https://streamlit.io/
- **Pydantic:** https://docs.pydantic.dev/
- **Pytest:** https://docs.pytest.org/
- **pip-tools:** https://pip-tools.readthedocs.io/
- **Podman:** https://podman.io/

---

## APIs & Data Sources

- **TMDB API (The Movie Database):** https://developers.themoviedb.org/3
  - Metadata, posters, trailers
  - Requires API key (store securely in `.env`)
- **IMDb API (optional):** https://imdb-api.com/
- **OMDb API (optional):** https://www.omdbapi.com/

---

## Secrets Management

- **.env File:** All secrets (API keys, etc.) MUST be stored in a `.env` file at the project root.
- **.gitignore:** The `.env` file is included in `.gitignore` and MUST NOT be committed to version control.
- **Current Secrets:**
  - `FIRECRAWL_API_KEY`: Used for the FireCrawl MCP server.

---

## Project Status (Current Features)

- **FastAPI Backend MVP:**
  - Content metadata endpoints
  - Category and filter endpoints
  - Authentication/secrets endpoints
  - Video streaming endpoints (both local and remote)
  - File download endpoints (both local and remote)
  - Episode-specific streaming for TV series
  
- **Streamlit Frontend MVP:**
  - Movie browsing with filters
  - TV show browsing with season/episode navigation
  - Metadata display (title, year, rating, description, cast)
  - Trailer playback via embedded YouTube player
  - Stream/download links for movies and TV episodes
  - Session state management for persistent UI state

- **Testing Suite:**
  - Comprehensive test fixtures
  - Unit tests for models and config loading
  - API endpoint integration tests
  - Utility tests for frontend functionality
  - Mocking for external dependencies

- **Next Up:**
  - Containerize with Podman

---

## API Endpoints

| Endpoint                                | Method | Description                                    |
|----------------------------------------|--------|------------------------------------------------|
| `/content`                              | GET    | Get all content items                          |
| `/categories`                           | GET    | Get all categories                             |
| `/content/{category_name}`              | GET    | Get content filtered by category               |
| `/content/year/{year}`                  | GET    | Get content filtered by year                   |
| `/stream/{content_id}`                  | GET    | Stream a movie or TV show                      |
| `/download/{content_id}`                | GET    | Download a movie or TV show                    |
| `/stream/episode/{content_id}/{season}/{episode}` | GET | Stream a specific episode of a TV show |

---

## Test Suite Structure

- **conftest.py:** Common fixtures and test setup
- **test_models.py:** Tests for Pydantic models and YAML loading
- **test_api.py:** Tests for FastAPI endpoints
- **test_streamlit_utils.py:** Tests for frontend utility functions

Run tests with:
```bash
# Run all tests
pytest tests/

# Run with coverage reporting
pytest --cov=app tests/
```

---

## Containerization

- **Podman Documentation:** https://docs.podman.io/
- Use `python:3.12-slim` as base image
- Pass secrets via environment variables
- Exclude unnecessary files with `.dockerignore`

---

## Testing

- **Pytest:** unit and integration tests
- **Fixtures:** for YAML configs and API responses
- **Coverage:** ensure core logic is well-tested
- **Test cases implemented:**
  - Content loading from YAML
  - Pydantic model validation
  - API endpoint responses
  - Stream/download functionality
  - Error handling
  - Frontend utility functions

---

## Installed MCP Servers

- **FireCrawl:** Web scraping, crawling, extraction
  - *Capabilities:* Scrape websites, extract structured data.
  - *API Key:* Stored in `.env` as `FIRECRAWL_API_KEY`.
  - *Docs:* [Insert FireCrawl MCP Server Docs Link Here if available]

## Planned MCP Servers (Future)

- **Brave Search:** Web search, news, articles
- **Qdrant:** Vector memory, semantic search
- **File System:** Local file management
- **GitHub:** Repo management, code search

---

## Config & Schema

- **YAML Config Files:**
  - [`app/config/content.yaml`](../app/config/content.yaml) — Content catalog (movies, shows, metadata)
  - [`app/config/categories.yaml`](../app/config/categories.yaml) — UI categories and filters
  - [`app/config/secrets.yaml`](../app/config/secrets.yaml) — API keys and secrets

- **Schema Documentation:**
  - [`app/config/SCHEMA_DESIGN.md`](../app/config/SCHEMA_DESIGN.md) — Detailed schema design for all configs

- **Validation:**
  - All YAML configs are **validated with Pydantic models** at startup.
  - Invalid configs will raise errors to prevent runtime issues.

---

_Last updated: 2025-04-13 19:56 EDT_
