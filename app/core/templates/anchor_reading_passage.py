from typing import Dict, Any, List
from .base import BaseTemplate, TemplateStructure, TemplateField, LENGTH_CONTROL_INSTRUCTION
from ..enums import TemplateType, WorldviewFlag, GradeLevel


class AnchorReadingPassageTemplate(BaseTemplate):
    def __init__(self):
        super().__init__(TemplateType.ANCHOR_READING_PASSAGE)

    def define_structure(self) -> TemplateStructure:
        return TemplateStructure(
            template_type=TemplateType.ANCHOR_READING_PASSAGE,
            fields=[
                TemplateField(name="title", type="string", max_length=100),
                TemplateField(name="slide1_content", type="text", max_length=1840,
                              constraints=["min 1 sentence about section", "key vocabulary: 5-7 words"]),
                TemplateField(name="slide2_content", type="text", max_length=2754,
                              min_word_count=350, max_word_count=500),
                TemplateField(name="slide3_content", type="text", max_length=2754,
                              constraints=["discussion questions: 4-5 questions"]),
                TemplateField(name="main_theme", type="string", max_length=80),
            ],
            christian_guidelines={
                "content_tone": "Academic and informative, values-aligned but not preachy",
                "themes": "Focus on character, perseverance, wisdom, service to others",
                "avoid": "Sermon-like language, direct Bible citations unless requested",
                "approach": "Integrate Christian values naturally through story themes"
            },
            grade_constraints={
                GradeLevel.GRADE_6: {"word_count_range": [350, 500], "reading_level": "6.0-6.9", "vocabulary_complexity": "grade_appropriate"},
                GradeLevel.GRADE_7: {"word_count_range": [350, 500], "reading_level": "7.0-7.9", "vocabulary_complexity": "slightly_challenging"},
                GradeLevel.GRADE_8: {"word_count_range": [350, 500], "reading_level": "8.0-8.9", "vocabulary_complexity": "challenging"}
            }
        )

    def validate_content(self, content: Dict[str, Any]) -> List[str]:
        errors = super().validate_content(content)
        passage = content.get('slide2_content', '')
        if passage:
            last_char = passage.strip()[-1] if passage.strip() else ''
            if last_char not in '.!?"':
                errors.append("slide2_content (passage) ends abruptly — must end with a complete sentence")
        return errors

    def generate_prompt(self, standard_code: str, grade_level: GradeLevel,
                        worldview_flag: WorldviewFlag) -> str:
        constraints = self.structure.grade_constraints[grade_level]
        christian_guidelines = self.structure.christian_guidelines if worldview_flag == WorldviewFlag.CHRISTIAN else {}

        prompt = f"""
Generate an Anchor Reading Passage for ELA Standard {standard_code}, Grade {grade_level.value}.

{LENGTH_CONTROL_INSTRUCTION}

CRITICAL: Content is split across 3 slides. Each slide gets different content. NO repetition across slides.

SLIDE STRUCTURE:
- Slide 1 (cover page content box): Background context (1–3 sentences) + Key Vocabulary (5–7 words) ONLY
- Slide 2 (reading page): The complete passage ONLY — MUST be 350–500 words. Must have a clear beginning, middle, and ending. Do NOT end mid-sentence or mid-paragraph.
- Slide 3 (questions page): Discussion Questions ONLY (4–5 questions) — NO vocabulary here

CRITICAL: Every field has a strict character limit. NEVER exceed it.

FIELD LIMITS:
- title: max 50 chars
- bundle_title: max 60 chars
- tagline: max 65 chars (3 verb phrases separated by " | ")
- objectives: max 220 chars (2 bullet points using •, one per line)
- directions: max 220 chars (1-2 sentences)
- main_theme: max 75 chars (one short sentence)
- slide1_content: max 1800 chars — "About This Passage:" section (1–3 sentences) + "Key Vocabulary:" section (exactly 5–7 bullet items)
- slide2_content: max 2700 chars — complete passage EXACTLY 350–500 words, ending with a complete sentence
- slide3_content: max 2700 chars — "Discussion Questions:" section with EXACTLY 4–5 numbered questions, NO vocabulary
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
  "slide2_content": "Complete passage text here (350-500 words, ending with a complete sentence)...",
  "slide3_content": "Discussion Questions:\\n1. Question one?\\n2. Question two?\\n3. Question three?\\n4. Question four?"
}
"""
        return prompt
