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
                TemplateField(name="questions", type="array"),
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

CRITICAL: The "title" field MUST be exactly "Short Quiz". Do not change it.
{"Apply a Christian worldview: questions should reflect values of truth and integrity." if christian else ""}

CRITICAL: Every field has a strict character limit. NEVER exceed it.

QUESTION TYPES:
- Questions 1-5: Multiple-choice with 4 options (A, B, C, D) — each fits in a 6-line box at 11pt
- Questions 6-7: Short-response — each fits in a 6-line box at 11pt

FIELD LIMITS (characters including spaces):
- title: exactly "Short Quiz"
- bundle_title: max 60 chars
- tagline: max 65 chars (3 verb phrases separated by " | ")
- objectives: max 220 chars (2 bullet points using •, one per line)
- directions: max 220 chars (1-2 sentences)
- answer_key_title: max 55 chars
- Q1-5 question text: max 80 chars (short, leaves room for 4 options in the box)
- Q1-5 each option (A/B/C/D): max 55 chars each
- Q1-5 answer: max 70 chars (format: "B - Answer text")
- Q6-7 question text: max 120 chars
- Q6-7 answer: max 300 chars (2-3 sentences)

OUTPUT FORMAT (JSON only, no markdown):
{{
  "title": "Short Quiz",
  "bundle_title": "{standard_code} [Topic] Bundle",
  "tagline": "[Verb Phrase] | [Verb Phrase] | [Verb Phrase]",
  "objectives": "• Objective one\\n• Objective two",
  "directions": "Directions: Choose the best answer for questions 1-5. Write your response for questions 6-7.",
  "answer_key_title": "Answer Key",
  "questions": [
    {{"number": 1, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "B - Option B"}},
    {{"number": 2, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "A - Option A"}},
    {{"number": 3, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "C - Option C"}},
    {{"number": 4, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "D - Option D"}},
    {{"number": 5, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "B - Option B"}},
    {{"number": 6, "question": "Short response question?", "answer": "Model answer here."}},
    {{"number": 7, "question": "Short response question?", "answer": "Model answer here."}}
  ]
}}
"""
