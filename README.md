# BrightFeed ☀️

> A full-stack positive news feed — because the world has good news too.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-yellow.svg)
![React](https://img.shields.io/badge/react-18-61DAFB.svg)

---

## ✨ Features

- 📰 Curated positive news articles across 7 categories
- 🔍 Live debounced search
- 😊 Emoji reaction system with optimistic UI updates
- 🔖 Save/bookmark articles
- 🎨 Warm amber gradient design with smooth animations
- ⚡ FastAPI async backend + React 18 + TypeScript frontend

---

## 🚀 Quick Start

```bash
git clone https://github.com/PioBisleri/positive_news_feed.git
cd positive_news_feed
./start.sh
```

Open **<http://localhost:5173>** 🌟

> The script handles everything: starts PostgreSQL, creates a venv, installs deps, seeds the DB (first run only), and launches both servers.

**Options:**

```bash
./start.sh           # normal start (skips seed if already done)
./start.sh --seed    # force re-seed the database
```

---

## 🗂️ Project Structure

```
positive_news_feed/
├── backend/
│   ├── main.py          # FastAPI app + CORS
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic v2 schemas
│   ├── crud.py          # Async CRUD operations
│   ├── database.py      # Async engine + session
│   ├── seed.py          # DB seeder (7 categories, 16 articles)
│   ├── routers/
│   │   ├── articles.py  # /api/articles endpoints
│   │   └── categories.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── api/         # Axios client
│       ├── components/  # Navbar, NewsCard, ReactionBar, …
│       ├── pages/       # Home, Article, Saved
│       └── types/       # TypeScript interfaces
├── start.sh             # One-command launcher
├── LICENSE
└── README.md
```

---

## 🛠️ Manual Setup

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL 15+

### First-time PostgreSQL setup (Arch Linux)

```bash
sudo su -l postgres -c "initdb --locale=C.UTF-8 --encoding=UTF8 -D '/var/lib/postgres/data'"
sudo systemctl start postgresql
sudo -u postgres createdb positivenews
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'password';"
```

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/articles` | List articles (filter: `category`, `search`, `featured`) |
| `GET` | `/api/articles/saved` | Get saved articles |
| `GET` | `/api/articles/{id}` | Get single article |
| `POST` | `/api/articles` | Create article |
| `POST` | `/api/articles/{id}/save` | Toggle save status |
| `POST` | `/api/articles/{id}/react` | Add reaction |
| `GET` | `/api/categories` | List all categories |
| `GET` | `/` | Health check |

---

## 🧰 Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | React 18 · TypeScript · Vite · Tailwind CSS |
| Backend | FastAPI · SQLAlchemy 2 (async) · Pydantic v2 |
| Database | PostgreSQL · asyncpg |
| Tooling | Alembic · Axios · React Router |

---

## 📄 License

[MIT](LICENSE) © 2026 Veer
