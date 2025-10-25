# BookForge AI

Professional book generation tool (backend + Streamlit frontend).

Overview
- FastAPI backend (generates outlines and full book content, exports DOCX/PDF).
- Streamlit frontend (5-step workflow: Create Outline → Edit Outline → Generate Book → Edit Book → Export).
- Dark, minimal, responsive UI (mobile-friendly).

Quick start (Windows / PowerShell)
1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Start the backend (default port 8000):

```powershell
# from project root
uvicorn backend.main:app --reload --port 8000
```

4. Start the frontend (Streamlit, default port 8501):

```powershell
streamlit run frontend/app.py
```

5. Open the app in your browser: http://localhost:8501

Notes
- API URL can be overridden with the `BACKEND_URL` environment variable for the frontend.
- If you want Streamlit native theme matching, see `.streamlit/config.toml`.

Repository
- Remote: https://github.com/CrazAr374/aibook.git

License
- Add your license file if desired.
