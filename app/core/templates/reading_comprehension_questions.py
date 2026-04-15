from typing import Dict, Any
from .base import BaseTemplate, TemplateStructure, TemplateField
from ..enums import TemplateType, WorldviewFlag, GradeLevel


class ReadingComprehensionQuestionsTemplate(BaseTemplate):
    def __init__(self):
        super().__init__(TemplateType.READING_COMPREHENSION_QUESTIONS)

    def define_structure(self) -> TemplateStructure:
        return TemplateStructure(
            template_type=TemplateType.READING_COMPREHENSION_QUESTIONS,
            fields=[
                TemplateField(name="title", type="string", max_length=100),
                TemplateField(name="objectives", type="string", max_length=300),
                TemplateField(name="directions", type="string", max_length=300),
                TemplateField(name="question_type_1_title", type="string", max_length=100),
                TemplateField(name="question_type_2_title", type="string", max_length=100),
                TemplateField(name="questions", type="array"),   # list of 10 dicts: {question, answer}
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
Generate Reading Comprehension Questions for ELA Standard {standard_code}, Grade {grade_level}.

Produce exactly 10 questions split into two types:
- Type 1 (questions 1-5): Literal / recall questions
- Type 2 (questions 6-10): Inferential / analytical questions

Each question must include the question text and a model answer.

{"Apply a Christian worldview: themes of truth, wisdom, and character." if christian else ""}

OUTPUT FORMAT (JSON):
{{
  "title": "Reading Comprehension Questions",
  "objectives": "objectives text",
  "directions": "directions text",
  "question_type_1_title": "Literal Questions",
  "question_type_2_title": "Inferential Questions",
  "answer_key_title": "Answer Key",
  "questions": [
    {{"number": 1, "question": "...", "answer": "..."}},
    ...
  ]
}}
"""
