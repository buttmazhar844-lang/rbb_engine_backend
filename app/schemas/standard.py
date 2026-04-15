from pydantic import BaseModel, field_validator
from datetime import datetime
from app.core.enums import Locale, CurriculumBoard

class StandardBase(BaseModel):
    locale: Locale = Locale.US
    curriculum_board: CurriculumBoard = CurriculumBoard.COMMON_CORE
    grade_level: int
    grade_range: str | None = None
    code: str
    description: str | None = None

class StandardCreate(StandardBase):
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

class StandardRead(StandardBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True