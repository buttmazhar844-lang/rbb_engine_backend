from pydantic import BaseModel, Field
from typing import List, Optional

class PassageSchema(BaseModel):
    title: str = Field(..., min_length=10, max_length=100)
    content: str = Field(..., min_length=200, max_length=2000)
    reading_level: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    word_count: int = Field(..., ge=150, le=1500)
    comprehension_questions: List[str] = Field(..., min_length=3, max_length=8)
    vocabulary_words: List[str] = Field(..., min_length=5, max_length=15)
    discussion_prompts: List[str] = Field(..., min_length=2, max_length=5)

class QuizSchema(BaseModel):
    title: str = Field(..., min_length=10, max_length=100)
    instructions: str = Field(..., min_length=20, max_length=300)
    questions: List[dict] = Field(..., min_length=5, max_length=20)
    time_limit: int = Field(..., ge=10, le=60)  # minutes
    total_points: int = Field(..., ge=5, le=100)

class AssessmentSchema(BaseModel):
    title: str = Field(..., min_length=10, max_length=100)
    instructions: str = Field(..., min_length=50, max_length=500)
    sections: List[dict] = Field(..., min_length=2, max_length=5)
    rubric: dict = Field(...)
    total_points: int = Field(..., ge=20, le=200)
    estimated_time: int = Field(..., ge=30, le=180)  # minutes