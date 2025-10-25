Render deployment notes (updated)
--------------------------------

If Render is used to host the FastAPI backend, two recommended workflows are shown below.

1) Docker (recommended when packages require Rust/Cargo/maturin):

- Add the provided `Dockerfile` at the repository root (already included).
- In Render, create a new "Web Service" and choose the Docker option (it will use the Dockerfile).
- Set environment variables in Render (GEMINI_API_KEY, BACKEND_URL if needed).

2) Native build on Render (non-Docker):

- Use the helper script `render/render_build.sh` as the Build Command. This installs a local Rust toolchain into writable directories before pip runs so maturin/Cargo-backed wheels can be built in Render's build environment.

  Build Command (native route):
  ```bash
  bash render/render_build.sh
  ```

  Start Command:
  ```bash
  gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT --workers 1
  ```

- If you still encounter build errors on native Render, fall back to the Docker approach above (recommended).

Security note: remove `.env` from the repository and set secrets in Render's Environment variables. Rotate any exposed API keys immediately.

Further notes:
- The provided `Dockerfile` already installs Rust and system build deps inside the image so maturin/cargo builds succeed.
