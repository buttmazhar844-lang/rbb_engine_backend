from sqlalchemy import Column, Integer, DateTime, Index, Enum, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from app.db.session import Base
from app.core.enums import Locale, CurriculumBoard, TemplateType, ProductStatus, ELAStandardType, GradeLevel, WorldviewFlag

class Product(Base):
    """Generated ELA educational content using templates"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    standard_id = Column(Integer, nullable=False, index=True)  # References Standard.id
    generation_job_id = Column(Integer, nullable=True, index=True)  # References GenerationJob.id
    template_type = Column(Enum(TemplateType), nullable=False, index=True)
    status = Column(Enum(ProductStatus), default=ProductStatus.DRAFT, index=True)
    locale = Column(Enum(Locale), nullable=False, default=Locale.US, index=True)
    curriculum_board = Column(Enum(CurriculumBoard), nullable=False, default=CurriculumBoard.COMMON_CORE, index=True)
    grade_level = Column(Enum(GradeLevel, values_callable=lambda x: [e.value for e in x]), nullable=False, index=True)
    ela_standard_type = Column(Enum(ELAStandardType), nullable=False, index=True)  # RI or RL
    ela_standard_code = Column(String(50), nullable=False, index=True)  # e.g., "RI.6.1"
    worldview_flag = Column(Enum(WorldviewFlag), nullable=False, default=WorldviewFlag.NEUTRAL, index=True)
    is_christian_content = Column(Boolean, default=False, index=True)
    seo_title = Column(String(255), nullable=True)
    seo_description = Column(String(500), nullable=True)
    internal_linking_block = Column(String(1000), nullable=True)
    social_snippets = Column(JSONB, nullable=True)  # JSON array of snippets
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('ix_products_generation_job_id', 'generation_job_id'),
        Index('ix_products_status_template', 'status', 'template_type'),
        Index('ix_products_standard_status', 'standard_id', 'status'),
        Index('ix_products_grade_ela', 'grade_level', 'ela_standard_type'),
        Index('ix_products_worldview', 'worldview_flag', 'is_christian_content'),
    )
