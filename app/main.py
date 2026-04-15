from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.v1.routes import health, standards, products, generation_jobs, dashboard, templates
from app.api.v1.routes import generate
from app.utils.storage import storage_manager
from app.utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {settings.app_name}")
    storage_manager.ensure_directories()
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        lifespan=lifespan,
        redirect_slashes=False
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register routers
    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(generate.router, prefix="/api", tags=["generate"])
    app.include_router(products.router, prefix="/api/products", tags=["products"])
    app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
    app.include_router(standards.router, prefix="/api/v1/standards", tags=["standards"])
    app.include_router(generation_jobs.router, prefix="/api/v1/generation-jobs", tags=["generation-jobs"])
    app.include_router(templates.router, prefix="/api/v1", tags=["templates"])
    
    return app

app = create_app()
