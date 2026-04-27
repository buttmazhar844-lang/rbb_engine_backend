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
                TemplateField(name="tickets", type="array"),
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

CRITICAL: The "title" field MUST be exactly "Exit Tickets". Do not change it.
{"Apply a Christian worldview: questions should encourage reflection on values and character." if christian else ""}

CRITICAL: Every field has a strict character limit. NEVER exceed it.

FIELD LIMITS (characters including spaces):
- title: exactly "Exit Tickets"
- bundle_title: max 60 chars
- tagline: max 65 chars (3 verb phrases separated by " | ")
- objectives: max 220 chars (2 bullet points using •, one per line)
- directions: max 220 chars (1-2 sentences)
- answer_key_title: max 55 chars
- Each ticket title: max 55 chars (Title Case)
- Each ticket question: max 150 chars (1-2 sentences, fits in 2-line box)
- Each ticket sample_answer: max 300 chars (2-3 sentences, fits in 4-line box)

OUTPUT FORMAT (JSON only, no markdown):
{{
  "title": "Exit Tickets",
  "bundle_title": "{standard_code} [Topic] Bundle",
  "tagline": "[Verb Phrase] | [Verb Phrase] | [Verb Phrase]",
  "objectives": "• Objective one\\n• Objective two",
  "directions": "Answer the question below in complete sentences.",
  "answer_key_title": "Answer Key",
  "tickets": [
    {{"number": 1, "title": "Ticket Title Here", "question": "Question text here?", "sample_answer": "Sample answer here."}},
    {{"number": 2, "title": "Ticket Title Here", "question": "Question text here?", "sample_answer": "Sample answer here."}},
    {{"number": 3, "title": "Ticket Title Here", "question": "Question text here?", "sample_answer": "Sample answer here."}},
    {{"number": 4, "title": "Ticket Title Here", "question": "Question text here?", "sample_answer": "Sample answer here."}},
    {{"number": 5, "title": "Ticket Title Here", "question": "Question text here?", "sample_answer": "Sample answer here."}}
  ]
}}
"""
