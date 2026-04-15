from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db
from app.schemas.generate import GenerateTemplateRequest, GenerateTemplateResponse
from app.models.generation_job import GenerationJob
from app.models.product import Product
from app.models.standard import Standard
from app.core.enums import JobType, JobStatus, ProductStatus
from app.utils.logger import logger
from app.utils.storage import storage_manager
from app.utils.pdf_stub import generate_stub_pdf
from app.utils.thumbnail_stub import generate_stub_thumbnail
from app.utils.validation import validate_positive_integer
from app.services.job_status import update_job_progress
from app.services.pptx_processor import pptx_processor

# AI Agents
from app.ai.agents.generator import generator_agent
from app.ai.agents.qc import qc_agent
from app.ai.agents.metadata import metadata_agent

router = APIRouter()

@router.post("/generate-template", response_model=GenerateTemplateResponse)
async def generate_template(
    request: GenerateTemplateRequest,
    db: Session = Depends(get_db)
):
    """Generate ELA template-based content with Christian worldview support"""
    
    # Validate input fields
    validate_positive_integer(request.standard_id, "standard_id")
    
    try:
        # Get standard information for AI generation
        standard = db.query(Standard).filter(Standard.id == request.standard_id).first()
        if not standard:
            raise HTTPException(status_code=404, detail="Standard not found")
        
        # Use transaction for atomic creation
        try:
            # Create generation job
            job = GenerationJob(
                standard_id=request.standard_id,
                locale=request.locale,
                curriculum_board=request.curriculum_board,
                grade_level=request.grade_level,
                ela_standard_type=request.ela_standard_type,
                ela_standard_code=request.ela_standard_code,
                worldview_flag=request.worldview_flag,
                job_type=JobType.SINGLE_TEMPLATE,
                status=JobStatus.PENDING,
                total_products=1,
                completed_products=0,
                failed_products=0
            )
            db.add(job)
            db.flush()  # Get job ID
            
            # Create product record
            product = Product(
                standard_id=request.standard_id,
                generation_job_id=job.id,
                template_type=request.template_type,
                status=ProductStatus.DRAFT,
                locale=request.locale,
                curriculum_board=request.curriculum_board,
                grade_level=request.grade_level,
                ela_standard_type=request.ela_standard_type,
                ela_standard_code=request.ela_standard_code,
                worldview_flag=request.worldview_flag,
                is_christian_content=(request.worldview_flag.value == "CHRISTIAN")
            )
            db.add(product)
            db.flush()  # Get product ID
            
            # Create storage structure and stub files
            try:
                storage_manager.create_stub_files(product.id)
                generate_stub_pdf(product.id, request.template_type.value)
                generate_stub_thumbnail(product.id, request.template_type.value)
            except Exception as storage_error:
                logger.warning(f"Storage setup failed for product {product.id}: {storage_error}")
            
            db.commit()
        except Exception as db_error:
            db.rollback()
            raise db_error
        
        # AI Agent Orchestration for Template-Based Generation
        try:
            logger.info(f"Starting template-based AI generation for product {product.id}")
            
            # Step 1: Generate Template Content
            content = await generator_agent.generate_template_content(
                product_id=product.id,
                template_type=request.template_type.value,
                standard=standard.description or standard.code,
                grade_level=request.grade_level.value,
                ela_standard_type=request.ela_standard_type.value,
                ela_standard_code=request.ela_standard_code,
                worldview_flag=request.worldview_flag.value,
                curriculum=request.curriculum_board.value
            )
            
            # Step 2: Quality Control with Christian Content Validation
            qc_result = await qc_agent.evaluate_template_content(
                product_id=product.id,
                template_type=request.template_type.value,
                content=content,
                standard=standard.description or standard.code,
                grade_level=request.grade_level.value,
                worldview_flag=request.worldview_flag.value
            )
            
            # Step 3: Generate SEO Metadata and Social Content
            metadata = await metadata_agent.generate_template_metadata(
                product_id=product.id,
                template_type=request.template_type.value,
                content=content,
                standard=standard.description or standard.code,
                grade_level=request.grade_level.value,
                ela_standard_code=request.ela_standard_code,
                worldview_flag=request.worldview_flag.value
            )
            
            # Update product with SEO metadata
            product.seo_title = metadata.get('seo_title')
            product.seo_description = metadata.get('seo_description')
            product.internal_linking_block = metadata.get('internal_linking_block')
            product.social_snippets = metadata.get('social_snippets')
            
            # Update product status based on QC result
            if qc_result.get('verdict') in ('PASS', 'NEEDS_FIX'):
                product.status = ProductStatus.GENERATED
                logger.info(f"Template {product.id} generated successfully (QC: {qc_result.get('score')}%)")
            else:
                product.status = ProductStatus.FAILED
                logger.warning(f"Template {product.id} failed QC: {qc_result.get('verdict')} (score: {qc_result.get('score')}%)")
            
            db.commit()
            
            # Step 4: Generate PPTX for all supported templates
            if product.status == ProductStatus.GENERATED:
                try:
                    logger.info(f"Starting PPTX generation for product {product.id}")
                    product_metadata = {
                        'grade_level': request.grade_level.value,
                        'ela_standard_code': request.ela_standard_code,
                        'ela_standard_type': request.ela_standard_type.value,
                        'worldview_flag': request.worldview_flag.value,
                        'curriculum_board': request.curriculum_board.value,
                    }
                    pptx_processor.process_template(
                        template_type=request.template_type.value,
                        content_data=content,
                        product_metadata=product_metadata,
                        product_id=product.id
                    )
                    logger.info(f"PPTX generation completed for product {product.id}")
                except Exception as pptx_error:
                    logger.error(f"PPTX generation failed for product {product.id}: {pptx_error}")
                    logger.warning(f"Product {product.id} generated but PPTX creation failed")
            
            # Update job progress
            update_job_progress(db, job.id, product.id, product.status)
            
        except Exception as ai_error:
            logger.error(f"AI template generation failed for product {product.id}: {ai_error}")
            product.status = ProductStatus.FAILED
            db.commit()
            update_job_progress(db, job.id, product.id, ProductStatus.FAILED)
            
        logger.info(
            f"Generated template job {job.id} with product {product.id}: "
            f"{request.template_type.value} for {request.ela_standard_code} "
            f"(Grade {request.grade_level.value}, {request.worldview_flag.value}) - Status: {product.status.value}"
        )
        
        return GenerateTemplateResponse(
            job_id=job.id,
            product_id=product.id,
            message=f"Template generation completed for {request.template_type.value} - Status: {product.status.value}",
            seo_title=product.seo_title,
            seo_description=product.seo_description
        )
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error in generate_template: {e}")
        raise HTTPException(status_code=500, detail="Failed to create generation job")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error in generate_template: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")