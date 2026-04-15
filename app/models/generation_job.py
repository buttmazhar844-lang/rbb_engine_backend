from sqlalchemy import Column, Integer, String, DateTime, Index, Enum
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.enums import Locale, CurriculumBoard, JobStatus, JobType, ELAStandardType, GradeLevel, WorldviewFlag

class GenerationJob(Base):
    """Jobs that generate ELA template-based products"""
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    standard_id = Column(Integer, nullable=False, index=True)  # References Standard.id
    locale = Column(Enum(Locale), nullable=False, default=Locale.US, index=True)
    curriculum_board = Column(Enum(CurriculumBoard), nullable=False, default=CurriculumBoard.COMMON_CORE, index=True)
    grade_level = Column(Enum(GradeLevel, values_callable=lambda x: [e.value for e in x]), nullable=False, index=True)
    ela_standard_type = Column(Enum(ELAStandardType), nullable=False, index=True)
    ela_standard_code = Column(String(50), nullable=False, index=True)
    worldview_flag = Column(Enum(WorldviewFlag), nullable=False, default=WorldviewFlag.NEUTRAL, index=True)
    job_type = Column(Enum(JobType), nullable=False, default=JobType.SINGLE_TEMPLATE, index=True)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, index=True)
    total_products = Column(Integer, default=1)  # Simplified to single template
    completed_products = Column(Integer, default=0)
    failed_products = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('ix_generation_jobs_locale_curriculum', 'locale', 'curriculum_board'),
        Index('ix_generation_jobs_status_created', 'status', 'created_at'),
        Index('ix_generation_jobs_standard_type', 'standard_id', 'job_type'),
        Index('ix_generation_jobs_grade_ela', 'grade_level', 'ela_standard_type'),
    )