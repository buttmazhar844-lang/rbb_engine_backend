from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.product import Product
from app.models.generation_job import GenerationJob
from app.core.enums import ProductStatus, JobStatus, TemplateType, WorldviewFlag
from app.core.responses import success
from app.utils.logger import logger

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get ELA template dashboard statistics"""
    try:
        # Product counts by status
        product_stats = db.query(
            Product.status, func.count(Product.id)
        ).group_by(Product.status).all()
        
        products_by_status = {status.value: 0 for status in ProductStatus}
        for status, count in product_stats:
            products_by_status[status.value] = count
        
        # Generation job counts by status
        job_stats = db.query(
            GenerationJob.status, func.count(GenerationJob.id)
        ).group_by(GenerationJob.status).all()
        
        jobs_by_status = {status.value: 0 for status in JobStatus}
        for status, count in job_stats:
            jobs_by_status[status.value] = count
        
        # Template type distribution
        template_stats = db.query(
            Product.template_type, func.count(Product.id)
        ).group_by(Product.template_type).all()
        
        templates_by_type = {template.value: 0 for template in TemplateType}
        for template_type, count in template_stats:
            templates_by_type[template_type.value] = count
        
        # Christian vs Neutral content
        worldview_stats = db.query(
            Product.worldview_flag, func.count(Product.id)
        ).group_by(Product.worldview_flag).all()
        
        content_by_worldview = {flag.value: 0 for flag in WorldviewFlag}
        for worldview, count in worldview_stats:
            content_by_worldview[worldview.value] = count
        
        # Grade level distribution
        grade_stats = db.query(
            Product.grade_level, func.count(Product.id)
        ).group_by(Product.grade_level).all()
        
        content_by_grade = {}
        for grade, count in grade_stats:
            content_by_grade[f"Grade {grade.value}"] = count
        
        # Total counts
        total_products = sum(products_by_status.values())
        total_jobs = sum(jobs_by_status.values())
        
        stats = {
            "total_products": total_products,
            "products_by_status": products_by_status,
            "total_generation_jobs": total_jobs,
            "jobs_by_status": jobs_by_status,
            "templates_by_type": templates_by_type,
            "content_by_worldview": content_by_worldview,
            "content_by_grade": content_by_grade
        }
        
        logger.info(f"ELA dashboard stats retrieved: {total_products} products, {total_jobs} jobs")
        return success("Dashboard stats retrieved", stats)
        
    except Exception as e:
        logger.error(f"Error retrieving dashboard stats: {e}")
        return success("Dashboard stats retrieved", {
            "total_products": 0,
            "products_by_status": {status.value: 0 for status in ProductStatus},
            "total_generation_jobs": 0,
            "jobs_by_status": {status.value: 0 for status in JobStatus},
            "templates_by_type": {template.value: 0 for template in TemplateType},
            "content_by_worldview": {flag.value: 0 for flag in WorldviewFlag},
            "content_by_grade": {}
        })

@router.get("/summary")
async def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get lightweight ELA dashboard summary"""
    try:
        total_products = db.query(func.count(Product.id)).scalar() or 0
        active_jobs = db.query(func.count(GenerationJob.id)).filter(
            GenerationJob.status == JobStatus.PENDING
        ).scalar() or 0
        christian_content = db.query(func.count(Product.id)).filter(
            Product.worldview_flag == WorldviewFlag.CHRISTIAN
        ).scalar() or 0
        
        summary = {
            "total_products": total_products,
            "active_jobs": active_jobs,
            "christian_content_count": christian_content
        }
        
        logger.info(f"ELA dashboard summary: {total_products} products, {active_jobs} active jobs, {christian_content} Christian content")
        return success("Dashboard summary retrieved", summary)
        
    except Exception as e:
        logger.error(f"Error retrieving dashboard summary: {e}")
        return success("Dashboard summary retrieved", {
            "total_products": 0,
            "active_jobs": 0,
            "christian_content_count": 0
        })