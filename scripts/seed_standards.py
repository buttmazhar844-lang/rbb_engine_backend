#!/usr/bin/env python3
"""Seed script to populate all ELA standards for grades 6-8 (Common Core)"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.standard import Standard
from app.core.enums import Locale, CurriculumBoard, GradeLevel, ELAStandardType

STANDARDS = [
    # ── Grade 6 RI ──────────────────────────────────────────────────────────
    ("6", "RI", "RI.6.1",  "Cite textual evidence to support analysis of what the text says explicitly as well as inferences drawn from the text"),
    ("6", "RI", "RI.6.2",  "Determine central ideas or themes of a text and analyze their development; summarize the key supporting details and ideas"),
    ("6", "RI", "RI.6.3",  "Analyze how a key individual, event, or idea is introduced, illustrated, and elaborated in a text"),
    ("6", "RI", "RI.6.4",  "Determine the meaning of words and phrases as they are used in a text, including figurative, connotative, and technical meanings"),
    ("6", "RI", "RI.6.5",  "Analyze how a particular sentence, paragraph, chapter, or section fits into the overall structure of a text"),
    ("6", "RI", "RI.6.6",  "Determine an author's point of view or purpose in a text and explain how it is conveyed in the text"),
    ("6", "RI", "RI.6.7",  "Integrate information presented in different media or formats to develop a coherent understanding of a topic"),
    ("6", "RI", "RI.6.8",  "Trace and evaluate the argument and specific claims in a text, distinguishing claims that are supported by reasons and evidence"),
    ("6", "RI", "RI.6.9",  "Compare and contrast one author's presentation of events with that of another"),
    ("6", "RI", "RI.6.10", "Read and comprehend literary nonfiction in the grades 6-8 text complexity band proficiently"),

    # ── Grade 6 RL ──────────────────────────────────────────────────────────
    ("6", "RL", "RL.6.1",  "Cite textual evidence to support analysis of what the text says explicitly as well as inferences drawn from the text"),
    ("6", "RL", "RL.6.2",  "Determine a theme or central idea of a text and how it is conveyed through particular details; provide a summary"),
    ("6", "RL", "RL.6.3",  "Describe how a particular story's or drama's plot unfolds in a series of episodes and how characters respond or change"),
    ("6", "RL", "RL.6.4",  "Determine the meaning of words and phrases as they are used in a text, including figurative and connotative meanings"),
    ("6", "RL", "RL.6.5",  "Analyze how a particular sentence, chapter, scene, or stanza fits into the overall structure of a text"),
    ("6", "RL", "RL.6.6",  "Explain how an author develops the point of view of the narrator or speaker in a text"),
    ("6", "RL", "RL.6.7",  "Compare and contrast the experience of reading a story, drama, or poem to listening to or viewing an audio, video, or live version"),
    ("6", "RL", "RL.6.9",  "Compare and contrast texts in different forms or genres in terms of their approaches to similar themes and topics"),
    ("6", "RL", "RL.6.10", "Read and comprehend literature, including stories, dramas, and poems, in the grades 6-8 text complexity band proficiently"),

    # ── Grade 7 RI ──────────────────────────────────────────────────────────
    ("7", "RI", "RI.7.1",  "Cite several pieces of textual evidence to support analysis of what the text says explicitly as well as inferences drawn from the text"),
    ("7", "RI", "RI.7.2",  "Determine two or more central ideas in a text and analyze their development over the course of the text; provide a summary"),
    ("7", "RI", "RI.7.3",  "Analyze the interactions between individuals, events, and ideas in a text"),
    ("7", "RI", "RI.7.4",  "Determine the meaning of words and phrases as they are used in a text, including figurative, connotative, and technical meanings"),
    ("7", "RI", "RI.7.5",  "Analyze the structure an author uses to organize a text, including how the major sections contribute to the whole"),
    ("7", "RI", "RI.7.6",  "Determine an author's point of view or purpose in a text and analyze how the author distinguishes their position from others"),
    ("7", "RI", "RI.7.7",  "Compare and contrast a text to an audio, video, or multimedia version of the text, analyzing each medium's portrayal"),
    ("7", "RI", "RI.7.8",  "Trace and evaluate the argument and specific claims in a text, assessing whether the reasoning is sound and the evidence is relevant"),
    ("7", "RI", "RI.7.9",  "Analyze how two or more authors writing about the same topic shape their presentations of key information"),
    ("7", "RI", "RI.7.10", "Read and comprehend literary nonfiction in the grades 6-8 text complexity band proficiently"),

    # ── Grade 7 RL ──────────────────────────────────────────────────────────
    ("7", "RL", "RL.7.1",  "Cite several pieces of textual evidence to support analysis of what the text says explicitly as well as inferences drawn from the text"),
    ("7", "RL", "RL.7.2",  "Determine a theme or central idea of a text and analyze its development over the course of the text; provide a summary"),
    ("7", "RL", "RL.7.3",  "Analyze how particular elements of a story or drama interact"),
    ("7", "RL", "RL.7.4",  "Determine the meaning of words and phrases as they are used in a text, including figurative and connotative meanings"),
    ("7", "RL", "RL.7.5",  "Analyze how a drama's or poem's form or structure contributes to its meaning"),
    ("7", "RL", "RL.7.6",  "Analyze how an author develops and contrasts the points of view of different characters or narrators in a text"),
    ("7", "RL", "RL.7.7",  "Compare and contrast a written story, drama, or poem to its audio, filmed, staged, or multimedia version"),
    ("7", "RL", "RL.7.9",  "Compare and contrast a fictional portrayal of a time, place, or character and a historical account of the same period"),
    ("7", "RL", "RL.7.10", "Read and comprehend literature, including stories, dramas, and poems, in the grades 6-8 text complexity band proficiently"),

    # ── Grade 8 RI ──────────────────────────────────────────────────────────
    ("8", "RI", "RI.8.1",  "Cite the textual evidence that most strongly supports an analysis of what the text says explicitly as well as inferences drawn from the text"),
    ("8", "RI", "RI.8.2",  "Determine a central idea of a text and analyze its development over the course of the text, including its relationship to supporting ideas; provide a summary"),
    ("8", "RI", "RI.8.3",  "Analyze how a text makes connections among and distinctions between individuals, ideas, or events"),
    ("8", "RI", "RI.8.4",  "Determine the meaning of words and phrases as they are used in a text, including figurative, connotative, and technical meanings"),
    ("8", "RI", "RI.8.5",  "Analyze in detail the structure of a specific paragraph in a text, including the role of particular sentences in developing and refining a key concept"),
    ("8", "RI", "RI.8.6",  "Determine an author's point of view or purpose in a text and analyze how the author acknowledges and responds to conflicting evidence or viewpoints"),
    ("8", "RI", "RI.8.7",  "Evaluate the advantages and disadvantages of using different mediums to present a particular topic or idea"),
    ("8", "RI", "RI.8.8",  "Delineate and evaluate the argument and specific claims in a text, assessing whether the reasoning is sound and the evidence is relevant and sufficient"),
    ("8", "RI", "RI.8.9",  "Analyze a case in which two or more texts provide conflicting information on the same topic"),
    ("8", "RI", "RI.8.10", "Read and comprehend literary nonfiction at the high end of the grades 6-8 text complexity band independently and proficiently"),

    # ── Grade 8 RL ──────────────────────────────────────────────────────────
    ("8", "RL", "RL.8.1",  "Cite the textual evidence that most strongly supports an analysis of what the text says explicitly as well as inferences drawn from the text"),
    ("8", "RL", "RL.8.2",  "Determine a theme or central idea of a text and analyze its development over the course of the text, including its relationship to the characters, setting, and plot; provide a summary"),
    ("8", "RL", "RL.8.3",  "Analyze how particular lines of dialogue or incidents in a story or drama propel the action, reveal aspects of a character, or provoke a decision"),
    ("8", "RL", "RL.8.4",  "Determine the meaning of words and phrases as they are used in a text, including figurative and connotative meanings"),
    ("8", "RL", "RL.8.5",  "Compare and contrast the structure of two or more texts and analyze how the differing structure of each text contributes to its meaning and style"),
    ("8", "RL", "RL.8.6",  "Analyze how differences in the points of view of the characters and the audience or reader create such effects as suspense or humor"),
    ("8", "RL", "RL.8.7",  "Analyze the extent to which a filmed or live production of a story or drama stays faithful to or departs from the text or script"),
    ("8", "RL", "RL.8.9",  "Analyze how a modern work of fiction draws on themes, patterns of events, or character types from myths, traditional stories, or religious works"),
    ("8", "RL", "RL.8.10", "Read and comprehend literature, including stories, dramas, and poems, at the high end of grades 6-8 text complexity band independently and proficiently"),
]


def seed_standards():
    db = SessionLocal()
    try:
        added = 0
        skipped = 0
        updated = 0
        for grade_val, type_val, code, desc in STANDARDS:
            grade  = GradeLevel(grade_val)
            ela    = ELAStandardType(type_val)
            exists = db.query(Standard).filter(Standard.code == code).first()
            if exists:
                if exists.description != desc:
                    exists.description = desc
                    exists.ela_standard_type = ela
                    updated += 1
                else:
                    skipped += 1
                continue
            db.add(Standard(
                locale=Locale.US,
                curriculum_board=CurriculumBoard.COMMON_CORE,
                grade_level=grade,
                ela_standard_type=ela,
                code=code,
                description=desc,
            ))
            added += 1

        db.commit()
        print(f"✓ Added {added}, updated {updated}, skipped {skipped} standards")

        for grade in [GradeLevel.GRADE_6, GradeLevel.GRADE_7, GradeLevel.GRADE_8]:
            for ela_type in [ELAStandardType.RI, ELAStandardType.RL]:
                count = db.query(Standard).filter(
                    Standard.grade_level == grade,
                    Standard.ela_standard_type == ela_type
                ).count()
                print(f"  Grade {grade.value} {ela_type.value}: {count} standards")

    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Seeding ELA standards...")
    seed_standards()
    print("Done!")
