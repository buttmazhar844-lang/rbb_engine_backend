from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel
from ..enums import TemplateType, WorldviewFlag, GradeLevel

class TemplateField(BaseModel):
    name: str
    type: str
    required: bool = True
    max_length: int = None
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
            elif field.name in content and field.max_length:
                if len(str(content[field.name])) > field.max_length:
                    errors.append(f"{field.name} exceeds max length of {field.max_length}")
        return errors