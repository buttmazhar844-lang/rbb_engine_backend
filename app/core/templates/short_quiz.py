from typing import Dict, Any
from .base import BaseTemplate, TemplateStructure, TemplateField, LENGTH_CONTROL_INSTRUCTION
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
                # 4-5 MC + 1-2 short-response = 6-7 total (within 6-8 spec)
                TemplateField(name="questions", type="array", min_items=6, max_items=8),
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

{LENGTH_CONTROL_INSTRUCTION}

CRITICAL: The "title" field MUST be exactly "Short Quiz". Do not change it.
{"Apply a Christian worldview: questions should reflect values of truth and integrity." if christian else ""}

QUESTION COUNTS (STRICT):
- Multiple-choice questions: EXACTLY 4 or 5 (with 4 options A, B, C, D each)
- Short-response questions: EXACTLY 1 or 2
- Total questions: EXACTLY 6, 7, or 8
- Include all answers concisely in the answer key

FIELD LIMITS (characters including spaces):
- title: exactly "Short Quiz"
- bundle_title: max 60 chars
- tagline: max 65 chars (3 verb phrases separated by " | ")
- objectives: max 220 chars (2 bullet points using •, one per line)
- directions: max 220 chars (1-2 sentences)
- answer_key_title: max 55 chars
- MC question text: max 80 chars
- MC each option (A/B/C/D): max 55 chars each
- MC answer: max 70 chars (format: "B - Answer text")
- Short-response question text: max 120 chars
- Short-response answer: max 300 chars (2-3 sentences)

OUTPUT FORMAT (JSON only, no markdown):
{{
  "title": "Short Quiz",
  "bundle_title": "{standard_code} [Topic] Bundle",
  "tagline": "[Verb Phrase] | [Verb Phrase] | [Verb Phrase]",
  "objectives": "• Objective one\\n• Objective two",
  "directions": "Directions: Choose the best answer for multiple choice questions. Write your response for short response questions.",
  "answer_key_title": "Answer Key",
  "questions": [
    {{"number": 1, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "B - Option B"}},
    {{"number": 2, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "A - Option A"}},
    {{"number": 3, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "C - Option C"}},
    {{"number": 4, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "D - Option D"}},
    {{"number": 5, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "B - Option B"}},
    {{"number": 6, "question": "Short response question?", "answer": "Model answer here."}}
  ]
}}
"""
