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

---

## Planned MCP Servers (Future)

- **Brave Search:** Web search, news, articles
- **FireCrawl:** Web scraping, crawling
- **Qdrant:** Vector memory, semantic search
- **File System:** Local file management
- **GitHub:** Repo management, code search

_Update this file as new tools, APIs, or servers are integrated._

---

_Last updated: 2025-04-09_
