# Mac Flix — Config Schema Design

---

## Overview

All domain logic and settings are **externalized into YAML configs**, validated with Pydantic models.

---

## 1. Content Catalog Schema (`content.yaml`)

| Field           | Type            | Description                                  | Required |
|-----------------|-----------------|----------------------------------------------|----------|
| `id`            | string          | Unique identifier (slug or UUID)             | Yes      |
| `title`         | string          | Movie/show title                             | Yes      |
| `type`          | enum            | `movie` or `tv`                             | Yes      |
| `year`          | int             | Release year                                | Yes      |
| `genres`        | list[string]    | Genres (e.g., Action, Drama)                | Yes      |
| `description`   | string          | Short description or tagline                | Yes      |
| `rating`        | float           | Rating (e.g., IMDb score)                   | No       |
| `poster_url`    | string (URL)    | Poster image URL                            | Yes      |
| `trailer_url`   | string (URL)    | Trailer video URL (YouTube, etc.)           | No       |
| `cast`          | list[string]    | Main actors                                 | No       |
| `director`      | string          | Director name                               | No       |
| `duration`      | int (minutes)   | Duration                                   | No       |
| `language`      | string          | Language                                   | No       |
| `video_url`     | string (URL)    | Streaming video URL                        | Yes (MVP)|
| `download_url`  | string (URL)    | Download link                              | No       |

---

## 2. Categories & Filters Schema (`categories.yaml`)

| Field           | Type            | Description                                  | Required |
|-----------------|-----------------|----------------------------------------------|----------|
| `categories`    | list[Category]  | List of categories                          | Yes      |

**Category Object:**

| Field        | Type          | Description                     | Required |
|--------------|---------------|---------------------------------|----------|
| `name`       | string        | Category name (e.g., New, Top)  | Yes      |
| `filters`    | list[Filter]  | Filters within this category    | No       |

**Filter Object:**

| Field        | Type          | Description                     | Required |
|--------------|---------------|---------------------------------|----------|
| `name`       | string        | Filter name (e.g., Action)      | Yes      |
| `type`       | enum          | `genre`, `year`, `rating`       | Yes      |
| `value`      | string/int/float| Filter value                  | Yes      |

---

## 3. API Keys & Secrets Schema (`secrets.yaml`)

| Field           | Type            | Description                                  | Required |
|-----------------|-----------------|----------------------------------------------|----------|
| `tmdb_api_key`  | string          | TMDB API key                                | Yes      |
| `other_api_keys`| dict            | Other API keys (IMDb, OMDb)                 | No       |

---

## Validation

- All configs are **validated with Pydantic models** before use.
- Invalid configs will **raise errors at startup**.

---

_Last updated: 2025-04-09_
