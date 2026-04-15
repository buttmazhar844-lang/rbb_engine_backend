from typing import List, Optional
from sqlalchemy.orm import Session, Query
from app.models.standard import Standard
from app.schemas.standard import StandardCreate
from app.core.enums import Locale, CurriculumBoard, GradeLevel, ELAStandardType

class StandardRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Standard

    def create(self, standard_data: StandardCreate) -> Standard:
        """Create new standard"""
        db_standard = Standard(**standard_data.model_dump())
        self.db.add(db_standard)
        self.db.commit()
        self.db.refresh(db_standard)
        return db_standard

    def get_by_id(self, standard_id: int) -> Optional[Standard]:
        """Get standard by ID"""
        return self.db.query(Standard).filter(Standard.id == standard_id).first()

    def get_all(
        self,
        curriculum_board: Optional[CurriculumBoard] = None,
        grade_level: Optional[GradeLevel] = None,
        ela_standard_type: Optional[ELAStandardType] = None,
        locale: Optional[Locale] = None
    ) -> Query:
        """Get all standards with optional filters"""
        query = self.db.query(Standard)
        
        if curriculum_board:
            query = query.filter(Standard.curriculum_board == curriculum_board)
        if grade_level:
            query = query.filter(Standard.grade_level == grade_level)
        if ela_standard_type:
            query = query.filter(Standard.ela_standard_type == ela_standard_type)
        if locale:
            query = query.filter(Standard.locale == locale)
            
        return query.order_by(Standard.created_at.desc())