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
                TemplateField(name="slide1_content", type="text", max_length=1840),
                TemplateField(name="slide2_content", type="text", max_length=2754),
                TemplateField(name="slide3_content", type="text", max_length=2754),
                TemplateField(name="main_theme", type="string", max_length=80),
            ],
            christian_guidelines={
                "content_tone": "Academic and informative, values-aligned but not preachy",
                "themes": "Focus on character, perseverance, wisdom, service to others",
                "avoid": "Sermon-like language, direct Bible citations unless requested",
                "approach": "Integrate Christian values naturally through story themes"
            },
            grade_constraints={
                GradeLevel.GRADE_6: {"word_count_range": [400, 600], "reading_level": "6.0-6.9", "vocabulary_complexity": "grade_appropriate"},
                GradeLevel.GRADE_7: {"word_count_range": [500, 750], "reading_level": "7.0-7.9", "vocabulary_complexity": "slightly_challenging"},
                GradeLevel.GRADE_8: {"word_count_range": [600, 900], "reading_level": "8.0-8.9", "vocabulary_complexity": "challenging"}
            }
        )

    def generate_prompt(self, standard_code: str, grade_level: GradeLevel,
                        worldview_flag: WorldviewFlag) -> str:
        constraints = self.structure.grade_constraints[grade_level]
        christian_guidelines = self.structure.christian_guidelines if worldview_flag == WorldviewFlag.CHRISTIAN else {}

        prompt = f"""
Generate an Anchor Reading Passage for ELA Standard {standard_code}, Grade {grade_level.value}.

CRITICAL: Content is split across 3 slides. Each slide gets different content. NO repetition across slides.

SLIDE STRUCTURE:
- Slide 1 (cover page content box): Background context + Key Vocabulary ONLY
- Slide 2 (reading page): The complete passage ONLY
- Slide 3 (questions page): Discussion Questions ONLY — NO vocabulary here

CRITICAL: Every field has a strict character limit. NEVER exceed it.

FIELD LIMITS:
- title: max 50 chars
- bundle_title: max 60 chars
- tagline: max 65 chars (3 verb phrases separated by " | ")
- objectives: max 220 chars (2 bullet points using •, one per line)
- directions: max 220 chars (1-2 sentences)
- main_theme: max 75 chars (one short sentence)
- slide1_content: max 1800 chars — "About This Passage:" section + "Key Vocabulary:" section
- slide2_content: max 2700 chars — complete passage ({constraints['word_count_range'][0]}-{constraints['word_count_range'][1]} words)
- slide3_content: max 2700 chars — "Discussion Questions:" section ONLY, no vocabulary
"""

        if worldview_flag == WorldviewFlag.CHRISTIAN:
            prompt += f"""
CHRISTIAN WORLDVIEW GUIDELINES:
- Tone: {christian_guidelines['content_tone']}
- Themes: {christian_guidelines['themes']}
- Avoid: {christian_guidelines['avoid']}
"""

        prompt += """
OUTPUT FORMAT (JSON only, no markdown):
{
  "title": "Story Title Here",
  "bundle_title": "Standard Code Topic Bundle",
  "tagline": "Verb Phrase One | Verb Phrase Two | Verb Phrase Three",
  "objectives": "• Objective one here\\n• Objective two here",
  "directions": "Read the passage carefully and answer the questions that follow.",
  "main_theme": "One concise theme sentence here",
  "slide1_content": "About This Passage:\\n2-3 sentences of background context.\\n\\nKey Vocabulary:\\n• Term One: definition\\n• Term Two: definition\\n• Term Three: definition\\n• Term Four: definition\\n• Term Five: definition",
  "slide2_content": "Complete passage text here...",
  "slide3_content": "Discussion Questions:\\n1. Question one?\\n2. Question two?\\n3. Question three?\\n4. Question four?"
}
"""
        return prompt
