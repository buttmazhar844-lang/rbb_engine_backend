from pydantic import BaseModel
from typing import Any
from app.core.enums import TemplateType, Locale, CurriculumBoard, ELAStandardType, GradeLevel, WorldviewFlag

class GenerateTemplateRequest(BaseModel):
    standard_id: int
    template_type: TemplateType
    locale: Locale = Locale.US
    curriculum_board: CurriculumBoard = CurriculumBoard.COMMON_CORE
    grade_level: GradeLevel
    ela_standard_type: ELAStandardType | None = None
    ela_standard_code: str
    worldview_flag: WorldviewFlag = WorldviewFlag.NEUTRAL

    def model_post_init(self, __context: Any) -> None:
        # Derive ela_standard_type from ela_standard_code if not provided
        if self.ela_standard_type is None and self.ela_standard_code:
            prefix = self.ela_standard_code.split('.')[0].upper()
            try:
                object.__setattr__(self, 'ela_standard_type', ELAStandardType(prefix))
            except ValueError:
                object.__setattr__(self, 'ela_standard_type', ELAStandardType.RI)

class GenerateTemplateResponse(BaseModel):
    job_id: int
    product_id: int
    message: str
    seo_title: str | None = None
    seo_description: str | None = None