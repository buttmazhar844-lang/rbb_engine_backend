from typing import Dict, Any
from .base import BaseTemplate, TemplateStructure, TemplateField
from ..enums import TemplateType, WorldviewFlag, GradeLevel


class BundleOverviewTemplate(BaseTemplate):
    def __init__(self):
        super().__init__(TemplateType.BUNDLE_OVERVIEW)

    def define_structure(self) -> TemplateStructure:
        return TemplateStructure(
            template_type=TemplateType.BUNDLE_OVERVIEW,
            fields=[
                TemplateField(name="title", type="string", max_length=100),
                TemplateField(name="standard_alignment_title", type="string", max_length=100),
                TemplateField(name="standard_alignment_content", type="string", max_length=500),
                TemplateField(name="standard_breakdown_title", type="string", max_length=100),
                TemplateField(name="standard_breakdown_content", type="string", max_length=800),
                TemplateField(name="whats_included_title", type="string", max_length=100),
                TemplateField(name="whats_included_content", type="string", max_length=800),
                TemplateField(name="learning_objectives_title", type="string", max_length=100),
                TemplateField(name="learning_objectives_content", type="string", max_length=600),
                TemplateField(name="suggested_pacing_title", type="string", max_length=100),
                TemplateField(name="suggested_pacing_content", type="string", max_length=600),
                TemplateField(name="materials_needed_title", type="string", max_length=100),
                TemplateField(name="materials_needed_content", type="string", max_length=700),
                TemplateField(name="differentiation_tips_title", type="string", max_length=100),
                TemplateField(name="differentiation_tips_content", type="string", max_length=800),
                TemplateField(name="assessment_overview_title", type="string", max_length=100),
                TemplateField(name="assessment_overview_content", type="string", max_length=700),
            ],
            christian_guidelines={},
            grade_constraints={
                GradeLevel.GRADE_6: {"complexity": "grade_appropriate"},
                GradeLevel.GRADE_7: {"complexity": "slightly_challenging"},
                GradeLevel.GRADE_8: {"complexity": "challenging"},
            }
        )

    def generate_prompt(self, standard_code: str, grade_level: GradeLevel,
                        worldview_flag: WorldviewFlag) -> str:
        christian = worldview_flag == WorldviewFlag.CHRISTIAN
        return f"""
Generate a Bundle Overview for ELA Standard {standard_code}, Grade {grade_level}.

{"Apply a Christian worldview perspective where appropriate." if christian else ""}

OUTPUT FORMAT (JSON):
{{
  "title": "Bundle Overview",
  "standard_alignment_title": "Standard Alignment",
  "standard_alignment_content": "...",
  "standard_breakdown_title": "Standard Breakdown",
  "standard_breakdown_content": "...",
  "whats_included_title": "What's Included",
  "whats_included_content": "...",
  "learning_objectives_title": "Learning Objectives",
  "learning_objectives_content": "...",
  "suggested_pacing_title": "Suggested Pacing",
  "suggested_pacing_content": "...",
  "materials_needed_title": "Materials Needed",
  "materials_needed_content": "...",
  "differentiation_tips_title": "Differentiation Tips",
  "differentiation_tips_content": "...",
  "assessment_overview_title": "Assessment Overview",
  "assessment_overview_content": "..."
}}
"""
