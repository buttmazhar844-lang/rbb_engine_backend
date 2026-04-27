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

CRITICAL: The content is split across 3 slides. You must provide content for each slide separately.

SLIDE STRUCTURE:
- Slide 1 (cover page): Beginning of the passage only — max 1800 chars
- Slide 2 (full passage): The complete passage from beginning to end — max 2700 chars
- Slide 3 (questions): Discussion questions + key vocabulary — max 2700 chars

CRITICAL: Every field has a strict character limit. NEVER exceed it.

FIELD LIMITS:
- title: max 50 chars (story/article title)
- bundle_title: max 60 chars
- tagline: max 65 chars (3 verb phrases separated by " | ")
- objectives: max 220 chars (2 bullet points using •, one per line)
- directions: max 220 chars (1-2 sentences)
- main_theme: max 75 chars (one short sentence, no period)
- slide1_content: max 1800 chars — ONLY the passage text (first {constraints['word_count_range'][0]//2} words approx)
- slide2_content: max 2700 chars — the COMPLETE passage ({constraints['word_count_range'][0]}-{constraints['word_count_range'][1]} words)
- slide3_content: max 2700 chars — Discussion Questions section followed by Key Vocabulary section
"""

        if worldview_flag == WorldviewFlag.CHRISTIAN:
            prompt += f"""
CHRISTIAN WORLDVIEW GUIDELINES:
- Tone: {christian_guidelines['content_tone']}
- Themes: {christian_guidelines['themes']}
- Avoid: {christian_guidelines['avoid']}
"""

        prompt += """
FORMAT FOR slide3_content (use exactly this structure):
Discussion Questions:
1. Question one here?
2. Question two here?
3. Question three here?
4. Question four here?

Key Vocabulary:
• Term One: definition here
• Term Two: definition here
• Term Three: definition here
• Term Four: definition here
• Term Five: definition here

OUTPUT FORMAT (JSON only, no markdown):
{
  "title": "Story Title Here",
  "bundle_title": "Standard Code Topic Bundle",
  "tagline": "Verb Phrase One | Verb Phrase Two | Verb Phrase Three",
  "objectives": "• Objective one here\\n• Objective two here",
  "directions": "Read the passage carefully and answer the questions that follow.",
  "main_theme": "One concise theme sentence here",
  "slide1_content": "Beginning of passage text here...",
  "slide2_content": "Complete passage text from beginning to end...",
  "slide3_content": "Discussion Questions:\\n1. Question one?\\n2. Question two?\\n3. Question three?\\n4. Question four?\\n\\nKey Vocabulary:\\n• Term: definition\\n• Term: definition\\n• Term: definition\\n• Term: definition\\n• Term: definition"
}
"""
        return prompt
