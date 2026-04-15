from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.db.session import get_db
from app.utils.logger import logger

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Enhanced health check endpoint with service info and DB connectivity"""
    try:
        # Test database connectivity
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "disconnected"
    
    health_info = {
        "status": "ok" if db_status == "connected" else "degraded",
        "service": "rbb-engine-backend",
        "version": "1.0.0",
        "environment": settings.environment,
        "database": db_status
    }
    
    logger.info(f"Health check: {health_info['status']} (DB: {db_status})")
    return health_info
