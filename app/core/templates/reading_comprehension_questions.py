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
Generate Reading Comprehension Questions for ELA Standard {standard_code}, Grade {grade_level.value}.

CRITICAL: The "title" field in your JSON output MUST be exactly "Reading Comprehension Questions". Do not change it.

Produce exactly 10 questions with mixed types:
- Questions 1-5 (Literal): Multiple-choice with 4 options (A, B, C, D)
- Questions 6-8 (Inferential): Short-response questions (2-4 sentence answer)
- Questions 9-10 (Extended): Extended-response questions (paragraph answer)

Each question must include the question text and a model answer.

{"Apply a Christian worldview: themes of truth, wisdom, and character." if christian else ""}

FORMATTING RULES (strictly follow):
- MCQ questions MUST have 4 options labeled A, B, C, D
- MCQ answer format: "A - [Answer Text]"
- Short/extended response: provide a model answer
- Objectives and directions use bullet points (\u2022), one per line
- Do NOT use markdown, asterisks, or hyphens for bullets

OUTPUT FORMAT (JSON):
{{
  "title": "Reading Comprehension Questions",
  "bundle_title": "[Standard Code] [Topic] Bundle",
  "tagline": "[VERB PHRASE] | [VERB PHRASE] | [VERB PHRASE]",
  "objectives": "\u2022 Objective one\n\u2022 Objective two",
  "directions": "Read each question carefully. Choose the best answer for questions 1-5. Write your response for questions 6-10.",
  "question_type_1_title": "Multiple Choice Questions",
  "question_type_2_title": "Short & Extended Response",
  "answer_key_title": "Answer Key",
  "questions": [
    {{"number": 1, "question": "Question text?", "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}}, "answer": "A - Answer Text"}},
    {{"number": 6, "question": "Short response question?", "answer": "Model short answer here."}},
    {{"number": 9, "question": "Extended response question?", "answer": "Model extended answer here."}},
    ...
  ]
}}
"""
