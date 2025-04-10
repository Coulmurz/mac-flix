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

## Frontend (Streamlit)

The current frontend is a **Streamlit app** located in `app/frontend.py`. It features:

- A **mock-data-based home page** with 5 sample movies, each showing:
  - Poster image
  - Title, year, genres
  - Description
  - Rotten Tomatoes score
- A **single-tab navigation** with:
  - **View Details** button for each movie
  - **Back Home** and **Previous** buttons in the details view
- This is a **demo UI** using **hardcoded mock data** only.  
  Integration with the FastAPI backend API is planned for future versions.

### Running the Streamlit Frontend

From the project root, run:

\`\`\`bash
streamlit run app/frontend.py
\`\`\`

This will launch the My Flix home page in your browser.

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

## Setup (Outline)

1. **Clone the repo**
2. **Create and activate a Python 3.12+ virtual environment**
3. **Install dependencies** (managed via pip-tools)
4. **Create a `.env` file** with your API keys (see `.env.example`)
5. **Run FastAPI backend**
6. **Run Streamlit frontend**

### API Keys

- **OMDB:** Required. Get a free key at [http://www.omdbapi.com/apikey.aspx](http://www.omdbapi.com/apikey.aspx)
- **TMDB:** Deprecated, optional. If used, get a key at [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)

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
