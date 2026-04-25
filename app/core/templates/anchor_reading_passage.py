from typing import Dict, Any
from .base import BaseTemplate, TemplateStructure, TemplateField
from ..enums import TemplateType, WorldviewFlag, GradeLevel

class AnchorReadingPassageTemplate(BaseTemplate):
    def __init__(self):
        super().__init__(TemplateType.ANCHOR_READING_PASSAGE)
    
    def define_structure(self) -> TemplateStructure:
        return TemplateStructure(
            template_type=TemplateType.ANCHOR_READING_PASSAGE,
            fields=[
                TemplateField(name="title", type="string", max_length=100),
                TemplateField(name="passage_text", type="text", max_length=2000),
                TemplateField(name="reading_level", type="string", max_length=20),
                TemplateField(name="word_count", type="integer"),
                TemplateField(name="key_vocabulary", type="array"),
                TemplateField(name="main_theme", type="string", max_length=200),
                TemplateField(name="discussion_questions", type="array"),
            ],
            christian_guidelines={
                "content_tone": "Academic and informative, values-aligned but not preachy",
                "themes": "Focus on character, perseverance, wisdom, service to others",
                "avoid": "Sermon-like language, direct Bible citations unless requested",
                "approach": "Integrate Christian values naturally through story themes"
            },
            grade_constraints={
                GradeLevel.GRADE_6: {
                    "word_count_range": [400, 600],
                    "reading_level": "6.0-6.9",
                    "vocabulary_complexity": "grade_appropriate"
                },
                GradeLevel.GRADE_7: {
                    "word_count_range": [500, 750],
                    "reading_level": "7.0-7.9", 
                    "vocabulary_complexity": "slightly_challenging"
                },
                GradeLevel.GRADE_8: {
                    "word_count_range": [600, 900],
                    "reading_level": "8.0-8.9",
                    "vocabulary_complexity": "challenging"
                }
            }
        )
    
    def generate_prompt(self, standard_code: str, grade_level: GradeLevel, 
                       worldview_flag: WorldviewFlag) -> str:
        constraints = self.structure.grade_constraints[grade_level]
        christian_guidelines = self.structure.christian_guidelines if worldview_flag == WorldviewFlag.CHRISTIAN else {}
        
        prompt = f"""
Generate an Anchor Reading Passage for ELA Standard {standard_code}, Grade {grade_level.value}.

CRITICAL: The "title" field in your JSON output must be the passage title (a creative story/article title), NOT the product type name.

STRUCTURE REQUIREMENTS:
- Title: Engaging, grade-appropriate (max 100 chars)
- Passage: {constraints['word_count_range'][0]}-{constraints['word_count_range'][1]} words
- Reading Level: {constraints['reading_level']}
- Key Vocabulary: 5-8 important terms with definitions
- Main Theme: Clear central message (max 200 chars)
- Discussion Questions: 3-4 thought-provoking questions

GRADE {grade_level} CONSTRAINTS:
- Vocabulary: {constraints['vocabulary_complexity']}
- Sentence complexity appropriate for grade level
- Content engaging for middle school students

FORMATTING RULES (strictly follow):
- Passage text: continuous prose paragraphs separated by a single newline, no excessive blank lines
- Key vocabulary: use format "Term: definition" (Camel Case for the term)
- Discussion questions: plain numbered list, one per line
- Do NOT use markdown, asterisks, or hyphens
"""

        if worldview_flag == WorldviewFlag.CHRISTIAN:
            prompt += f"""
CHRISTIAN WORLDVIEW GUIDELINES:
- Tone: {christian_guidelines['content_tone']}
- Themes: {christian_guidelines['themes']}
- Avoid: {christian_guidelines['avoid']}
- Approach: {christian_guidelines['approach']}
"""

        prompt += """
OUTPUT FORMAT (JSON):
{
  "title": "passage title",
  "bundle_title": "[Standard Code] [Topic] Bundle",
  "tagline": "[VERB PHRASE] | [VERB PHRASE] | [VERB PHRASE]",
  "objectives": "\u2022 Objective one\n\u2022 Objective two\n\u2022 Objective three",
  "directions": "Read the passage carefully. Pay attention to the main theme and key vocabulary.",
  "passage_text": "full passage text with paragraphs separated by single newlines",
  "reading_level": "calculated level",
  "word_count": actual_count,
  "key_vocabulary": ["Camel Case Term: definition", "Term Two: definition"],
  "main_theme": "central message",
  "discussion_questions": ["question1", "question2", "question3"]
}
"""
        return prompt