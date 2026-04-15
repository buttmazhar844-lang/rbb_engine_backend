from typing import Dict, Any
from .base import BaseTemplate, TemplateStructure, TemplateField
from ..enums import TemplateType, WorldviewFlag, GradeLevel


class ShortQuizTemplate(BaseTemplate):
    def __init__(self):
        super().__init__(TemplateType.SHORT_QUIZ)

    def define_structure(self) -> TemplateStructure:
        return TemplateStructure(
            template_type=TemplateType.SHORT_QUIZ,
            fields=[
                TemplateField(name="title", type="string", max_length=100),
                TemplateField(name="objectives", type="string", max_length=300),
                TemplateField(name="directions", type="string", max_length=300),
                TemplateField(name="questions", type="array"),  # list of 7 dicts: {question, answer}
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
Generate a Short Quiz for ELA Standard {standard_code}, Grade {grade_level}.

Create exactly 7 questions with model answers.

{"Apply a Christian worldview: questions should reflect values of truth and integrity." if christian else ""}

OUTPUT FORMAT (JSON):
{{
  "title": "Short Quiz",
  "objectives": "objectives text",
  "directions": "directions text",
  "answer_key_title": "Answer Key",
  "questions": [
    {{"number": 1, "question": "...", "answer": "..."}},
    ...
  ]
}}
"""
