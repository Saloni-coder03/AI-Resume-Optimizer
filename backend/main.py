
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.resume_routes import router as resume_router
from api.routes.match_routes import router as match_router
from api.routes.dashboard_routes import router as dashboard_router

from database.db_setup import init_db, check_db_connection


# --------------------------------------------------
# APPLICATION LIFESPAN
# --------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


# --------------------------------------------------
# CREATE FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="AI Resume Optimizer API",
    description=(
        "API for resume analysis, AI matching, "
        "recommendations, learning roadmap, "
        "and dashboard history."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------

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


# --------------------------------------------------
# REGISTER ROUTES
# --------------------------------------------------

app.include_router(resume_router)
app.include_router(match_router)
app.include_router(dashboard_router)


# --------------------------------------------------
# ROOT ENDPOINT
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "AI Resume Optimizer API is running"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": (
            "connected"
            if check_db_connection()
            else "disconnected"
        ),
    }
