from typing import Dict, Any
from .base import BaseTemplate, TemplateStructure, TemplateField
from ..enums import TemplateType, WorldviewFlag, GradeLevel


class VocabularyPackTemplate(BaseTemplate):
    def __init__(self):
        super().__init__(TemplateType.VOCABULARY_PACK)

    def define_structure(self) -> TemplateStructure:
        return TemplateStructure(
            template_type=TemplateType.VOCABULARY_PACK,
            fields=[
                TemplateField(name="title", type="string", max_length=100),
                TemplateField(name="objectives", type="string", max_length=300),
                TemplateField(name="directions", type="string", max_length=300),
                TemplateField(name="vocabulary_words", type="array"),  # list of 10 dicts: {word, definition, sentence}
                TemplateField(name="quiz_header", type="string", max_length=100),
                TemplateField(name="quiz_direction", type="string", max_length=200),
                TemplateField(name="quiz_questions", type="array"),    # list of 6 dicts: {question, answer}
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
Generate a Vocabulary Pack for ELA Standard {standard_code}, Grade {grade_level.value}.

CRITICAL: The "title" field in your JSON output MUST be exactly "Vocabulary Pack". Do not change it.

Include exactly 10 vocabulary words, each with a definition and an example sentence.
Also include a 6-question vocabulary quiz with answers.

{"Apply a Christian worldview: choose words that reflect virtue, wisdom, and character." if christian else ""}

FORMATTING RULES (strictly follow):
- Vocabulary word labels MUST use Camel Case: e.g. "Parallel Structure", "Frame Narrative"
- Objectives: use bullet points (\u2022), one per line, no blank lines between bullets
- Quiz questions MUST include 4 multiple-choice options labeled A, B, C, D
- Answer format: "C - [Correct Term]"
- Do NOT use markdown, asterisks, or hyphens for bullets

OUTPUT FORMAT (JSON):
{{
  "title": "Vocabulary Pack",
  "bundle_title": "[Standard Code] [Topic] Bundle",
  "tagline": "[VERB PHRASE] | [VERB PHRASE] | [VERB PHRASE]",
  "objectives": "\u2022 Objective one\n\u2022 Objective two",
  "directions": "Study the key vocabulary terms and examples, then complete the quiz by selecting the best answer for each question.",
  "quiz_header": "Vocabulary Quiz",
  "quiz_direction": "Directions: Choose the best answer for each question.",
  "answer_key_title": "Answer Key",
  "vocabulary_words": [
    {{"number": 1, "word": "Camel Case Word", "definition": "...", "sentence": "..."}},
    ...
  ],
  "quiz_questions": [
    {{"number": 1, "question": "Question text here?", "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}}, "answer": "C - Correct Term"}},
    ...
  ]
}}
"""
