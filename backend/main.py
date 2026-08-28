from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.resume_routes import router as resume_router
from api.routes.match_routes import router as match_router


app = FastAPI(
    title="AI Resume Optimizer API",
    description="API for resume and job description matching",
    version="1.0.0",
)


# Development CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(match_router)


@app.get("/")
def root():
    return {
        "message": "AI Resume Optimizer API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }