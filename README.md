# BrightFeed 🌟 — Positive News Feed

A full-stack web app that surfaces uplifting, positive news stories. Browse by category, search headlines, save favorites, and react to stories that inspire you.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + TypeScript, Tailwind CSS 3, Vite |
| Backend | Python 3.11+, FastAPI, SQLAlchemy 2 (async) |
| Database | PostgreSQL |
| HTTP | Axios (frontend), asyncpg (backend driver) |

---

## Project Structure

```
positive-news-feed/
├── backend/
│   ├── main.py          # FastAPI app + CORS
│   ├── database.py      # Async engine + session
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic v2 schemas
│   ├── crud.py          # Async DB operations
│   ├── routers/
│   │   ├── articles.py  # Article endpoints
│   │   ├── categories.py
│   │   └── reactions.py
│   ├── seed.py          # Database seeder
│   ├── requirements.txt
│   └── .env
└── frontend/
    ├── src/
    │   ├── api/client.ts      # Axios API functions
    │   ├── types/index.ts     # TypeScript interfaces
    │   ├── components/        # Navbar, NewsCard, ReactionBar, etc.
    │   └── pages/             # Home, Article, Saved
    ├── vite.config.ts
    └── tailwind.config.js
```

---

## Setup Instructions

### 1. PostgreSQL Database

```bash
# Create the database
psql -U postgres -c "CREATE DATABASE positivenews;"
```

> **Default credentials**: `postgres` / `password` on `localhost:5432`  
> To use different credentials, edit `backend/.env`:
>
> ```
> DATABASE_URL=postgresql://YOUR_USER:YOUR_PASSWORD@localhost:5432/positivenews
> ```

---

### 2. Backend

```bash
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn main:app --reload --port 8000
```

The API will be available at **<http://localhost:8000>**

Health check: `curl http://localhost:8000/` → `{"status":"ok"}`

---

### 3. Seed the Database

With the backend dependencies installed and the database created:

```bash
cd backend
python seed.py
```

This will:

- Create the `categories`, `articles`, and `reactions` tables
- Insert **7 categories** (Science, Environment, Community, Health, Animals, Technology, Arts & Culture)
- Insert **16 positive news articles** with full content, realistic authors, and sources
- Insert **4 reaction rows per article** with random counts (10–500)

---

### 4. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The app will be available at **<http://localhost:5173>**

The Vite dev server proxies all `/api/*` requests to the FastAPI backend at `http://localhost:8000`.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/api/articles` | List articles (`?category=&search=&featured=`) |
| `GET` | `/api/articles/saved` | List saved articles |
| `GET` | `/api/articles/{id}` | Get article detail |
| `POST` | `/api/articles` | Create article |
| `PATCH` | `/api/articles/{id}/save` | Toggle saved status |
| `POST` | `/api/articles/{id}/react` | Increment a reaction `{"reaction_type": "inspiring"}` |
| `GET` | `/api/categories` | List categories |

---

## Features

- 🔍 **Search** — debounced real-time headline search
- 🏷️ **Category filters** — horizontal scrollable pill buttons
- ⭐ **Featured articles** — displayed in a larger hero layout
- 🔖 **Save articles** — bookmark stories to read later
- 🌟🤗🎉🌱 **Reactions** — optimistic UI updates with bounce animation
- 📱 **Responsive** — 1-col mobile → 2-col tablet → 3-col desktop
- 🎨 **Loading skeletons** — smooth shimmer while data loads
