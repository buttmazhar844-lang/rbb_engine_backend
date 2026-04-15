from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
from pathlib import Path
import json
from app.db.session import get_db
from app.repositories.products import ProductRepository
from app.schemas.product import ProductRead, ProductCreate
from app.core.enums import Locale, CurriculumBoard, TemplateType, ProductStatus
from app.core.responses import success
from app.utils.pagination import PaginationParams, paginate_query
from app.utils.logger import logger
from app.utils.storage import storage_manager
from app.utils.pdf_generator import pdf_generator

router = APIRouter()

@router.post("")
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create new product"""
    try:
        repo = ProductRepository(db)
        db_product = repo.create(product)
        logger.info(f"Created product: {db_product.product_type} for standard {db_product.standard_id} (ID: {db_product.id})")
        return success("Product created successfully", ProductRead.model_validate(db_product))
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("")
async def list_products(
    status: Optional[ProductStatus] = Query(None),
    template_type: Optional[TemplateType] = Query(None),
    generation_job_id: Optional[int] = Query(None),
    standard_id: Optional[int] = Query(None),
    curriculum_board: Optional[CurriculumBoard] = Query(None),
    grade_level: Optional[int] = Query(None),
    locale: Optional[Locale] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List all products with filtering and pagination (newest first)"""
    try:
        repo = ProductRepository(db)
        query = repo.get_all(status, template_type, generation_job_id, standard_id, curriculum_board, grade_level, locale)
        
        # Ensure consistent ordering (newest first)
        query = query.order_by(repo.model.created_at.desc())
        
        pagination_params = PaginationParams(limit=limit, offset=offset)
        paginated_result = paginate_query(query, pagination_params)
        
        products_data = [ProductRead.model_validate(product) for product in paginated_result.items]
        
        # Log filtering info
        filters_applied = []
        if status: filters_applied.append(f"status={status.value}")
        if template_type: filters_applied.append(f"type={template_type.value}")
        if generation_job_id: filters_applied.append(f"job_id={generation_job_id}")
        if standard_id: filters_applied.append(f"standard_id={standard_id}")
        
        filter_str = ", ".join(filters_applied) if filters_applied else "no filters"
        logger.info(f"Listed {len(products_data)} products (total: {paginated_result.total}) with {filter_str}")
        
        return success("Products retrieved successfully", {
            "products": products_data,
            "pagination": {
                "total": paginated_result.total,
                "limit": paginated_result.limit,
                "offset": paginated_result.offset,
                "has_next": paginated_result.has_next
            }
        })
    except Exception as e:
        logger.error(f"Error listing products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get specific product details"""
    if product_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid product ID")
        
    try:
        repo = ProductRepository(db)
        product = repo.get_by_id(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
            
        logger.info(f"Retrieved product {product_id}")
        return success("Product retrieved successfully", ProductRead.model_validate(product))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{product_id}/content")
async def get_product_content(product_id: int, db: Session = Depends(get_db)):
    """Get the actual generated content for a product"""
    if product_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid product ID")
        
    try:
        repo = ProductRepository(db)
        product = repo.get_by_id(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Load content from raw.json
        product_path = storage_manager.get_product_path(product_id)
        raw_json_path = product_path / "raw.json"
        
        if not raw_json_path.exists():
            raise HTTPException(status_code=404, detail="Product content not found")
        
        with open(raw_json_path, 'r') as f:
            content_data = json.load(f)
        
        logger.info(f"Retrieved content for product {product_id}")
        return success("Product content retrieved successfully", content_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting content for product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{product_id}/download/pdf")
async def download_product_pdf(product_id: int, db: Session = Depends(get_db)):
    """Download product as PDF file"""
    try:
        repo = ProductRepository(db)
        product = repo.get_by_id(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        if product.status != ProductStatus.GENERATED:
            raise HTTPException(status_code=400, detail="Product not ready for download")
        
        # Check if PDF already exists
        product_path = storage_manager.get_product_path(product_id)
        pdf_path = product_path / f"worksheet_{product_id}.pdf"
        
        # Generate PDF if it doesn't exist
        if not pdf_path.exists():
            # Load content from raw.json
            raw_json_path = product_path / "raw.json"
            if not raw_json_path.exists():
                raise HTTPException(status_code=404, detail="Product content not found")
            
            with open(raw_json_path, 'r') as f:
                content_data = json.load(f)
            
            # Add product metadata to content for PDF generation
            content_data['grade_level'] = product.grade_level.value
            content_data['ela_standard_code'] = product.ela_standard_code
            content_data['worldview_flag'] = product.worldview_flag.value
            
            # Generate PDF
            pdf_path = pdf_generator.generate_pdf_from_content(
                product_id, 
                product.template_type.value, 
                content_data
            )
        
        # Return PDF file
        filename = f"{product.template_type.value.lower()}_{product.grade_level}_{product_id}.pdf"
        return FileResponse(
            path=str(pdf_path),
            filename=filename,
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading PDF for product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF")

@router.get("/{product_id}/download/pptx")
async def download_product_pptx(product_id: int, db: Session = Depends(get_db)):
    """Download product as PPTX file — generates on-the-fly if not already on disk"""
    PPTX_FILENAMES = {
        'ANCHOR_READING_PASSAGE':          'anchor_reading_passage.pptx',
        'BUNDLE_OVERVIEW':                 'bundle_overview.pptx',
        'EXIT_TICKETS':                    'exit_tickets.pptx',
        'READING_COMPREHENSION_QUESTIONS': 'reading_comprehension_questions.pptx',
        'SHORT_QUIZ':                      'short_quiz.pptx',
        'VOCABULARY_PACK':                 'vocabulary_pack.pptx',
        'WRITING_PROMPTS':                 'writing_prompts.pptx',
    }
    try:
        repo = ProductRepository(db)
        product = repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.status != ProductStatus.GENERATED:
            raise HTTPException(status_code=400, detail="Product not ready for download")
        pptx_filename = PPTX_FILENAMES.get(product.template_type.value)
        if not pptx_filename:
            raise HTTPException(status_code=400, detail="PPTX download not supported for this template type")

        product_path = storage_manager.get_product_path(product_id)
        pptx_path = product_path / pptx_filename

        # Generate on-the-fly if the file doesn't exist yet
        if not pptx_path.exists():
            raw_json_path = product_path / "raw.json"
            if not raw_json_path.exists():
                raise HTTPException(status_code=404, detail="Product content not found — cannot generate PPTX")
            with open(raw_json_path, 'r') as f:
                content_data = json.load(f)
            product_metadata = {
                'grade_level': product.grade_level.value,
                'ela_standard_code': product.ela_standard_code,
                'ela_standard_type': product.ela_standard_type.value,
                'worldview_flag': product.worldview_flag.value,
                'curriculum_board': product.curriculum_board.value,
            }
            from app.services.pptx_processor import pptx_processor
            pptx_path = pptx_processor.process_template(
                template_type=product.template_type.value,
                content_data=content_data,
                product_metadata=product_metadata,
                product_id=product_id
            )
            logger.info(f"Generated PPTX on-the-fly for product {product_id}")

        filename = f"{product.template_type.value.lower()}_grade_{product.grade_level}_{product_id}.pptx"
        return FileResponse(
            path=str(pptx_path),
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading PPTX for product {product_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate PPTX: {e}")
@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product and its associated files"""
    if product_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid product ID")
    try:
        repo = ProductRepository(db)
        product = repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        # Delete storage files
        import shutil
        product_path = storage_manager.get_product_path(product_id)
        if product_path.exists():
            shutil.rmtree(str(product_path))
        repo.delete(product_id)
        logger.info(f"Deleted product {product_id}")
        return success("Product deleted successfully", {"id": product_id})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/{product_id}/status")
async def update_product_status(
    product_id: int,
    status: ProductStatus,
    db: Session = Depends(get_db)
):
    """Update product status with validation and job progress tracking"""
    if product_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid product ID")
        
    try:
        repo = ProductRepository(db)
        product = repo.get_by_id(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Validate status transitions
        valid_transitions = {
            ProductStatus.DRAFT: [ProductStatus.GENERATED, ProductStatus.FAILED],
            ProductStatus.GENERATED: [ProductStatus.FAILED],
            ProductStatus.FAILED: [ProductStatus.DRAFT]
        }
        
        if status not in valid_transitions.get(product.status, []):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid status transition from {product.status.value} to {status.value}"
            )
        
        old_status = product.status
        
        # Update product status
        updated_product = repo.update_status(product_id, status)
        
        # Update associated generation job progress
        if updated_product.generation_job_id:
            from app.services.job_status import update_job_progress
            update_job_progress(db, updated_product.generation_job_id, product_id, status)
        
        logger.info(f"Updated product {product_id} status from {old_status.value} to {status.value}")
        
        return success("Product status updated", {
            "id": product_id, 
            "status": status.value,
            "previous_status": old_status.value,
            "product": ProductRead.model_validate(updated_product)
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product {product_id} status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")