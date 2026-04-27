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
                TemplateField(name="prompts", type="array"),
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

CRITICAL: The "title" field MUST be exactly "Writing Prompts". Do not change it.
{"Apply a Christian worldview: prompts should encourage reflection on faith, virtue, and purpose." if christian else ""}

CRITICAL: Every field has a strict character limit. NEVER exceed it.

FIELD LIMITS (characters including spaces):
- title: exactly "Writing Prompts"
- bundle_title: max 60 chars
- tagline: max 65 chars (3 verb phrases separated by " | ")
- objectives: max 220 chars (2 bullet points using •, one per line)
- directions: max 220 chars (1-2 sentences)
- exemplar_title: max 55 chars (e.g. "Writing Exemplar")
- exemplar_subtitle: max 75 chars (e.g. "Sample Response")
- exemplar_content: max 2500 chars (full model response, 32 lines max)
- Each prompt title: max 75 chars (Title Case)
- Each prompt content: max 460 chars (3-5 sentences: context + task + guidance — fits in 6-line box)

OUTPUT FORMAT (JSON only, no markdown):
{{
  "title": "Writing Prompts",
  "bundle_title": "{standard_code} [Topic] Bundle",
  "tagline": "[Verb Phrase] | [Verb Phrase] | [Verb Phrase]",
  "objectives": "• Objective one\\n• Objective two",
  "directions": "Choose one prompt and write a well-organized response using evidence from the text.",
  "exemplar_title": "Writing Exemplar",
  "exemplar_subtitle": "Sample Response",
  "exemplar_content": "Full model response here...",
  "prompts": [
    {{"number": 1, "title": "Prompt Title Here", "content": "Prompt context and task here. Include guidance for the student response."}},
    {{"number": 2, "title": "Prompt Title Here", "content": "Prompt context and task here. Include guidance for the student response."}},
    {{"number": 3, "title": "Prompt Title Here", "content": "Prompt context and task here. Include guidance for the student response."}}
  ]
}}
"""
