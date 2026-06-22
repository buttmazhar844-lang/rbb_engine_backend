from typing import Dict, Any
from .base import BaseTemplate, TemplateStructure, TemplateField, LENGTH_CONTROL_INSTRUCTION
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
                TemplateField(name="prompts", type="array", min_items=2, max_items=3),
                TemplateField(name="exemplar_title", type="string", max_length=100),
                TemplateField(name="exemplar_subtitle", type="string", max_length=100),
                # 180-275 words ≈ 900-1400 chars; cap at 1500 to allow punctuation
                TemplateField(name="exemplar_content", type="text", max_length=1500,
                              min_word_count=180, max_word_count=275),
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

{LENGTH_CONTROL_INSTRUCTION}

CRITICAL: The "title" field MUST be exactly "Writing Prompts". Do not change it.
{"Apply a Christian worldview: prompts should encourage reflection on faith, virtue, and purpose." if christian else ""}

LENGTH REQUIREMENTS (STRICT):
- prompts array: EXACTLY 2 or 3 prompts (no fewer, no more)
- Each prompt content: 2–4 concise sentences (max 460 chars)
- exemplar_content: EXACTLY 180–275 words (do not go under 180 or over 275 words)

FIELD LIMITS (characters including spaces):
- title: exactly "Writing Prompts"
- bundle_title: max 60 chars
- tagline: max 65 chars (3 verb phrases separated by " | ")
- objectives: max 220 chars (2 bullet points using •, one per line)
- directions: max 220 chars (1-2 sentences)
- exemplar_title: max 55 chars
- exemplar_subtitle: max 75 chars
- exemplar_content: 180–275 words, max 1500 chars
- Each prompt title: max 75 chars (Title Case)
- Each prompt content: 2–4 sentences, max 460 chars

OUTPUT FORMAT (JSON only, no markdown):
{{
  "title": "Writing Prompts",
  "bundle_title": "{standard_code} [Topic] Bundle",
  "tagline": "[Verb Phrase] | [Verb Phrase] | [Verb Phrase]",
  "objectives": "• Objective one\\n• Objective two",
  "directions": "Choose one prompt and write a well-organized response using evidence from the text.",
  "exemplar_title": "Writing Exemplar",
  "exemplar_subtitle": "Sample Response",
  "exemplar_content": "Full model response here (180-275 words)...",
  "prompts": [
    {{"number": 1, "title": "Prompt Title Here", "content": "Prompt context and task here (2-4 sentences)."}},
    {{"number": 2, "title": "Prompt Title Here", "content": "Prompt context and task here (2-4 sentences)."}}
  ]
}}
"""
