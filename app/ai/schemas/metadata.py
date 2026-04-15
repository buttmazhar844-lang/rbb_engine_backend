from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class MetadataSchema(BaseModel):
    title: str = Field(..., min_length=10, max_length=100)
    description: str = Field(..., min_length=50, max_length=300)
    tags: List[str] = Field(..., min_length=3, max_length=10)
    seo_keywords: List[str] = Field(..., min_length=5, max_length=15)
    suggested_price: float = Field(..., ge=0.99, le=99.99)
    
    # Educational metadata
    difficulty_level: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    estimated_duration: int = Field(..., ge=15, le=180)  # minutes
    learning_outcomes: List[str] = Field(..., min_length=2, max_length=5)
    
    # Content categorization
    subject_area: str = Field(..., min_length=3, max_length=50)
    topic_focus: str = Field(..., min_length=5, max_length=100)
    skill_level: str = Field(..., pattern="^(foundational|developing|proficient|advanced)$")
    
    # Usage context
    classroom_ready: bool = Field(...)
    homework_suitable: bool = Field(...)
    assessment_type: Optional[str] = Field(None, pattern="^(formative|summative|diagnostic)$")
    
    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        for tag in v:
            if len(tag) < 2 or len(tag) > 30:
                raise ValueError("Each tag must be 2-30 characters")
            if not tag.replace('-', '').replace('_', '').isalnum():
                raise ValueError("Tags must be alphanumeric with hyphens/underscores only")
        return v
    
    @field_validator('seo_keywords')
    @classmethod
    def validate_keywords(cls, v):
        for keyword in v:
            if len(keyword) < 3 or len(keyword) > 50:
                raise ValueError("Each keyword must be 3-50 characters")
        return v
    
    @field_validator('learning_outcomes')
    @classmethod
    def validate_outcomes(cls, v):
        for outcome in v:
            if len(outcome) < 15 or len(outcome) > 150:
                raise ValueError("Each learning outcome must be 15-150 characters")
        return v