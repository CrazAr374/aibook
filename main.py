# Root-level FastAPI entrypoint for Vercel
from backend.main import app

# Expose `app` for ASGI servers
__all__ = ["app"]
