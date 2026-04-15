#!/usr/bin/env python3
"""Seed script to populate default ELA standards for grades 6-8"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.standard import Standard
from app.core.enums import Locale, CurriculumBoard, GradeLevel, ELAStandardType

def seed_standards():
    """Seed default standards for all grade levels and ELA types"""
    db = SessionLocal()
    
    try:
        # Check existing standards by grade/type combination
        print("Checking existing standards...")
        existing_count = db.query(Standard).count()
        print(f"Total existing standards: {existing_count}")
        
        standards_data = [
            # Grade 6 RI
            {"grade": GradeLevel.GRADE_6, "type": ELAStandardType.RI, "code": "RI.6.1", "desc": "Cite textual evidence to support analysis"},
            {"grade": GradeLevel.GRADE_6, "type": ELAStandardType.RI, "code": "RI.6.2", "desc": "Determine central idea and provide summary"},
            {"grade": GradeLevel.GRADE_6, "type": ELAStandardType.RI, "code": "RI.6.3", "desc": "Analyze how individuals, events, and ideas develop"},
            
            # Grade 6 RL
            {"grade": GradeLevel.GRADE_6, "type": ELAStandardType.RL, "code": "RL.6.1", "desc": "Cite textual evidence to support analysis"},
            {"grade": GradeLevel.GRADE_6, "type": ELAStandardType.RL, "code": "RL.6.2", "desc": "Determine theme and provide summary"},
            {"grade": GradeLevel.GRADE_6, "type": ELAStandardType.RL, "code": "RL.6.3", "desc": "Describe how plot unfolds and characters respond"},
            
            # Grade 7 RI
            {"grade": GradeLevel.GRADE_7, "type": ELAStandardType.RI, "code": "RI.7.1", "desc": "Cite several pieces of textual evidence"},
            {"grade": GradeLevel.GRADE_7, "type": ELAStandardType.RI, "code": "RI.7.2", "desc": "Determine central ideas and analyze development"},
            {"grade": GradeLevel.GRADE_7, "type": ELAStandardType.RI, "code": "RI.7.3", "desc": "Analyze interactions between individuals, events, and ideas"},
            
            # Grade 7 RL
            {"grade": GradeLevel.GRADE_7, "type": ELAStandardType.RL, "code": "RL.7.1", "desc": "Cite several pieces of textual evidence"},
            {"grade": GradeLevel.GRADE_7, "type": ELAStandardType.RL, "code": "RL.7.2", "desc": "Determine theme and analyze development"},
            {"grade": GradeLevel.GRADE_7, "type": ELAStandardType.RL, "code": "RL.7.3", "desc": "Analyze how elements of story interact"},
            
            # Grade 8 RI
            {"grade": GradeLevel.GRADE_8, "type": ELAStandardType.RI, "code": "RI.8.1", "desc": "Cite strongest textual evidence"},
            {"grade": GradeLevel.GRADE_8, "type": ELAStandardType.RI, "code": "RI.8.2", "desc": "Determine central idea and analyze development"},
            {"grade": GradeLevel.GRADE_8, "type": ELAStandardType.RI, "code": "RI.8.3", "desc": "Analyze connections and distinctions between individuals, ideas, and events"},
            
            # Grade 8 RL
            {"grade": GradeLevel.GRADE_8, "type": ELAStandardType.RL, "code": "RL.8.1", "desc": "Cite strongest textual evidence"},
            {"grade": GradeLevel.GRADE_8, "type": ELAStandardType.RL, "code": "RL.8.2", "desc": "Determine theme and analyze development"},
            {"grade": GradeLevel.GRADE_8, "type": ELAStandardType.RL, "code": "RL.8.3", "desc": "Analyze how dialogue and incidents propel action"},
        ]
        
        added_count = 0
        for std_data in standards_data:
            # Check if this specific standard already exists
            exists = db.query(Standard).filter(
                Standard.code == std_data["code"],
                Standard.grade_level == std_data["grade"],
                Standard.ela_standard_type == std_data["type"]
            ).first()
            
            if not exists:
                standard = Standard(
                    locale=Locale.US,
                    curriculum_board=CurriculumBoard.COMMON_CORE,
                    grade_level=std_data["grade"],
                    ela_standard_type=std_data["type"],
                    code=std_data["code"],
                    description=std_data["desc"]
                )
                db.add(standard)
                added_count += 1
        
        if added_count > 0:
            db.commit()
            print(f"✓ Successfully added {added_count} new standards")
        else:
            print("✓ All standards already exist, no new standards added")
        
        # Print summary
        for grade in [GradeLevel.GRADE_6, GradeLevel.GRADE_7, GradeLevel.GRADE_8]:
            for ela_type in [ELAStandardType.RI, ELAStandardType.RL]:
                count = db.query(Standard).filter(
                    Standard.grade_level == grade,
                    Standard.ela_standard_type == ela_type
                ).count()
                print(f"  Grade {grade.value} {ela_type.value}: {count} standards")
        
    except Exception as e:
        print(f"✗ Error seeding standards: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding ELA standards...")
    seed_standards()
    print("Done!")
