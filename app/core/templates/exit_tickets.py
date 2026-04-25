from typing import Dict, Any
from .base import BaseTemplate, TemplateStructure, TemplateField
from ..enums import TemplateType, WorldviewFlag, GradeLevel


class ExitTicketsTemplate(BaseTemplate):
    def __init__(self):
        super().__init__(TemplateType.EXIT_TICKETS)

    def define_structure(self) -> TemplateStructure:
        return TemplateStructure(
            template_type=TemplateType.EXIT_TICKETS,
            fields=[
                TemplateField(name="title", type="string", max_length=100),
                TemplateField(name="objectives", type="string", max_length=300),
                TemplateField(name="directions", type="string", max_length=300),
                TemplateField(name="tickets", type="array"),  # list of 5 dicts: {title, question, sample_answer}
                TemplateField(name="answer_key_title", type="string", max_length=100),
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
Generate Exit Tickets for ELA Standard {standard_code}, Grade {grade_level.value}.

CRITICAL: The "title" field in your JSON output MUST be exactly "Exit Tickets". Do not change it.

Create exactly 5 exit tickets. Each ticket has a short title, a question, and a sample answer.

{"Apply a Christian worldview: questions should encourage reflection on values and character." if christian else ""}

FORMATTING RULES (strictly follow):
- Objectives use bullet points (\u2022), one per line, no blank lines between bullets
- Ticket titles use Title Case
- Questions are clear and concise (1-2 sentences)
- Sample answers are brief model responses (2-4 sentences)
- Do NOT use markdown, asterisks, or hyphens for bullets

OUTPUT FORMAT (JSON):
{{
  "title": "Exit Tickets",
  "bundle_title": "[Standard Code] [Topic] Bundle",
  "tagline": "[VERB PHRASE] | [VERB PHRASE] | [VERB PHRASE]",
  "objectives": "\u2022 Objective one\n\u2022 Objective two",
  "directions": "Answer the question below in complete sentences.",
  "answer_key_title": "Answer Key",
  "tickets": [
    {{"number": 1, "title": "Ticket Title", "question": "...", "sample_answer": "..."}},
    ...
  ]
}}
"""
