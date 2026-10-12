"""
FastAPI Main Application Entrypoint for Marketing Mix Copilot
Serves REST API endpoints, scenario simulations, and static web dashboard.
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.app.config import settings
from backend.app.db.database import engine, Base
from backend.app.routers.agents_router import router as agents_router
from backend.app.routers.modeling_router import router as modeling_router
from backend.app.routers.recommendations_router import router as recs_router
from backend.app.routers.approvals_router import router as approvals_router
from backend.app.routers.observability_router import router as observability_router

# Initialize schema
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Bayesian Marketing Mix Modeling & Causal Incrementality agentic copilot with human governance."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents_router)
app.include_router(modeling_router)
app.include_router(recs_router)
app.include_router(approvals_router)
app.include_router(observability_router)

FRONTEND_PATH = Path(__file__).resolve().parent.parent.parent / "frontend"


@app.get("/", include_in_schema=False)
def serve_dashboard():
    """Serves the interactive Marketing Mix Copilot dashboard."""
    index_file = FRONTEND_PATH / "index.html"
    return FileResponse(index_file)


@app.get("/health", tags=["Health"])
def health_check():
    """Health & readiness status."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
        "demo_mode": settings.demo_mode
    }
