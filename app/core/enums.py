from enum import Enum

class Locale(str, Enum):
    """Supported locales - US only for ELA content"""
    US = "US"  # United States

class CurriculumBoard(str, Enum):
    """Educational curriculum boards - Common Core only"""
    COMMON_CORE = "COMMON_CORE"  # Common Core State Standards (US)

class Currency(str, Enum):
    """Supported currencies - USD only"""
    USD = "USD"  # US Dollar

class JobStatus(str, Enum):
    """Generation job statuses - simplified"""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TemplateType(str, Enum):
    """ELA Template types for Christian-facing content"""
    BUNDLE_OVERVIEW = "BUNDLE_OVERVIEW"
    VOCABULARY_PACK = "VOCABULARY_PACK"
    ANCHOR_READING_PASSAGE = "ANCHOR_READING_PASSAGE"
    READING_COMPREHENSION_QUESTIONS = "READING_COMPREHENSION_QUESTIONS"
    SHORT_QUIZ = "SHORT_QUIZ"
    EXIT_TICKETS = "EXIT_TICKETS"
    WRITING_PROMPTS = "WRITING_PROMPTS"

class ProductStatus(str, Enum):
    """Product statuses"""
    DRAFT = "DRAFT"
    GENERATED = "GENERATED"
    FAILED = "FAILED"

class JobType(str, Enum):
    """Generation job types - simplified"""
    SINGLE_TEMPLATE = "SINGLE_TEMPLATE"

class ELAStandardType(str, Enum):
    """ELA Standard types"""
    RI = "RI"  # Reading Informational
    RL = "RL"  # Reading Literature

class GradeLevel(str, Enum):
    """Supported grade levels for ELA content"""
    GRADE_6 = "6"
    GRADE_7 = "7"
    GRADE_8 = "8"

class WorldviewFlag(str, Enum):
    """Content worldview options"""
    CHRISTIAN = "CHRISTIAN"
    NEUTRAL = "NEUTRAL"

class FileType(str, Enum):
    """File artifact types"""
    RAW_JSON = "RAW_JSON"
    FINAL_JSON = "FINAL_JSON"
    METADATA_JSON = "METADATA_JSON"
    PDF = "PDF"
    ZIP = "ZIP"
    THUMBNAIL = "THUMBNAIL"