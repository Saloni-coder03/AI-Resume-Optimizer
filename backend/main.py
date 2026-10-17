
# backend/main.py

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Centralized application configuration
from core.config import settings

# API routes
from api.routes.resume_routes import router as resume_router
from api.routes.match_routes import router as match_router
from api.routes.dashboard_routes import router as dashboard_router

# Database initialization and connection checks
from database.db_setup import init_db, check_db_connection


# --------------------------------------------------
# APPLICATION LIFESPAN
# --------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize the database when FastAPI starts.
    """

    init_db()

    yield


# --------------------------------------------------
# CREATE FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "API for resume analysis, AI matching, "
        "recommendations, learning roadmap, "
        "and dashboard history."
    ),
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------

# Allowed origins are loaded from core/config.py
# and can be overridden through backend/.env.

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# REGISTER API ROUTES
# --------------------------------------------------

# Resume upload endpoint
app.include_router(resume_router)

# AI resume matching endpoint
app.include_router(match_router)

# Dashboard statistics and history endpoints
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
