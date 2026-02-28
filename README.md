# BrightFeed ☀️

> A full-stack positive news feed — because the world has good news too.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-yellow.svg)
![React](https://img.shields.io/badge/react-18-61DAFB.svg)

---

## ✨ Features

- 📰 Curated positive news articles across 7 categories
- 🔍 Live debounced search
- � Save / bookmark articles
- 🌐 Live news via [NewsAPI](https://newsapi.org) (optional)
- 🎨 Warm amber gradient design with smooth animations
- ⚡ FastAPI async backend + React 18 + TypeScript frontend

---

## ️ Project Structure

```
positive_news_feed/
├── backend/
│   ├── main.py          # FastAPI app + CORS
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic v2 schemas
│   ├── crud.py          # Async CRUD operations
│   ├── database.py      # Async engine + session
│   ├── config.py        # Settings (reads .env)
│   ├── seed.py          # DB seeder (categories)
│   ├── fetcher.py       # NewsAPI article fetcher
│   ├── routers/
│   │   ├── articles.py  # /api/articles endpoints
│   │   └── categories.py
│   ├── .env             # Your secrets (gitignored)
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── api/         # Axios client
│       ├── components/  # Navbar, NewsCard, …
│       ├── pages/       # Home, Article, Saved
│       └── types/       # TypeScript interfaces
├── LICENSE
└── README.md
```

---

## � Setup

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL 15+

### 1 · PostgreSQL (first time, Arch Linux)

```bash
sudo su -l postgres -c "initdb --locale=C.UTF-8 --encoding=UTF8 -D '/var/lib/postgres/data'"
sudo systemctl start postgresql
sudo -u postgres createdb positivenews
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'password';"
```

### 2 · Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/positivenews
NEWS_API_KEY=your_key_here   # optional – get one at https://newsapi.org/register
```

Seed the database and start the server:

```bash
python seed.py
uvicorn main:app --reload --port 8000
```

### 3 · Frontend

```bash
cd frontend
npm install
npm run dev
```

Open **<http://localhost:5173>** 🌟

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/articles` | List articles (filter: `category`, `search`, `featured`) |
| `GET` | `/api/articles/saved` | Get saved articles |
| `GET` | `/api/articles/{id}` | Get single article |
| `POST` | `/api/articles/{id}/save` | Toggle save status |
| `GET` | `/api/categories` | List all categories |
| `GET` | `/` | Health check |

---

## 🧰 Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | React 18 · TypeScript · Vite |
| Backend | FastAPI · SQLAlchemy 2 (async) · Pydantic v2 |
| Database | PostgreSQL · asyncpg |
| Tooling | Axios · React Router · APScheduler |

---

## 📄 License

[MIT](LICENSE) © 2026 Veer
