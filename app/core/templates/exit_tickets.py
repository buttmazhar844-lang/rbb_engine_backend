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
Generate Exit Tickets for ELA Standard {standard_code}, Grade {grade_level}.

Create exactly 5 exit tickets. Each ticket has a short title, a question, and a sample answer.

{"Apply a Christian worldview: questions should encourage reflection on values and character." if christian else ""}

OUTPUT FORMAT (JSON):
{{
  "title": "Exit Tickets",
  "objectives": "objectives text",
  "directions": "directions text",
  "answer_key_title": "Answer Key",
  "tickets": [
    {{"number": 1, "title": "...", "question": "...", "sample_answer": "..."}},
    ...
  ]
}}
"""
