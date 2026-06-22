from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from ..enums import TemplateType, WorldviewFlag, GradeLevel

LENGTH_CONTROL_INSTRUCTION = (
    "Generate content that stays within the specified minimum and maximum length limits. "
    "Do not make the content too short, vague, or underdeveloped. "
    "Do not exceed the maximum length because the PPTX template has fixed text areas. "
    "Keep the output classroom-ready, complete, and concise."
)

class TemplateField(BaseModel):
    name: str
    type: str
    required: bool = True
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    min_items: Optional[int] = None
    max_items: Optional[int] = None
    min_word_count: Optional[int] = None
    max_word_count: Optional[int] = None
    constraints: List[str] = []

class TemplateStructure(BaseModel):
    template_type: TemplateType
    fields: List[TemplateField]
    christian_guidelines: Dict[str, str] = {}
    grade_constraints: Dict[GradeLevel, Dict[str, Any]] = {}

class BaseTemplate(ABC):
    def __init__(self, template_type: TemplateType):
        self.template_type = template_type
        self.structure = self.define_structure()
    
    @abstractmethod
    def define_structure(self) -> TemplateStructure:
        pass
    
    @abstractmethod
    def generate_prompt(self, standard_code: str, grade_level: GradeLevel, 
                       worldview_flag: WorldviewFlag) -> str:
        pass
    
    def validate_content(self, content: Dict[str, Any]) -> List[str]:
        errors = []
        for field in self.structure.fields:
            if field.required and field.name not in content:
                errors.append(f"Missing required field: {field.name}")
                continue
            if field.name not in content:
                continue
            value = content[field.name]
            if field.max_length and isinstance(value, str) and len(value) > field.max_length:
                errors.append(f"{field.name} exceeds max length of {field.max_length}")
            if field.min_length and isinstance(value, str) and len(value) < field.min_length:
                errors.append(f"{field.name} below min length of {field.min_length}")
            if field.max_word_count and isinstance(value, str):
                wc = len(value.split())
                if wc > field.max_word_count:
                    errors.append(f"{field.name} exceeds max word count of {field.max_word_count} (got {wc})")
            if field.min_word_count and isinstance(value, str):
                wc = len(value.split())
                if wc < field.min_word_count:
                    errors.append(f"{field.name} below min word count of {field.min_word_count} (got {wc})")
            if isinstance(value, list):
                if field.min_items and len(value) < field.min_items:
                    errors.append(f"{field.name} has fewer than {field.min_items} items (got {len(value)})")
                if field.max_items and len(value) > field.max_items:
                    errors.append(f"{field.name} has more than {field.max_items} items (got {len(value)})")
        return errors
    
    def has_length_violations(self, content: Dict[str, Any]) -> bool:
        return bool(self.validate_content(content))
