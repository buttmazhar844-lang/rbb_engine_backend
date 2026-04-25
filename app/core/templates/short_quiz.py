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
Generate a Short Quiz for ELA Standard {standard_code}, Grade {grade_level.value}.

CRITICAL: The "title" field in your JSON output MUST be exactly "Short Quiz". Do not change it.

Create exactly 7 questions with mixed types:
- Questions 1-5: Multiple-choice with 4 options (A, B, C, D)
- Questions 6-7: Short-response questions (2-3 sentence model answer)

{"Apply a Christian worldview: questions should reflect values of truth and integrity." if christian else ""}

FORMATTING RULES (strictly follow):
- MCQ questions MUST have 4 options labeled A, B, C, D
- MCQ answer format: "B - [Answer Text]"
- Short-response answer: provide a model answer (2-3 sentences)
- Objectives and directions use bullet points (\u2022), one per line
- Do NOT use markdown, asterisks, or hyphens for bullets

OUTPUT FORMAT (JSON):
{{
  "title": "Short Quiz",
  "bundle_title": "[Standard Code] [Topic] Bundle",
  "tagline": "[VERB PHRASE] | [VERB PHRASE] | [VERB PHRASE]",
  "objectives": "\u2022 Objective one\n\u2022 Objective two",
  "directions": "Directions: Choose the best answer for questions 1-5. Write your response for questions 6-7.",
  "answer_key_title": "Answer Key",
  "questions": [
    {{"number": 1, "question": "Question text?", "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}}, "answer": "B - Answer Text"}},
    {{"number": 6, "question": "Short response question?", "answer": "Model answer here."}},
    {{"number": 7, "question": "Short response question?", "answer": "Model answer here."}}
  ]
}}
"""
