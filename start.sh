#!/usr/bin/env bash
# BrightFeed – start everything
# Usage:  ./start.sh          (normal start)
#         ./start.sh --seed   (force re-seed the database)
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND="$ROOT/backend"
FRONTEND="$ROOT/frontend"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()  { echo -e "${GREEN}[BrightFeed]${NC} $*"; }
warn()  { echo -e "${YELLOW}[BrightFeed]${NC} $*"; }
error() { echo -e "${RED}[BrightFeed]${NC} $*" >&2; }

# ── 1. PostgreSQL ────────────────────────────────────────────────────────────
info "Checking PostgreSQL..."
if ! pg_isready -q 2>/dev/null; then
    warn "PostgreSQL is not running. Attempting to start..."
    if sudo systemctl start postgresql 2>/dev/null; then
        sleep 1
    else
        error "Could not start PostgreSQL automatically."
        error "Run manually:  sudo systemctl start postgresql"
        exit 1
    fi
fi
info "PostgreSQL is ready ✓"

# ── 2. Python venv ───────────────────────────────────────────────────────────
if [ ! -d "$BACKEND/venv" ]; then
    info "Creating Python virtual environment..."
    python -m venv "$BACKEND/venv"
fi

info "Installing/updating backend dependencies..."
"$BACKEND/venv/bin/pip" install -r "$BACKEND/requirements.txt" -q

# ── 3. Frontend deps ─────────────────────────────────────────────────────────
if [ ! -d "$FRONTEND/node_modules" ]; then
    info "Installing frontend dependencies..."
    npm --prefix "$FRONTEND" install --silent
fi

# ── 4. Seed database ─────────────────────────────────────────────────────────
SEEDED_FLAG="$BACKEND/.seeded"
FORCE_SEED=false
[[ "${1:-}" == "--seed" ]] && FORCE_SEED=true

if [ "$FORCE_SEED" = true ] || [ ! -f "$SEEDED_FLAG" ]; then
    info "Seeding database..."
    # Ensure the DB exists
    sudo -u postgres createdb positivenews 2>/dev/null || true
    sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'password';" -q 2>/dev/null || true

    "$BACKEND/venv/bin/python" "$BACKEND/seed.py"
    touch "$SEEDED_FLAG"
    info "Database seeded ✓"
else
    info "Database already seeded (use --seed to re-seed)"
fi

# ── 5. Launch servers ────────────────────────────────────────────────────────
cleanup() {
    info "Shutting down..."
    kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

info "Starting FastAPI backend on http://localhost:8000 ..."
"$BACKEND/venv/bin/uvicorn" main:app --app-dir "$BACKEND" --reload --port 8000 &
BACKEND_PID=$!

info "Starting Vite frontend on http://localhost:5173 ..."
npm --prefix "$FRONTEND" run dev &
FRONTEND_PID=$!

echo ""
echo -e "  ${GREEN}✨ BrightFeed is running!${NC}"
echo    "  Frontend → http://localhost:5173"
echo    "  Backend  → http://localhost:8000"
echo    "  Press Ctrl+C to stop"
echo ""

wait
