from sqlalchemy import Column, Integer, String, DateTime, Index, Enum
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.enums import Locale, CurriculumBoard, ELAStandardType, GradeLevel

class Standard(Base):
    """ELA educational standards for template-based content generation"""
    __tablename__ = "standards"

    id = Column(Integer, primary_key=True, index=True)
    locale = Column(Enum(Locale), nullable=False, default=Locale.US, index=True)
    curriculum_board = Column(Enum(CurriculumBoard), nullable=False, default=CurriculumBoard.COMMON_CORE, index=True)
    grade_level = Column(Enum(GradeLevel, values_callable=lambda x: [e.value for e in x]), nullable=False, index=True)  # 6, 7, 8
    ela_standard_type = Column(Enum(ELAStandardType), nullable=False, index=True)  # RI or RL
    code = Column(String, nullable=False, index=True)  # e.g., "RI.6.1", "RL.7.2"
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('ix_standards_locale_curriculum', 'locale', 'curriculum_board'),
        Index('ix_standards_grade_ela', 'grade_level', 'ela_standard_type'),
        Index('ix_standards_code_unique', 'locale', 'curriculum_board', 'code', unique=True),
    )