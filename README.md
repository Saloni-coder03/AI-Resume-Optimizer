# AI Resume Optimizer

An AI-powered resume matching system that tells you
exactly how well your resume matches a job description
and what you need to improve

##  What Does This Do

- Upload your resume PDF or Word file
- Paste any job description
- Get a match score instantly
- See exactly which skills you are missing
- Get personalized recommendations
- Get a free learning roadmap to close skill gaps

##  How The AI Works

Resume PDF or Word
↓
Extract Text using pdfminer or docx2txt
↓
Find Skills Experience Education using spaCy
↓
Convert to Vector using all-MiniLM-L6-v2
↓
Compare with Job Description Vector
↓
Calculate Match Score using Cosine Similarity
↓
Generate Recommendations
↓
Show Results on Screen

##  Team
Person 1 → AI and ML Engineer → owns backend/ai/ and backend/data/
Person 2 → Full Stack Developer → owns backend/api/ and frontend/

##  Tech Stack

### AI and ML
- all-MiniLM-L6-v2 → Resume and job semantic matching
- spaCy → Skill and entity extraction
- sentence-transformers → Text to vector conversion
- scikit-learn → Cosine similarity calculation
- pdfminer.six → PDF text extraction
- docx2txt → Word file text extraction

### Backend
- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic

### Frontend
- React.js
- Tailwind CSS
- Chart.js
- React Dropzone
- Axios

##  Project Structure

backend/
├── core/          ← Config and Logger
├── ai/            ← All AI and ML code
├── api/           ← FastAPI routes
├── database/      ← Database models
├── data/          ← Datasets and skills
├── evaluation/    ← Quality testing
└── tests/         ← Unit tests

frontend/
└── src/
    ├── pages/     ← All pages
    ├── components/← UI components
    ├── api/       ← API calls
    └── utils/     ← Helper functions

##  Setup

### Person 1 Setup

cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_lg
python data/download_data.py
python scripts/build_skills_db.py

### Person 2 Setup

cd frontend
npm install

##  How To Run

### Run Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload
Runs at http://localhost:8000
API docs at http://localhost:8000/docs

### Run Frontend
cd frontend
npm start
Runs at http://localhost:3000

##  API Endpoints

POST /api/upload-resume → Upload PDF or Word resume
POST /api/match-job → Match resume to job description
GET  /api/dashboard → Get match history

## How Scoring Works

Final Score = Weighted Average

Overall Semantic Match  ×  35%
Skills Match Score      ×  40%
Experience Match        ×  15%
Education Match         ×  10%

80% and above → Excellent Match
60% to 79%    → Good Match
40% to 59%    → Partial Match
Below 40%     → Poor Match