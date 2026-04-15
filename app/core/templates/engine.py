from typing import Dict, Type
from .base import BaseTemplate
from .anchor_reading_passage import AnchorReadingPassageTemplate
from .bundle_overview import BundleOverviewTemplate
from .exit_tickets import ExitTicketsTemplate
from .reading_comprehension_questions import ReadingComprehensionQuestionsTemplate
from .short_quiz import ShortQuizTemplate
from .vocabulary_pack import VocabularyPackTemplate
from .writing_prompts import WritingPromptsTemplate
from ..enums import TemplateType

class TemplateEngine:
    def __init__(self):
        self._templates: Dict[TemplateType, Type[BaseTemplate]] = {
            TemplateType.ANCHOR_READING_PASSAGE:          AnchorReadingPassageTemplate,
            TemplateType.BUNDLE_OVERVIEW:                 BundleOverviewTemplate,
            TemplateType.EXIT_TICKETS:                    ExitTicketsTemplate,
            TemplateType.READING_COMPREHENSION_QUESTIONS: ReadingComprehensionQuestionsTemplate,
            TemplateType.SHORT_QUIZ:                      ShortQuizTemplate,
            TemplateType.VOCABULARY_PACK:                 VocabularyPackTemplate,
            TemplateType.WRITING_PROMPTS:                 WritingPromptsTemplate,
        }
    
    def get_template(self, template_type: TemplateType) -> BaseTemplate:
        if template_type not in self._templates:
            raise ValueError(f"Template type {template_type} not implemented")
        return self._templates[template_type]()
    
    def get_available_templates(self) -> list[TemplateType]:
        return list(self._templates.keys())
    
    def get_template_structure(self, template_type: TemplateType) -> dict:
        template = self.get_template(template_type)
        return {
            "template_type": template.template_type,
            "fields": [field.dict() for field in template.structure.fields],
            "christian_guidelines": template.structure.christian_guidelines,
            "grade_constraints": {
                str(grade): constraints 
                for grade, constraints in template.structure.grade_constraints.items()
            }
        }

# Global template engine instance
template_engine = TemplateEngine()