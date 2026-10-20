# HireMeAI — AI Portfolio Chatbot for HR

HireMeAI is an AI-powered portfolio chatbot that helps recruiters and HR professionals learn about a candidate through natural conversations. Recruiters can explore the candidate's skills, projects, strengths, weaknesses, hobbies, and career goals using information provided in the candidate's profile and resume.

The application also supports **voice-based interaction**, resume parsing, and AI-powered job description matching.

## Key Features

- **AI-Powered HR Chatbot:** Answers recruiter questions using the candidate's saved profile and resume data.
- **Voice Input:** Allows users to ask questions using their microphone through browser speech recognition.
- **Spoken AI Responses:** Reads chatbot answers aloud using browser text-to-speech.
- **Resume Upload and Parsing:** Upload PDF, DOCX, or TXT resumes and extract their text.
- **Job Description Matching:** Evaluates candidate suitability for a job description and provides a match score, strengths, and skill gaps.
- **Candidate Profile Management:** Add and update candidate information, including skills, projects, strengths, weaknesses, hobbies, and goals.
- **Streaming Responses:** Displays AI-generated responses as they are received.
- **Privacy-Conscious Responses:** Instructs the AI to answer using available candidate information and avoid inventing facts.
- **Responsive Web Interface:** Provides a simple interface for interacting with the chatbot.

## Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI, Uvicorn
- **LLM:** Groq API — `openai/gpt-oss-120b`
- **Database:** SQLAlchemy with SQLite by default; PostgreSQL can be configured
- **Data Validation:** Pydantic
- **Document Processing:** pypdf, python-docx
- **Voice Features:** Web Speech API (speech recognition and speech synthesis)

## Project Structure

```text
hiremeai/
├── backend/
│   ├── main.py
│   ├── llm.py
│   ├── parsing.py
│   ├── db.py
│   └── __init__.py
├── frontend/
│   └── index.html
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/hiremeai.git
cd hiremeai
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and add your Groq API key.

```dotenv
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Get an API key from the [Groq Console](https://console.groq.com/keys).

**Security:** Never commit your `.env` file or expose your API key in source code.

### 5. Run the application

From the project root, execute:

```bash
uvicorn backend.main:app --reload
```

Open the application at:

- **Web app:** http://127.0.0.1:8000
- **API documentation:** http://127.0.0.1:8000/docs

## How to Use

1. Open the Candidate Profile section.
2. Upload a resume and enter the candidate's profile information.
3. Save the profile.
4. Open HR Chat and ask questions by typing or using the microphone.
5. Listen to AI responses when spoken output is enabled.
6. Use the job-matching feature to submit a job description and review the candidate's score, strengths, and gaps.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/candidate` | Retrieve the candidate profile |
| PUT | `/api/candidate` | Update the candidate profile |
| POST | `/api/candidate/resume` | Upload and parse a resume |
| POST | `/api/chat` | Stream AI chatbot responses |
| POST | `/api/score` | Evaluate candidate-job compatibility |
| GET | `/api/health` | Check application health and API configuration |

## Database Configuration

SQLite is used by default. PostgreSQL can be configured through the `DATABASE_URL` environment variable if supported by the application's database configuration.

Example:

```dotenv
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/hiremeai
```

Install the PostgreSQL driver if required:

```bash
pip install psycopg2-binary
```

## Voice Feature Compatibility

Voice input and spoken responses use browser-provided speech APIs. Microphone access generally requires user permission and a secure context, such as HTTPS, or localhost during development. Availability and voice support may vary by browser and operating system.

## Limitations

- Image-only scanned PDFs may require OCR before their text can be extracted.
- The chatbot depends on the availability of the configured Groq API.
- Job matching provides an AI-generated assessment, not a definitive hiring decision.
- The current application is designed around a single candidate portfolio.

## Future Improvements

- Multi-candidate profile management
- Authentication and role-based access
- OCR support for scanned resumes
- Improved voice controls and multilingual support
- Deployment with a managed database and production monitoring

## License

Add a license if you intend to distribute or allow others to reuse this project.
