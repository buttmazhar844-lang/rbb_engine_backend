from sqlalchemy.orm import Session
from app.models.generation_job import GenerationJob
from app.models.product import Product
from app.core.enums import JobStatus, ProductStatus
from app.utils.logger import logger

def mark_job_running(db: Session, job_id: int) -> None:
    """Mark job as running and log the transition"""
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job:
        logger.warning(f"Job {job_id} not found for status update")
        return
    
    job.status = JobStatus.PENDING
    db.commit()
    logger.info(f"Job {job_id} marked as PENDING")

def mark_job_completed(db: Session, job_id: int) -> None:
    """Mark job as completed and log the transition"""
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job:
        logger.warning(f"Job {job_id} not found for status update")
        return
    
    job.status = JobStatus.COMPLETED
    db.commit()
    logger.info(f"Job {job_id} marked as COMPLETED")

def mark_job_failed(db: Session, job_id: int) -> None:
    """Mark job as failed and log the transition"""
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job:
        logger.warning(f"Job {job_id} not found for status update")
        return
    
    job.status = JobStatus.FAILED
    db.commit()
    logger.info(f"Job {job_id} marked as FAILED")

def update_job_progress(db: Session, job_id: int, product_id: int, new_status: ProductStatus) -> None:
    """Update job progress counters when product status changes"""
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job:
        logger.warning(f"Job {job_id} not found for progress update")
        return
    
    # Count products by status
    products = db.query(Product).filter(Product.generation_job_id == job_id).all()
    
    total = len(products)
    completed = sum(1 for p in products if p.status == ProductStatus.GENERATED)
    failed = sum(1 for p in products if p.status == ProductStatus.FAILED)
    
    # Update job tracking fields
    job.total_products = total
    job.completed_products = completed
    job.failed_products = failed
    
    # Update job status based on completion
    old_status = job.status
    if completed + failed == total and total > 0:
        job.status = JobStatus.COMPLETED
        logger.info(f"Job {job_id} completed: {completed} generated, {failed} failed")
    elif completed > 0 or failed > 0:
        job.status = JobStatus.PENDING
    
    db.commit()
    
    if old_status != job.status:
        logger.info(f"Job {job_id} status changed from {old_status} to {job.status}")
    
    logger.info(f"Job {job_id} progress: {completed}/{total} completed, {failed} failed (product {product_id} → {new_status.value})")

def update_job_status(db: Session, job_id: int) -> None:
    """Update generation job status based on associated products"""
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job:
        logger.warning(f"Job {job_id} not found for status update")
        return
    
    # Count products by status
    products = db.query(Product).filter(Product.generation_job_id == job_id).all()
    
    total = len(products)
    completed = sum(1 for p in products if p.status == ProductStatus.GENERATED)
    failed = sum(1 for p in products if p.status == ProductStatus.FAILED)
    
    # Update job tracking fields
    job.total_products = total
    job.completed_products = completed
    job.failed_products = failed
    
    # Update job status based on product states
    old_status = job.status
    if total == 0:
        job.status = JobStatus.PENDING
    elif completed + failed == total:
        job.status = JobStatus.COMPLETED
    elif completed > 0 or failed > 0:
        job.status = JobStatus.PENDING
    else:
        job.status = JobStatus.PENDING
    
    db.commit()
    
    if old_status != job.status:
        logger.info(f"Job {job_id} status changed from {old_status} to {job.status}")
    
    logger.info(f"Updated job {job_id}: {completed}/{total} completed, {failed} failed")