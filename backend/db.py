"""Database layer (SQLAlchemy). SQLite by default, PostgreSQL via DATABASE_URL."""
import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
URL = os.getenv("DATABASE_URL", "sqlite:///./hiremeai.db")
engine = create_engine(
    URL, connect_args={"check_same_thread": False} if URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), default="")
    headline = Column(String(200), default="")
    resume_filename = Column(String(200), default="")
    resume_text = Column(Text, default="")
    profile = Column(Text, default="{}")  # JSON: about, skills, strengths, ...
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_candidate(db) -> Candidate:
    """This app serves one candidate portfolio (id=1)."""
    c = db.get(Candidate, 1)
    if not c:
        c = Candidate(id=1)
        db.add(c)
        db.commit()
        db.refresh(c)
    return c
