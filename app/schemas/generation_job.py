from pydantic import BaseModel, field_validator
from datetime import datetime
from app.core.enums import Locale, CurriculumBoard, JobStatus, JobType

class GenerationJobBase(BaseModel):
    standard_id: int
    locale: Locale = Locale.US
    curriculum_board: CurriculumBoard = CurriculumBoard.COMMON_CORE
    grade_level: int
    job_type: JobType
    status: JobStatus | None = None

class GenerationJobCreate(GenerationJobBase):
    @field_validator('curriculum_board')
    @classmethod
    def validate_curriculum_board(cls, v, info):
        locale = info.data.get('locale', Locale.US)
        if locale == Locale.US and v != CurriculumBoard.COMMON_CORE:
            raise ValueError("US locale must use Common Core curriculum")
        return v

    @field_validator('grade_level')
    @classmethod
    def validate_grade_level(cls, v):
        if not 1 <= v <= 12:
            raise ValueError("Grade level must be between 1 and 12")
        return v

class GenerationJobRead(GenerationJobBase):
    id: int
    total_products: int
    completed_products: int
    failed_products: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True