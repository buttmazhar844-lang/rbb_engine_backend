from typing import Dict, Any
from .base import BaseTemplate, TemplateStructure, TemplateField, LENGTH_CONTROL_INSTRUCTION
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
                TemplateField(name="vocabulary_words", type="array", min_items=6, max_items=8),
                TemplateField(name="quiz_header", type="string", max_length=100),
                TemplateField(name="quiz_direction", type="string", max_length=200),
                TemplateField(name="quiz_questions", type="array", min_items=5, max_items=6),
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

{LENGTH_CONTROL_INSTRUCTION}

CRITICAL: The "title" field MUST be exactly "Vocabulary Pack". Do not change it.
{"Apply a Christian worldview: choose words that reflect virtue, wisdom, and character." if christian else ""}

CRITICAL: Every field has a strict character limit. NEVER exceed it.

LENGTH REQUIREMENTS:
- vocabulary_words: EXACTLY 6–8 words (no fewer, no more)
- Each definition: 1 concise sentence (max 75 chars)
- Each example sentence: 1 sentence per word (max 220 chars)
- quiz_questions: EXACTLY 5–6 questions (no fewer, no more)

FIELD LIMITS (characters including spaces):
- title: exactly "Vocabulary Pack"
- bundle_title: max 60 chars
- tagline: max 65 chars (3 verb phrases separated by " | ")
- objectives: max 220 chars (2 bullet points using •, one per line)
- directions: max 220 chars (1-2 sentences)
- quiz_header: max 75 chars (e.g. "Vocabulary Quiz")
- quiz_direction: max 75 chars (1 sentence)
- answer_key_title: max 55 chars
- Each word label: max 75 chars
- Each definition: max 75 chars (1 concise sentence)
- Each sentence: max 220 chars (1 sentence in context)
- Each quiz question text: max 80 chars
- Each quiz option (A/B/C/D): max 55 chars
- Each quiz answer: max 75 chars (format: "C - Term")

OUTPUT FORMAT (JSON only, no markdown):
{{
  "title": "Vocabulary Pack",
  "bundle_title": "{standard_code} [Topic] Bundle",
  "tagline": "[Verb Phrase] | [Verb Phrase] | [Verb Phrase]",
  "objectives": "• Objective one\\n• Objective two",
  "directions": "Study the key vocabulary terms and examples, then complete the quiz.",
  "quiz_header": "Vocabulary Quiz",
  "quiz_direction": "Directions: Choose the best answer for each question.",
  "answer_key_title": "Answer Key",
  "vocabulary_words": [
    {{"number": 1, "word": "Camel Case Term", "definition": "Concise definition here.", "sentence": "Example sentence using the term in context."}},
    {{"number": 2, "word": "Camel Case Term", "definition": "Concise definition here.", "sentence": "Example sentence using the term in context."}},
    {{"number": 3, "word": "Camel Case Term", "definition": "Concise definition here.", "sentence": "Example sentence using the term in context."}},
    {{"number": 4, "word": "Camel Case Term", "definition": "Concise definition here.", "sentence": "Example sentence using the term in context."}},
    {{"number": 5, "word": "Camel Case Term", "definition": "Concise definition here.", "sentence": "Example sentence using the term in context."}},
    {{"number": 6, "word": "Camel Case Term", "definition": "Concise definition here.", "sentence": "Example sentence using the term in context."}}
  ],
  "quiz_questions": [
    {{"number": 1, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "C - Term"}},
    {{"number": 2, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "A - Term"}},
    {{"number": 3, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "B - Term"}},
    {{"number": 4, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "D - Term"}},
    {{"number": 5, "question": "Short MCQ question?", "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}}, "answer": "C - Term"}}
  ]
}}
"""
