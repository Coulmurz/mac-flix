# Mac Flix

**Mac Flix** is a modular, config-driven app for browsing, streaming, and downloading movies and TV shows, inspired by Netflix and Google Movies.

---

## Features

- Browse movies and TV shows categorized by type and genre
- View metadata: title, poster, year, genre, description, rating, trailer link
- Filter content with an intuitive filter bar
- Watch trailers via embedded YouTube player
- Stream or download video files
- User accounts and watchlists (planned)
- Adaptive streaming (HLS/DASH) (planned)
- Cloud storage integration (planned)
- Advanced search and scraping (planned)
- Vector memory and agentic workflows (planned)
- Multi-user access controls (planned)
- Modern React/Vue frontend (planned)
- Enhanced security and access management (planned)
- Config-driven content catalog and UI
- Built with **FastAPI** (backend) and **Streamlit** (prototype frontend)
- Containerized with **Podman** for portability

---

## Architecture Overview

- **Backend:** FastAPI serving metadata, streaming, download, user, and search endpoints
- **Frontend:** Streamlit UI (prototype), migrating to React/Vue
- **Configs:** YAML files validated with Pydantic models
- **Storage:** Local filesystem (MVP), expandable to cloud storage
- **Testing:** Pytest for unit and integration tests
- **Containerization:** Podman with Dockerfile and Compose

---

## Frontend

Currently a **Streamlit app** (`app/frontend.py`) featuring:

- Mock-data-based home page with sample movies
- Details page with metadata and trailer
- Navigation with home/details views

### Planned Frontend

- Full React or Vue SPA
- User authentication and watchlists
- Adaptive streaming player
- Advanced search and recommendations

---

## API Endpoints

| Endpoint                   | Method | Description                                         |
|----------------------------|--------|-----------------------------------------------------|
| `/`                        | GET    | Welcome message                                     |
| `/content`                 | GET    | List all movies and TV shows                        |
| `/content/{id}`            | GET    | Get metadata for a specific content                 |
| `/categories`              | GET    | List categories and filters                         |
| `/omdb/search?title=TITLE` | GET    | Search movies by title using OMDB API               |
| `/tmdb/search`             | GET    | (Deprecated) Search TMDB for movies or TV shows     |

All responses are JSON and validated with Pydantic models.

---

## Setup

1. **Clone the repo**
2. **Create a Python 3.12+ virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** with your API keys (see `.env.example`)
5. **Build and run with Podman**

```bash
podman-compose build
podman-compose up
```

6. Access:

- FastAPI docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Streamlit UI: [http://localhost:8501](http://localhost:8501)

---

## API Keys

- **OMDB:** Required. Get a free key at [http://www.omdbapi.com/apikey.aspx](http://www.omdbapi.com/apikey.aspx)
- **TMDB:** Deprecated, optional. If used, get a key at [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)

---

## Roadmap

- [x] Project scaffolding and documentation
- [x] YAML config schemas
- [x] FastAPI backend MVP
- [x] Streamlit frontend MVP
- [x] Basic streaming and download
- [x] Trailer integration
- [x] Testing suite
- [x] Containerization with Podman
- [ ] User accounts & watchlists
- [ ] Adaptive streaming (HLS/DASH)
- [ ] Cloud storage integration
- [ ] Advanced search and scraping
- [ ] Vector memory and agentic workflows
- [ ] Multi-user access controls
- [ ] Replace Streamlit with React/Vue frontend
- [ ] Enhanced security and access management

---

## Config Files

| Config File                   | Purpose                                         |
|------------------------------|-------------------------------------------------|
| `app/config/content.yaml`    | Content catalog: movies, TV shows, metadata     |
| `app/config/categories.yaml` | UI categories and filters                       |
| `app/config/secrets.yaml`    | API keys and secrets                            |

See [Config Schema Design](app/config/SCHEMA_DESIGN.md) for detailed schema documentation.

---

## License

TBD
