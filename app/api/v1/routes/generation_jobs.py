from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.repositories.generation_jobs import GenerationJobRepository
from app.schemas.generation_job import GenerationJobRead, GenerationJobCreate
from app.core.enums import JobStatus, JobType, Locale, CurriculumBoard
from app.core.responses import success
from app.utils.pagination import PaginationParams, paginate_query
from app.utils.logger import logger

router = APIRouter()

@router.post("/")
async def create_generation_job(job: GenerationJobCreate, db: Session = Depends(get_db)):
    """Create new generation job"""
    try:
        repo = GenerationJobRepository(db)
        db_job = repo.create(job)
        logger.info(f"Created generation job: {db_job.job_type} for standard {db_job.standard_id} (ID: {db_job.id})")
        return success("Generation job created successfully", GenerationJobRead.model_validate(db_job))
    except Exception as e:
        logger.error(f"Error creating generation job: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def list_generation_jobs(
    status: Optional[JobStatus] = Query(None),
    job_type: Optional[JobType] = Query(None),
    curriculum_board: Optional[CurriculumBoard] = Query(None),
    grade_level: Optional[int] = Query(None),
    locale: Optional[Locale] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List all generation jobs with optional filtering and pagination"""
    try:
        repo = GenerationJobRepository(db)
        query = repo.get_all(status, curriculum_board, grade_level, locale, job_type)
        
        pagination_params = PaginationParams(limit=limit, offset=offset)
        paginated_result = paginate_query(query, pagination_params)
        
        jobs_data = [GenerationJobRead.model_validate(job) for job in paginated_result.items]
        
        return success("Generation jobs retrieved successfully", {
            "jobs": jobs_data,
            "pagination": {
                "total": paginated_result.total,
                "limit": paginated_result.limit,
                "offset": paginated_result.offset,
                "has_next": paginated_result.has_next
            }
        })
    except Exception as e:
        logger.error(f"Error listing generation jobs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{job_id}/summary")
async def get_generation_job_summary(job_id: int, db: Session = Depends(get_db)):
    """Get lightweight job summary for frontend status panels"""
    if job_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid job ID")
        
    try:
        repo = GenerationJobRepository(db)
        job = repo.get_by_id(job_id)
        
        if not job:
            raise HTTPException(status_code=404, detail="Generation job not found")
        
        # Update job counts from products before returning
        from app.services.job_status import update_job_status
        update_job_status(db, job_id)
        
        # Refresh job to get updated counts
        db.refresh(job)
        
        summary = {
            "job_id": job.id,
            "status": job.status,
            "total_products": job.total_products,
            "completed_products": job.completed_products,
            "failed_products": job.failed_products,
            "created_at": job.created_at
        }
        
        logger.info(f"Retrieved job {job_id} summary: {job.completed_products}/{job.total_products} completed")
        return success("Job summary retrieved successfully", summary)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job {job_id} summary: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{job_id}")
async def get_generation_job(job_id: int, db: Session = Depends(get_db)):
    """Get specific job details and progress"""
    if job_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid job ID")
        
    try:
        repo = GenerationJobRepository(db)
        job = repo.get_by_id(job_id)
        
        if not job:
            raise HTTPException(status_code=404, detail="Generation job not found")
        
        # Update job counts from products before returning
        from app.services.job_status import update_job_status
        update_job_status(db, job_id)
        
        # Refresh job to get updated counts
        db.refresh(job)
        
        logger.info(f"Retrieved job {job_id}: {job.completed_products}/{job.total_products} completed")
        return success("Generation job retrieved successfully", GenerationJobRead.model_validate(job))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting generation job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")