from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db
from app.schemas.generate import GenerateProductRequest, GenerateProductResponse
from app.models.generation_job import GenerationJob
from app.models.product import Product
from app.models.standard import Standard
from app.core.enums import JobType, JobStatus, ProductStatus
from app.core.responses import success
from app.utils.logger import logger

router = APIRouter()

@router.post("/generate-product")
async def generate_product(
    request: GenerateProductRequest,
    db: Session = Depends(get_db)
):
    """Generate product endpoint - simplified version"""
    
    try:
        # Validate standard exists
        standard = db.query(Standard).filter(Standard.id == request.standard_id).first()
        if not standard:
            raise HTTPException(status_code=404, detail="Standard not found")
        
        # Validate grade level
        if not 1 <= request.grade_level <= 12:
            raise HTTPException(status_code=400, detail="Grade level must be between 1 and 12")
        
        # Create generation job (using only fields that exist in current schema)
        job = GenerationJob(
            standard_id=request.standard_id,
            locale=request.locale,
            curriculum_board=request.curriculum_board,
            grade_level=request.grade_level,
            job_type=JobType.SINGLE_PRODUCT,
            status=JobStatus.PENDING
        )
        db.add(job)
        db.flush()  # Get job ID
        
        # Create product record
        product = Product(
            standard_id=request.standard_id,
            generation_job_id=job.id,
            product_type=request.product_type,
            status=ProductStatus.DRAFT,
            locale=request.locale,
            curriculum_board=request.curriculum_board,
            grade_level=request.grade_level
        )
        db.add(product)
        db.flush()  # Get product ID
        
        db.commit()
        
        logger.info(
            f"Created job {job.id} with product {product.id}: "
            f"{request.product_type.value} for standard {request.standard_id} "
            f"(Grade {request.grade_level}, {request.curriculum_board.value})"
        )
        
        return success(
            f"Product generation job created successfully",
            {
                "job_id": job.id,
                "product_ids": [product.id],
                "message": f"Job created for {request.product_type.value} - Status: {product.status.value}"
            }
        )
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in generate_product: {e}")
        raise HTTPException(status_code=500, detail="Failed to create generation job")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in generate_product: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")