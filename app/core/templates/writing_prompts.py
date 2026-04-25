from typing import Dict, Any
from .base import BaseTemplate, TemplateStructure, TemplateField
from ..enums import TemplateType, WorldviewFlag, GradeLevel


class WritingPromptsTemplate(BaseTemplate):
    def __init__(self):
        super().__init__(TemplateType.WRITING_PROMPTS)

    def define_structure(self) -> TemplateStructure:
        return TemplateStructure(
            template_type=TemplateType.WRITING_PROMPTS,
            fields=[
                TemplateField(name="title", type="string", max_length=100),
                TemplateField(name="objectives", type="string", max_length=300),
                TemplateField(name="directions", type="string", max_length=300),
                TemplateField(name="prompts", type="array"),       # list of 3 dicts: {title, content}
                TemplateField(name="exemplar_title", type="string", max_length=100),
                TemplateField(name="exemplar_subtitle", type="string", max_length=100),
                TemplateField(name="exemplar_content", type="text", max_length=2000),
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
Generate a Writing Prompts Pack for ELA Standard {standard_code}, Grade {grade_level.value}.

CRITICAL: The "title" field in your JSON output MUST be exactly "Writing Prompts". Do not change it.

Include exactly 3 writing prompts and one writing exemplar response.

{"Apply a Christian worldview: prompts should encourage reflection on faith, virtue, and purpose." if christian else ""}

FORMATTING RULES (strictly follow):
- Objectives use bullet points (\u2022), one per line, no blank lines between bullets
- Prompt titles use Title Case
- Prompt content is 2-4 sentences: context + task + guidance
- Exemplar content is continuous prose, paragraphs separated by single newlines
- Do NOT use markdown, asterisks, or hyphens for bullets

OUTPUT FORMAT (JSON):
{{
  "title": "Writing Prompts",
  "bundle_title": "[Standard Code] [Topic] Bundle",
  "tagline": "[VERB PHRASE] | [VERB PHRASE] | [VERB PHRASE]",
  "objectives": "\u2022 Objective one\n\u2022 Objective two",
  "directions": "Choose one prompt and write a well-organized response using evidence from the text.",
  "exemplar_title": "Writing Exemplar",
  "exemplar_subtitle": "Sample Response",
  "exemplar_content": "full exemplar text with paragraphs separated by single newlines",
  "prompts": [
    {{"number": 1, "title": "Prompt Title", "content": "..."}},
    {{"number": 2, "title": "Prompt Title", "content": "..."}},
    {{"number": 3, "title": "Prompt Title", "content": "..."}}
  ]
}}
"""
