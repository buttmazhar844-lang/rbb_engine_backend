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
Generate a Bundle Overview for ELA Standard {standard_code}, Grade {grade_level.value}.

CRITICAL: The "title" field in your JSON output MUST be exactly "Bundle Overview". Do not change it.

{"Apply a Christian worldview perspective where appropriate." if christian else ""}

FORMATTING RULES (strictly follow):
- Use bullet points (\u2022) for list items, one per line, no blank lines between bullets
- Use numbered lists (1. 2. 3.) for sequential items like What's Included
- Keep each section concise and compact — no excessive blank lines
- Subheading titles use Title Case
- Do NOT use markdown, asterisks, or hyphens for bullets

OUTPUT FORMAT (JSON):
{{
  "title": "Bundle Overview",
  "bundle_title": "[Standard Code] [Topic] Bundle",
  "tagline": "[VERB PHRASE] | [VERB PHRASE] | [VERB PHRASE]",
  "standard_alignment_title": "Standard Alignment",
  "standard_alignment_content": "{standard_code}: [full standard description]",
  "standard_breakdown_title": "Standard Breakdown",
  "standard_breakdown_content": "What students must know: ...\nWhat students must do: ...\nRequired skills: ...\nDepth of knowledge: ...",
  "whats_included_title": "What's Included",
  "whats_included_content": "1. Bundle Overview Page\n2. Vocabulary Pack\n3. Anchor Reading Passages\n4. Reading Comprehension Questions\n5. Writing Prompt Pack\n6. Graphic Organizer Pack\n7. Mini-Lesson & Anchor Chart\n8. Exit Tickets\n9. Short Quiz\n10. Performance Task\n11. Homework Page\n12. Final Review Page + Answer Key",
  "learning_objectives_title": "Learning Objectives",
  "learning_objectives_content": "\u2022 Objective one\n\u2022 Objective two\n\u2022 Objective three",
  "suggested_pacing_title": "Suggested Pacing",
  "suggested_pacing_content": "Day 1: ...\nDay 2: ...\nDay 3: ...\nDay 4: ...\nDay 5: ...",
  "materials_needed_title": "Materials Needed",
  "materials_needed_content": "\u2022 Item one\n\u2022 Item two\n\u2022 Item three",
  "differentiation_tips_title": "Differentiation Tips",
  "differentiation_tips_content": "For Struggling Readers: ...\nFor Advanced Learners: ...\nFor ELL Students: ...",
  "assessment_overview_title": "Assessment Overview",
  "assessment_overview_content": "Formative: ...\nSummative: ...\nStandards-Based: ..."
}}
"""
