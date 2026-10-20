"""HireMeAI — FastAPI backend. Run:  uvicorn backend.main:app --reload"""
import json
from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import llm
from .db import get_candidate, get_db
from .parsing import extract_text

FIELDS = ["about", "skills", "strengths", "weaknesses", "hobbies", "goals", "extra"]
LABELS = {
    "about": "About / summary", "skills": "Skills", "strengths": "Strengths",
    "weaknesses": "Weaknesses / areas to improve", "hobbies": "Hobbies & interests",
    "goals": "Career goals", "extra": "Other details (availability, location, etc.)",
}
MAX_UPLOAD = 5 * 1024 * 1024

app = FastAPI(title="HireMeAI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class ProfileIn(BaseModel):
    name: str = ""
    headline: str = ""
    about: str = ""
    skills: str = ""
    strengths: str = ""
    weaknesses: str = ""
    hobbies: str = ""
    goals: str = ""
    extra: str = ""


class ChatIn(BaseModel):
    message: str
    history: list[dict] = []


def build_context(c) -> str:
    prof = json.loads(c.profile or "{}")
    parts = [f"Name: {c.name or 'not provided'}", f"Headline: {c.headline or 'not provided'}"]
    for f in FIELDS:
        parts.append(f"{LABELS[f]}: {prof.get(f) or 'not provided'}")
    parts.append("\n--- RESUME TEXT ---\n" + (c.resume_text[:20000] or "no resume uploaded"))
    return "\n".join(parts)


def candidate_dict(c) -> dict:
    prof = json.loads(c.profile or "{}")
    return {
        "name": c.name or "", "headline": c.headline or "",
        **{f: prof.get(f, "") for f in FIELDS},
        "has_resume": bool(c.resume_text), "resume_filename": c.resume_filename or "",
        "resume_chars": len(c.resume_text or ""), "llm_ready": llm.llm_ready(),
    }


@app.get("/api/health")
def health():
    return {"ok": True, "llm_ready": llm.llm_ready(), "model": llm.MODEL}


@app.get("/api/candidate")
def read_candidate(db=Depends(get_db)):
    return candidate_dict(get_candidate(db))


@app.put("/api/candidate")
def save_candidate(body: ProfileIn, db=Depends(get_db)):
    c = get_candidate(db)
    c.name, c.headline = body.name.strip()[:120], body.headline.strip()[:200]
    c.profile = json.dumps({f: getattr(body, f).strip()[:3000] for f in FIELDS})
    db.commit()
    return candidate_dict(c)


@app.post("/api/candidate/resume")
async def upload_resume(file: UploadFile = File(...), db=Depends(get_db)):
    data = await file.read()
    if len(data) > MAX_UPLOAD:
        raise HTTPException(413, "File too large (max 5 MB).")
    try:
        text = extract_text(file.filename or "", data)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception:
        raise HTTPException(400, "Could not read that file. Is it a valid PDF/DOCX?")
    c = get_candidate(db)
    c.resume_text, c.resume_filename = text, file.filename
    db.commit()
    return candidate_dict(c)


@app.post("/api/chat")
def chat(body: ChatIn, db=Depends(get_db)):
    c = get_candidate(db)
    if not c.resume_text and c.profile in (None, "", "{}"):
        raise HTTPException(409, "No candidate data yet. Upload a resume in the Profile tab first.")
    context = build_context(c)
    return StreamingResponse(
        llm.stream_chat(context, body.message, body.history), media_type="text/plain; charset=utf-8"
    )


@app.post("/api/score")
async def score(
    job_description: str = Form(""), file: UploadFile | None = File(None), db=Depends(get_db)
):
    jd = job_description.strip()
    if file is not None and file.filename:
        try:
            jd = extract_text(file.filename, await file.read())
        except ValueError as e:
            raise HTTPException(400, str(e))
    if not jd:
        raise HTTPException(400, "Provide a job description (text or file).")
    c = get_candidate(db)
    if not c.resume_text:
        raise HTTPException(409, "Upload a resume first.")
    try:
        return llm.score_fit(build_context(c), jd).model_dump()
    except RuntimeError as e:
        raise HTTPException(502, str(e))


# Serve the frontend at "/" (mounted last so /api routes win)
FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="frontend")
