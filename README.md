# HireMeAI — AI Portfolio Chatbot for HR

A candidate uploads their resume and profile once. HR can then chat with an AI assistant that
answers questions about the candidate (skills, projects, strengths, weaknesses, hobbies, goals…)
using **only** the data on file, and can score the candidate against any job description.

**Stack:** FastAPI · Groq (`openai/gpt-oss-120b`) · SQLAlchemy (SQLite or PostgreSQL) · Pydantic ·
pypdf / python-docx · streaming responses · vanilla HTML/JS frontend (served by FastAPI).

## Project layout
```
hiremeai/
├── backend/
│   ├── main.py      # API routes + serves the frontend
│   ├── llm.py       # Groq streaming chat + JSON-mode fit scoring
│   ├── parsing.py   # PDF / DOCX / TXT text extraction
│   └── db.py        # SQLAlchemy models (SQLite default)
├── frontend/index.html
├── .vscode/launch.json
├── requirements.txt
└── .env.example
```

## Run in VS Code (5 steps)
1. Open the `hiremeai` folder in VS Code (**File → Open Folder**).
2. Open a terminal (**Ctrl+`**) and create a virtual environment:
   - Windows: `python -m venv .venv` then `.venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and paste your Groq API key (free at https://console.groq.com/keys).
5. Start the server: `uvicorn backend.main:app --reload`
   (or press **F5** and pick "HireMeAI (FastAPI)").

Open **http://127.0.0.1:8000** →
- **Candidate Profile** tab: upload the resume, fill strengths / weaknesses / hobbies etc., Save.
- **HR Chat** tab: ask questions. Use the sidebar to score the candidate against a pasted JD.

API docs are at http://127.0.0.1:8000/docs.

## API
| Method | Path | Purpose |
|---|---|---|
| GET/PUT | `/api/candidate` | Read / save profile fields |
| POST | `/api/candidate/resume` | Upload PDF/DOCX/TXT resume (form field `file`) |
| POST | `/api/chat` | `{message, history}` → streamed text answer |
| POST | `/api/score` | form `job_description` (or `file`) → `{score, summary, strengths, gaps}` |
| GET | `/api/health` | Status + whether the API key is set |

## Use PostgreSQL instead of SQLite
`pip install psycopg2-binary`, then set in `.env`:
`DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/hiremeai`
Tables are created automatically on startup.

## Notes
- Scanned (image-only) PDFs have no extractable text; export a text-based PDF.
- The assistant is instructed never to invent facts and to ignore instructions hidden in resumes.
- The app holds a single candidate portfolio. To support many candidates, add a `slug` to the
  `Candidate` model and pass it in each route.
