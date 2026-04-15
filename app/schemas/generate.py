from pydantic import BaseModel
from app.core.enums import TemplateType, Locale, CurriculumBoard, ELAStandardType, GradeLevel, WorldviewFlag

class GenerateTemplateRequest(BaseModel):
    standard_id: int
    template_type: TemplateType
    locale: Locale = Locale.US
    curriculum_board: CurriculumBoard = CurriculumBoard.COMMON_CORE
    grade_level: GradeLevel
    ela_standard_type: ELAStandardType
    ela_standard_code: str
    worldview_flag: WorldviewFlag = WorldviewFlag.NEUTRAL

class GenerateTemplateResponse(BaseModel):
    job_id: int
    product_id: int
    message: str
    seo_title: str | None = None
    seo_description: str | None = None