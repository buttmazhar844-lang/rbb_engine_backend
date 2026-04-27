from typing import Dict, Any
from .base import BaseTemplate, TemplateStructure, TemplateField
from ..enums import TemplateType, WorldviewFlag, GradeLevel


class BundleOverviewTemplate(BaseTemplate):
    def __init__(self):
        super().__init__(TemplateType.BUNDLE_OVERVIEW)

    def define_structure(self) -> TemplateStructure:
        return TemplateStructure(
            template_type=TemplateType.BUNDLE_OVERVIEW,
            fields=[
                TemplateField(name="title", type="string", max_length=100),
                TemplateField(name="standard_alignment_title", type="string", max_length=100),
                TemplateField(name="standard_alignment_content", type="string", max_length=500),
                TemplateField(name="standard_breakdown_title", type="string", max_length=100),
                TemplateField(name="standard_breakdown_content", type="string", max_length=800),
                TemplateField(name="whats_included_title", type="string", max_length=100),
                TemplateField(name="whats_included_content", type="string", max_length=800),
                TemplateField(name="learning_objectives_title", type="string", max_length=100),
                TemplateField(name="learning_objectives_content", type="string", max_length=600),
                TemplateField(name="suggested_pacing_title", type="string", max_length=100),
                TemplateField(name="suggested_pacing_content", type="string", max_length=600),
                TemplateField(name="materials_needed_title", type="string", max_length=100),
                TemplateField(name="materials_needed_content", type="string", max_length=700),
                TemplateField(name="differentiation_tips_title", type="string", max_length=100),
                TemplateField(name="differentiation_tips_content", type="string", max_length=800),
                TemplateField(name="assessment_overview_title", type="string", max_length=100),
                TemplateField(name="assessment_overview_content", type="string", max_length=700),
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
Generate a Bundle Overview for ELA Standard {standard_code}, Grade {grade_level.value}.

CRITICAL: The "title" field MUST be exactly "Bundle Overview". Do not change it.
{"Apply a Christian worldview perspective where appropriate." if christian else ""}

CRITICAL: Every field has a strict character limit. NEVER exceed it.

FIELD LIMITS (characters including spaces):
- title: exactly "Bundle Overview"
- bundle_title: max 60 chars (e.g. "{standard_code} Topic Bundle")
- tagline: max 65 chars (3 verb phrases separated by " | ")
- standard_alignment_title: max 75 chars
- standard_alignment_content: max 300 chars (2-3 sentences)
- standard_breakdown_title: max 75 chars
- standard_breakdown_content: max 600 chars (4 short lines using labels like "What students must know:", "What students must do:", "Required skills:", "Depth of knowledge:")
- whats_included_title: max 75 chars
- whats_included_content: max 700 chars (numbered list 1-12, one item per line)
- learning_objectives_title: max 75 chars
- learning_objectives_content: max 450 chars (5-6 bullet points using •, one per line)
- suggested_pacing_title: max 75 chars
- suggested_pacing_content: max 520 chars (5 lines: "Day 1: ...", "Day 2: ...", etc.)
- materials_needed_title: max 75 chars
- materials_needed_content: max 600 chars (bullet points using •, one per line)
- differentiation_tips_title: max 75 chars
- differentiation_tips_content: max 680 chars (3 short paragraphs: "For Struggling Readers:", "For Advanced Learners:", "For ELL Students:")
- assessment_overview_title: max 75 chars
- assessment_overview_content: max 520 chars (3 lines: "Formative:", "Summative:", "Standards-Based:")

OUTPUT FORMAT (JSON only, no markdown):
{{
  "title": "Bundle Overview",
  "bundle_title": "{standard_code} [Topic] Bundle",
  "tagline": "[Verb Phrase] | [Verb Phrase] | [Verb Phrase]",
  "standard_alignment_title": "Standard Alignment",
  "standard_alignment_content": "{standard_code}: [full standard description]",
  "standard_breakdown_title": "Standard Breakdown",
  "standard_breakdown_content": "What students must know: ...\\nWhat students must do: ...\\nRequired skills: ...\\nDepth of knowledge: ...",
  "whats_included_title": "What's Included",
  "whats_included_content": "1. Bundle Overview Page\\n2. Vocabulary Pack\\n3. Anchor Reading Passages\\n4. Reading Comprehension Questions\\n5. Writing Prompt Pack\\n6. Graphic Organizer Pack\\n7. Mini-Lesson & Anchor Chart\\n8. Exit Tickets\\n9. Short Quiz\\n10. Performance Task\\n11. Homework Page\\n12. Final Review Page + Answer Key",
  "learning_objectives_title": "Learning Objectives",
  "learning_objectives_content": "• Objective one\\n• Objective two\\n• Objective three\\n• Objective four\\n• Objective five",
  "suggested_pacing_title": "Suggested Pacing",
  "suggested_pacing_content": "Day 1: ...\\nDay 2: ...\\nDay 3: ...\\nDay 4: ...\\nDay 5: ...",
  "materials_needed_title": "Materials Needed",
  "materials_needed_content": "• Item one\\n• Item two\\n• Item three\\n• Item four",
  "differentiation_tips_title": "Differentiation Tips",
  "differentiation_tips_content": "For Struggling Readers: ...\\nFor Advanced Learners: ...\\nFor ELL Students: ...",
  "assessment_overview_title": "Assessment Overview",
  "assessment_overview_content": "Formative: ...\\nSummative: ...\\nStandards-Based: ..."
}}
"""
