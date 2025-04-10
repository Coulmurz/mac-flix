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

## API Endpoints

| Endpoint             | Method | Description                          |
|----------------------|--------|--------------------------------------|
| `/`                  | GET    | Welcome message                      |
| `/content`           | GET    | List all movies and TV shows         |
| `/content/{id}`      | GET    | Get metadata for a specific content  |
| `/categories`        | GET    | List categories and filters          |

All responses are JSON and validated with Pydantic models.

---

## Setup (Outline)

1. **Clone the repo**
2. **Create and activate a Python 3.12+ virtual environment**
3. **Install dependencies** (managed via pip-tools)
4. **Configure content and API keys in YAML files**
5. **Run FastAPI backend**
6. **Run Streamlit frontend**

Detailed setup instructions will be added as development progresses.

---

## Roadmap

- [x] Project scaffolding and documentation
- [x] YAML config schemas
- [ ] FastAPI backend MVP
- [ ] Streamlit frontend MVP
- [ ] Basic streaming and download
- [ ] Trailer integration
- [ ] Testing suite
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

## License

TBD
