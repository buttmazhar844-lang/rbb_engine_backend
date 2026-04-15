from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.repositories.standards import StandardRepository
from app.schemas.standard import StandardRead, StandardCreate
from app.core.enums import Locale, CurriculumBoard, GradeLevel, ELAStandardType
from app.core.responses import success
from app.utils.pagination import PaginationParams, paginate_query
from app.utils.logger import logger

router = APIRouter()

@router.post("")
async def create_standard(standard: StandardCreate, db: Session = Depends(get_db)):
    """Create new educational standard"""
    try:
        repo = StandardRepository(db)
        db_standard = repo.create(standard)
        logger.info(f"Created standard: {db_standard.code} (ID: {db_standard.id})")
        return success("Standard created successfully", StandardRead.model_validate(db_standard))
    except Exception as e:
        logger.error(f"Error creating standard: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("")
async def list_standards(
    curriculum_board: Optional[CurriculumBoard] = Query(None),
    grade_level: Optional[GradeLevel] = Query(None),
    ela_standard_type: Optional[ELAStandardType] = Query(None),
    locale: Optional[Locale] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List all available standards with filtering and pagination"""
    try:
        logger.info(f"Standards query - grade_level: {grade_level}, ela_standard_type: {ela_standard_type}, curriculum: {curriculum_board}")
        
        repo = StandardRepository(db)
        query = repo.get_all(curriculum_board, grade_level, ela_standard_type, locale)
        
        pagination_params = PaginationParams(limit=limit, offset=offset)
        paginated_result = paginate_query(query, pagination_params)
        
        standards_data = [StandardRead.model_validate(std) for std in paginated_result.items]
        
        logger.info(f"Standards found: {len(standards_data)} (total: {paginated_result.total})")
        
        return success("Standards retrieved successfully", {
            "standards": standards_data,
            "pagination": {
                "total": paginated_result.total,
                "limit": paginated_result.limit,
                "offset": paginated_result.offset,
                "has_next": paginated_result.has_next
            }
        })
    except Exception as e:
        logger.error(f"Error listing standards: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{standard_id}")
async def get_standard(standard_id: int, db: Session = Depends(get_db)):
    """Get specific standard details"""
    try:
        repo = StandardRepository(db)
        standard = repo.get_by_id(standard_id)
        
        if not standard:
            raise HTTPException(status_code=404, detail="Standard not found")
            
        logger.info(f"Retrieved standard {standard_id}")
        return success("Standard retrieved successfully", StandardRead.model_validate(standard))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting standard {standard_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
@router.get("/lookup")
async def lookup_standards(
    code: Optional[str] = Query(None, description="Search by standard code"),
    grade_level: Optional[GradeLevel] = Query(None),
    ela_standard_type: Optional[ELAStandardType] = Query(None),
    curriculum_board: Optional[CurriculumBoard] = Query(None),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Lightweight standards lookup for Quick Generate flow"""
    try:
        repo = StandardRepository(db)
        query = repo.get_all(curriculum_board, grade_level, ela_standard_type, None)
        
        if code:
            query = query.filter(repo.model.code.ilike(f"%{code}%"))
        
        standards = query.limit(limit).all()
        
        return success("Standards found", {
            "standards": [StandardRead.model_validate(std) for std in standards],
            "count": len(standards)
        })
    except Exception as e:
        logger.error(f"Error in standards lookup: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")