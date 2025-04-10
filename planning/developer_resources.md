
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

## Frontend (Streamlit)

- The **Streamlit frontend** is located at `app/frontend.py`.
- It currently uses **mock data** with 5 sample movies for demo purposes.
- To run the frontend:

\`\`\`bash
streamlit run app/frontend.py
\`\`\`

- Backend API integration is planned for future versions.

---

## Planned MCP Servers (Future)

- **Brave Search:** Web search, news, articles
- **FireCrawl:** Web scraping, crawling
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

_Last updated: 2025-04-09 14:11 EDT_
