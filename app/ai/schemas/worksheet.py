from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class WorksheetQuestion(BaseModel):
    question_number: int = Field(..., ge=1)
    question_text: str = Field(..., min_length=10, max_length=500)
    question_type: str = Field(..., pattern="^(multiple_choice|short_answer|problem_solving|creative)$")
    options: Optional[List[str]] = Field(None, min_length=2, max_length=5)
    correct_answer: str = Field(..., min_length=1, max_length=200)
    explanation: str = Field(..., min_length=10, max_length=300)
    points: int = Field(..., ge=1, le=10)

class WorksheetExtension(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=20, max_length=300)
    difficulty: str = Field(..., pattern="^(advanced|enrichment|challenge)$")

class WorksheetSchema(BaseModel):
    title: str = Field(..., min_length=10, max_length=100)
    learning_objectives: List[str] = Field(..., min_length=2, max_length=4)
    instructions: str = Field(..., min_length=50, max_length=500)
    estimated_time: int = Field(..., ge=15, le=120)  # minutes
    questions: List[WorksheetQuestion] = Field(..., min_length=8, max_length=12)
    extensions: List[WorksheetExtension] = Field(..., min_length=2, max_length=3)
    total_points: int = Field(..., ge=8, le=100)
    
    @field_validator('learning_objectives')
    @classmethod
    def validate_objectives(cls, v):
        for obj in v:
            if len(obj) < 10 or len(obj) > 150:
                raise ValueError("Each learning objective must be 10-150 characters")
        return v
    
    @field_validator('questions')
    @classmethod
    def validate_questions(cls, v):
        question_types = [q.question_type for q in v]
        if question_types.count('multiple_choice') < 2:
            raise ValueError("Must have at least 2 multiple choice questions")
        if question_types.count('short_answer') < 3:
            raise ValueError("Must have at least 3 short answer questions")
        return v
    
    @field_validator('total_points')
    @classmethod
    def validate_total_points(cls, v, info):
        if 'questions' in info.data:
            calculated_total = sum(q.points for q in info.data['questions'])
            if v != calculated_total:
                raise ValueError("Total points must equal sum of question points")
        return v