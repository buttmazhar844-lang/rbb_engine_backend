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
Generate Reading Comprehension Questions for ELA Standard {standard_code}, Grade {grade_level.value}.

CRITICAL: The "title" field MUST be exactly "Reading Comprehension Questions". Do not change it.
{"Apply a Christian worldview: themes of truth, wisdom, and character." if christian else ""}

CRITICAL: Every field has a strict character limit. NEVER exceed it.

QUESTION TYPES:
- Questions 1-5: Multiple-choice with 4 options (A, B, C, D) — fits in a 5-line box at 10pt
- Questions 6-8: Short-response (2-4 sentence answer)
- Questions 9-10: Extended-response (paragraph answer)

FIELD LIMITS (characters including spaces):
- title: exactly "Reading Comprehension Questions"
- bundle_title: max 60 chars
- tagline: max 65 chars (3 verb phrases separated by " | ")
- objectives: max 220 chars (2 bullet points using •, one per line)
- directions: max 300 chars (1-2 sentences)
- question_type_1_title: max 75 chars (e.g. "Multiple Choice Questions")
- question_type_2_title: max 75 chars (e.g. "Short & Extended Response")
- answer_key_title: max 65 chars
- Q1-5 question text: max 80 chars each (short enough to leave room for 4 options)
- Q1-5 each option (A/B/C/D): max 60 chars each
- Q1-5 answer: max 75 chars (format: "A - Answer text")
- Q6-8 question text: max 120 chars
- Q6-8 answer: max 300 chars (2-4 sentences)
- Q9-10 question text: max 150 chars
- Q9-10 answer: max 300 chars (paragraph)

OUTPUT FORMAT (JSON only, no markdown):
{{
  "title": "Reading Comprehension Questions",
  "bundle_title": "{standard_code} [Topic] Bundle",
  "tagline": "[Verb Phrase] | [Verb Phrase] | [Verb Phrase]",
  "objectives": "• Objective one\\n• Objective two",
  "directions": "Read each question carefully. Choose the best answer for questions 1-5. Write your response for questions 6-10.",
  "question_type_1_title": "Multiple Choice Questions",
  "question_type_2_title": "Short & Extended Response",
  "answer_key_title": "Answer Key",
  "questions": [
    {{"number": 1, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "A - Option A"}},
    {{"number": 2, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "B - Option B"}},
    {{"number": 3, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "C - Option C"}},
    {{"number": 4, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "D - Option D"}},
    {{"number": 5, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "A - Option A"}},
    {{"number": 6, "question": "Short response question?", "answer": "Model short answer here."}},
    {{"number": 7, "question": "Short response question?", "answer": "Model short answer here."}},
    {{"number": 8, "question": "Short response question?", "answer": "Model short answer here."}},
    {{"number": 9, "question": "Extended response question?", "answer": "Model extended answer here."}},
    {{"number": 10, "question": "Extended response question?", "answer": "Model extended answer here."}}
  ]
}}
"""
