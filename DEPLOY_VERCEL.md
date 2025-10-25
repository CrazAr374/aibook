Vercel deployment notes — ignore backend
--------------------------------------

If you're using Vercel for a frontend-only deployment, prevent Vercel from trying to build your FastAPI backend (which causes large serverless functions or build errors).

What I added:
- `.vercelignore` — placed at repo root to exclude `backend/`, `Dockerfile`, `.env`, `render/`, and other build artifacts.

Recommended workflows:
1) Frontend on Vercel, backend elsewhere (recommended)
 - Keep your Streamlit app local or host it on Streamlit Cloud / Render (as a separate service). Vercel is not ideal for Streamlit or heavyweight Python backends.
 - Vercel can host static assets or a lightweight Next.js/React frontend. If you want a web UI on Vercel, separate it from the FastAPI backend and configure the frontend to call the backend URL.

2) If you want Vercel to host only static pieces:
 - Ensure `.vercelignore` excludes the backend and other non-frontend files (already added).

3) If you previously tried to deploy the backend to Vercel and received function-size errors:
 - Remove backend from Vercel deploy by adding `.vercelignore` as done here.
 - Deploy the backend to Render (Docker), Railway, Cloud Run, or another platform that supports Python server apps.

Next steps for you (pick one):
- Use Render Docker (recommended): see `Dockerfile` and the `render` docs in the repo.
- Use native Render build: set the Build Command to `bash render/render_build.sh` (script added) and Start Command to `gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT --workers 1`.
