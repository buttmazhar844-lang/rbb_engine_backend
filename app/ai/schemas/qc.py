from pydantic import BaseModel, Field, field_validator
from typing import List

class QCIssue(BaseModel):
    category: str = Field(..., pattern="^(structure|alignment|clarity|difficulty|inclusivity|accuracy)$")
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    description: str = Field(..., min_length=10, max_length=200)
    suggestion: str = Field(..., min_length=10, max_length=200)

class QCSchema(BaseModel):
    verdict: str = Field(..., pattern="^(PASS|NEEDS_FIX|FAIL)$")
    score: int = Field(..., ge=0, le=100)
    issues: List[QCIssue] = Field(..., max_length=10)
    
    # Detailed scores by category
    structure_score: int = Field(..., ge=0, le=100)
    alignment_score: int = Field(..., ge=0, le=100)
    clarity_score: int = Field(..., ge=0, le=100)
    difficulty_score: int = Field(..., ge=0, le=100)
    inclusivity_score: int = Field(..., ge=0, le=100)
    accuracy_score: int = Field(..., ge=0, le=100)
    
    # Summary
    strengths: List[str] = Field(..., min_length=1, max_length=5)
    recommendations: List[str] = Field(..., max_length=5)
    
    @field_validator('score')
    @classmethod
    def validate_overall_score(cls, v, info):
        # Overall score should be average of category scores
        data = info.data
        category_scores = [
            data.get('structure_score', 0),
            data.get('alignment_score', 0),
            data.get('clarity_score', 0),
            data.get('difficulty_score', 0),
            data.get('inclusivity_score', 0),
            data.get('accuracy_score', 0)
        ]
        expected_avg = sum(category_scores) // 6
        if abs(v - expected_avg) > 5:  # Allow 5 point variance
            raise ValueError("Overall score should approximate category average")
        return v
    
    @field_validator('verdict')
    @classmethod
    def validate_verdict_consistency(cls, v, info):
        score = info.data.get('score', 0)
        if v == 'PASS' and score < 75:
            raise ValueError("PASS verdict requires score >= 75")
        if v == 'FAIL' and score > 50:
            raise ValueError("FAIL verdict requires score <= 50")
        return v