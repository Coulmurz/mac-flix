# Mac Flix

**Mac Flix** is a modular, config-driven MVP app for browsing, streaming, and downloading movies and TV shows, inspired by Netflix and Google Movies.

---

## Features (MVP)

- Browse movies and TV shows categorized by type and genre
- View metadata: title, poster, year, genre, description, rating, trailer link
- Filter content with an intuitive filter bar
- Watch trailers via embedded YouTube player
- Stream or download video files
- Config-driven content catalog and UI
- Built with **FastAPI** (backend) and **Streamlit** (frontend)
- Containerized with **Podman** for portability

---

## Architecture Overview

- **Backend:** FastAPI serving metadata, streaming, and download endpoints
- **Frontend:** Streamlit UI with embedded video and trailer players
- **Configs:** YAML files validated with Pydantic models
- **Storage:** Local filesystem (MVP), expandable to cloud
- **Testing:** Pytest for unit and integration tests

---

## Setup (Outline)

1. **Clone the repo**
2. **Create and activate a Python 3.12+ virtual environment**
3. **Install dependencies** (managed via pip-tools)
4. **Configure content and API keys in YAML files**
5. **Run FastAPI backend**
   ```bash
   python app/main.py
   ```
6. **Run Streamlit frontend**
   ```bash
   streamlit run app/streamlit_app.py
   ```
7. **Run tests**
   ```bash
   pytest tests/
   ```

---

## Roadmap

- [x] Project scaffolding and documentation
- [x] YAML config schemas
- [x] FastAPI backend MVP
  - Serves content, categories, and secrets via API endpoints
- [x] Streamlit frontend MVP
  - Fetches and displays content from the FastAPI backend
- [x] Trailer integration
  - Embedded YouTube player for trailers
- [x] Basic streaming and download
  - Stream and download movies and TV episodes
  - Support for both local files and remote URLs
- [x] Testing suite
  - Unit tests for models and config loading
  - Integration tests for API endpoints
  - Utility test helpers for Streamlit app
- [ ] Containerization with Podman
- [ ] Future: User accounts, adaptive streaming, recommendations

---

## Config Files

All domain logic and content metadata are externalized into YAML files:

| Config File                   | Purpose                                         |
|------------------------------|-------------------------------------------------|
| `app/config/content.yaml`    | Content catalog: movies, TV shows, metadata     |
| `app/config/categories.yaml` | UI categories and filters                       |
| `app/config/secrets.yaml`    | API keys and secrets                            |

See [Config Schema Design](app/config/SCHEMA_DESIGN.md) for detailed schema documentation.

Update these files to customize content, filters, and API keys.

---

## API Endpoints

The FastAPI backend provides the following endpoints:

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

## Testing

The project includes a comprehensive test suite using pytest:

- **Model tests:** Validation of data models and YAML configuration loading
- **API tests:** Verification of all API endpoints functionality
- **Utility tests:** Helper functions for the Streamlit frontend

To run the tests:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v tests/
```

---

## License

TBD
