from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.core.enums import Locale, CurriculumBoard, TemplateType, ProductStatus, ELAStandardType, GradeLevel, WorldviewFlag

class ProductBase(BaseModel):
    standard_id: int
    generation_job_id: Optional[int] = None
    template_type: TemplateType
    status: ProductStatus = ProductStatus.DRAFT
    locale: Locale = Locale.US
    curriculum_board: CurriculumBoard = CurriculumBoard.COMMON_CORE
    grade_level: GradeLevel
    ela_standard_type: ELAStandardType
    ela_standard_code: str
    worldview_flag: WorldviewFlag = WorldviewFlag.NEUTRAL
    is_christian_content: bool = False
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    internal_linking_block: Optional[str] = None
    social_snippets: Optional[List[Dict[str, Any]]] = None

class ProductCreate(ProductBase):
    @field_validator('curriculum_board')
    @classmethod
    def validate_curriculum_board(cls, v, info):
        # Only Common Core supported for ELA content
        if v != CurriculumBoard.COMMON_CORE:
            raise ValueError("Only Common Core curriculum is supported for ELA content")
        return v

    @field_validator('grade_level')
    @classmethod
    def validate_grade_level(cls, v):
        if v not in [GradeLevel.GRADE_6, GradeLevel.GRADE_7, GradeLevel.GRADE_8]:
            raise ValueError("Grade level must be 6, 7, or 8 for ELA content")
        return v

    @field_validator('ela_standard_code')
    @classmethod
    def validate_ela_standard_code(cls, v, info):
        ela_type = info.data.get('ela_standard_type')
        grade_level = info.data.get('grade_level')
        if ela_type and grade_level:
            expected_prefix = f"{ela_type.value}.{grade_level.value}."
            if not v.startswith(expected_prefix):
                raise ValueError(f"ELA standard code must start with {expected_prefix}")
        return v

class ProductRead(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
