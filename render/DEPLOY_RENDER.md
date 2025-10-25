Render deployment notes
-----------------------

If Render is used to host the FastAPI backend, two recommended workflows are shown below.

1) Docker (recommended when packages require Rust/Cargo/maturin):

- Add the provided `Dockerfile` at the repository root (already included).
- In Render, create a new "Web Service" and choose the Docker option (it will use the Dockerfile).
- Set environment variables in Render (GEMINI_API_KEY, BACKEND_URL if needed).

2) Native build on Render (non-Docker):

- Use these Build/Start commands in Render's service form:

  Build Command:
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

  Start Command:
  ```bash
  gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT --workers 1
  ```

- If a dependency requires Rust/Cargo (maturin), the native build may fail on Render's default environment due to read-only locations. In that case use the Docker approach above, or install Rust in the Build Command by setting writable CARGO_HOME and RUSTUP_HOME and running the rustup installer (more complex).

Security note: remove `.env` from the repository and set secrets in Render's Environment variables.
