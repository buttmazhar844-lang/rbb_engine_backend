from typing import List, Optional
from sqlalchemy.orm import Session, Query
from app.models.generation_job import GenerationJob
from app.schemas.generation_job import GenerationJobCreate
from app.core.enums import Locale, CurriculumBoard, JobStatus, JobType

class GenerationJobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, job_data: GenerationJobCreate) -> GenerationJob:
        """Create new generation job"""
        job_dict = job_data.model_dump()
        job_dict['status'] = JobStatus.PENDING
        db_job = GenerationJob(**job_dict)
        self.db.add(db_job)
        self.db.commit()
        self.db.refresh(db_job)
        return db_job

    def get_by_id(self, job_id: int) -> Optional[GenerationJob]:
        """Get generation job by ID"""
        return self.db.query(GenerationJob).filter(GenerationJob.id == job_id).first()

    def get_all(
        self,
        status: Optional[JobStatus] = None,
        curriculum_board: Optional[CurriculumBoard] = None,
        grade_level: Optional[int] = None,
        locale: Optional[Locale] = None,
        job_type: Optional[JobType] = None
    ) -> Query:
        """Get all generation jobs with optional filters"""
        query = self.db.query(GenerationJob)
        
        if status:
            query = query.filter(GenerationJob.status == status)
        if curriculum_board:
            query = query.filter(GenerationJob.curriculum_board == curriculum_board)
        if grade_level:
            query = query.filter(GenerationJob.grade_level == grade_level)
        if locale:
            query = query.filter(GenerationJob.locale == locale)
        if job_type:
            query = query.filter(GenerationJob.job_type == job_type)
            
        return query.order_by(GenerationJob.created_at.desc())