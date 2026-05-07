from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.bundle_context import BundleContext
from app.core.responses import success

router = APIRouter()

@router.get("/{standard_id}")
async def get_bundle_context(standard_id: int, db: Session = Depends(get_db)):
    """Get the active bundle context (passage info) for a standard, if one exists."""
    ctx = db.query(BundleContext).filter(BundleContext.standard_id == standard_id).first()
    if not ctx:
        return success("No bundle context found", None)
    return success("Bundle context found", {
        "standard_id": ctx.standard_id,
        "passage_title": ctx.passage_title,
        "passage_topic": ctx.passage_topic,
        "key_vocabulary": ctx.key_vocabulary,
        "updated_at": ctx.updated_at.isoformat() if ctx.updated_at else None,
    })
