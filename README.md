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
6. **Run Streamlit frontend**

Detailed setup instructions will be added as development progresses.

---

## Roadmap

- [x] Project scaffolding and documentation
- [ ] YAML config schemas
- [ ] FastAPI backend MVP
- [ ] Streamlit frontend MVP
- [ ] Basic streaming and download
- [ ] Trailer integration
- [ ] Testing suite
- [ ] Containerization with Podman
- [ ] Future: User accounts, adaptive streaming, recommendations

---

## License

TBD
